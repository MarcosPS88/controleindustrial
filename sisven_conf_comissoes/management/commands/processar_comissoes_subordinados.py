import logging
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from django.core.management.base import BaseCommand
from django.db import transaction, models
import json

# Importando os models do Sisven
from sisven_core.models import Ped01, ComLogPedRepCli, ComCliEsp, ComRepSub

# Importando os models do Acedata
from acedata_core.models import Pdv01, Pdv02, Pdv03

# Configurando um logger para registrar informações importantes
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Verifica pedidos novos e ATIVOS, aplica as regras de comissão e insere os registros no Acedata.'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('--- Iniciando rotina de verificação de comissão para representantes subordinados ---'))

        pedidos_a_verificar = Ped01.objects.using('sisven').filter(
            rotina_gera_com_rep='N',
            pedsta='ATIVO'
        ).select_related('cliente', 'representante')

        if not pedidos_a_verificar.exists():
            self.stdout.write(self.style.NOTICE('Nenhum pedido novo e ativo para processar.'))
            return

        self.stdout.write(f'Encontrados {pedidos_a_verificar.count()} pedidos para verificação.')

        for pedido in pedidos_a_verificar:
            try:
                # Transação principal para o banco Sisven
                with transaction.atomic(using='sisven'):
                    self.stdout.write(
                        f"\n--- Processando Pedido Sisven: {pedido.pedcod} | Cliente: {pedido.pedclinom} ({pedido.cliente_id}) ---")

                    comissao_info = self.apurar_comissao_para_pedido(pedido)

                    if comissao_info:
                        self.stdout.write(self.style.SUCCESS(
                            f"  [SUCESSO] Comissão apurada para o pedido {pedido.pedcod}:\n"
                            f"  - Representante Subordinado: {comissao_info['representante_subordinado'].codigo} ({comissao_info['representante_subordinado'].nome})\n"
                            f"  - Percentual: {comissao_info['percentual']:.2f}%\n"
                            f"  - Origem da Regra: {comissao_info['origem']}"
                        ))

                        # ==============================================================================
                        # PARTE 2: INSERÇÃO REAL DA COMISSÃO NO ACEDATA
                        # ==============================================================================
                        self.inserir_comissao_acedata(comissao_info, pedido)

                    else:
                        self.stdout.write(self.style.WARNING(
                            f"  [INFO] Nenhuma comissão de representante subordinado aplicável para o pedido {pedido.pedcod}."
                        ))

                    # Se tudo correu bem (incluindo a inserção no Acedata), marca o pedido como processado.
                    # Descomentar as linhas abaixo após os testes
                    #pedido.rotina_gera_com_rep = 'S'
                    #pedido.save(using='sisven', update_fields=['rotina_gera_com_rep'])
                    self.stdout.write(self.style.HTTP_INFO(
                        f"  - Status Sisven: Pedido {pedido.pedcod} marcado como processado ('S')."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'ERRO CRÍTICO ao processar o pedido {pedido.pedcod}: {e}'))
                continue

        self.stdout.write(self.style.SUCCESS('\n--- Rotina finalizada com sucesso! ---'))

    def inserir_comissao_acedata(self, comissao_info, pedido_sisven: Ped01):
        """
        Localiza o pedido no Acedata e INSERE os registros de comissão na PDV03.
        """
        subordinado = comissao_info['representante_subordinado']
        percentual_comissao = Decimal(str(comissao_info['percentual']))

        try:
            pedido_acedata = Pdv01.objects.using('acedata').get(pdvcodpocket=pedido_sisven.pedcod)
            self.stdout.write(
                f"  - Acedata: Pedido {pedido_acedata.pdvcod} (Pocket: {pedido_acedata.pdvcodpocket}) encontrado.")

            itens_pedido_acedata = Pdv02.objects.using('acedata').filter(
                pdvempcod=pedido_acedata.pdvempcod, pdvfilcod=pedido_acedata.pdvfilcod,
                pdvpfxcod=pedido_acedata.pdvpfxcod, pdvcod=pedido_acedata.pdvcod
            ).order_by('pdvitmpro')

            if not itens_pedido_acedata.exists():
                raise Exception("Nenhum item (PDV02) encontrado para este pedido no Acedata.")

            # --- ESTRATÉGIA CORRIGIDA ---
            # 1. Encontrar o maior PdvCItmCom para o PEDIDO INTEIRO.
            ultima_comissao_no_pedido = Pdv03.objects.using('acedata').filter(
                pdvempcod=pedido_acedata.pdvempcod, pdvfilcod=pedido_acedata.pdvfilcod,
                pdvpfxcod=pedido_acedata.pdvpfxcod, pdvcod=pedido_acedata.pdvcod
            ).order_by('-pdvcitmcom').first()

            # 2. Iniciar nosso contador a partir do maior valor encontrado.
            proxima_seq_comissao_contador = (ultima_comissao_no_pedido.pdvcitmcom if ultima_comissao_no_pedido else 0)

            with transaction.atomic(using='acedata'):
                self.stdout.write(
                    f"  - Acedata: Iniciando inserção de comissão para {itens_pedido_acedata.count()} item(ns).")
                for item in itens_pedido_acedata:
                    comissao_principal_molde = Pdv03.objects.using('acedata').filter(
                        pdvempcod=item.pdvempcod, pdvfilcod=item.pdvfilcod,
                        pdvpfxcod=item.pdvpfxcod, pdvcod=item.pdvcod,
                        pdvcitmped=item.pdvitmpro
                    ).order_by('-pdvcitmcom').first()

                    if not comissao_principal_molde:
                        self.stdout.write(self.style.WARNING(
                            f"    - Alerta: Nenhuma comissão principal encontrada para o item {item.pdvitmpro}. Pulando."))
                        continue

                    # 3. Incrementar o contador para cada NOVO registro a ser inserido.
                    proxima_seq_comissao_contador += 1

                    base_calculo = Decimal(str(item.pdvtotitm))
                    valor_comissao = (base_calculo * (percentual_comissao / Decimal(100))).quantize(
                        Decimal('0.01'), rounding=ROUND_HALF_UP
                    )

                    # Criando um novo objeto Pdv03 do zero para evitar erros de PK
                    nova_comissao = Pdv03()

                    # Copiando todos os campos do molde para a nova instância
                    for field in Pdv03._meta.fields:
                        # Ignora o campo de ID automático se houver um
                        if field.auto_created:
                            continue
                        setattr(nova_comissao, field.name, getattr(comissao_principal_molde, field.name))

                    # Sobrescrevendo os campos específicos da nova comissão
                    nova_comissao.pdvcitmcom = proxima_seq_comissao_contador  # Usa o contador do pedido
                    nova_comissao.pdvcrepdoc = subordinado.codigo
                    nova_comissao.pdvccompor = percentual_comissao
                    nova_comissao.pdvccombas = base_calculo
                    nova_comissao.pdvccomval = valor_comissao
                    nova_comissao.pdvcreptip = 'C'
                    nova_comissao.pdvccomtip = 'M'

                    nova_comissao.save(using='acedata', force_insert=True)

                    self.stdout.write(self.style.SUCCESS(
                        f"    - Item {item.pdvitmpro}: Comissão (Seq {proxima_seq_comissao_contador}) de {percentual_comissao:.2f}% "
                        f"(R$ {valor_comissao:.2f}) inserida para o rep {subordinado.codigo}."
                    ))

        except Pdv01.DoesNotExist:
            raise Exception(
                f"Pedido do Sisven {pedido_sisven.pedcod} não foi encontrado na PDV01 do Acedata (campo pdvcodpocket).")
        except Exception as e:
            raise Exception(f"Erro ao inserir comissão no Acedata: {e}")

    def apurar_comissao_para_pedido(self, pedido: Ped01):
        """
        Contém a lógica principal para verificar e retornar as informações de comissão.
        """
        # --- CASO A: Pedido possui um registro direto na com_log_ped_rep_cli ---
        log_direto = ComLogPedRepCli.objects.using('sisven').filter(pedido=pedido).select_related(
            'representante_subordinado').first()
        if log_direto and log_direto.representante_subordinado:
            self.stdout.write("  - Verificação: Encontrado log de visita direto para este pedido.")
            rep_subordinado = log_direto.representante_subordinado

            comissao_cliente = ComCliEsp.objects.using('sisven').filter(clicod=pedido.cliente_id).first()
            if comissao_cliente:
                return {'representante_subordinado': rep_subordinado,
                        'percentual': comissao_cliente.percentual_comissao,
                        'origem': f'Configuração Específica do Cliente (ID: {comissao_cliente.clicod})'}

            comissao_rep = ComRepSub.objects.using('sisven').filter(representante=rep_subordinado).first()
            if comissao_rep:
                return {'representante_subordinado': rep_subordinado, 'percentual': comissao_rep.percentual_comissao,
                        'origem': f'Configuração Geral do Representante (ID: {rep_subordinado.id})'}
            return None

            # --- CASO B: Pedido NÃO possui registro direto, verificar comissão residual ---
        self.stdout.write("  - Verificação: Nenhum log de visita direto. Verificando comissão residual...")

        ultimo_log = ComLogPedRepCli.objects.using('sisven').filter(cliente_id=pedido.cliente_id).select_related(
            'representante_subordinado').order_by('-data_pedido').first()

        if not ultimo_log or not ultimo_log.representante_subordinado:
            self.stdout.write("  - Verificação: Nenhum log de visita anterior encontrado para este cliente.")
            return None

        rep_subordinado_residual = ultimo_log.representante_subordinado
        data_ultima_visita = ultimo_log.data_pedido
        data_pedido_atual = pedido.peddat

        if not all([data_pedido_atual, data_ultima_visita]):
            self.stdout.write("  - Verificação: Data do pedido atual ou data da última visita está nula.")
            return None

        dias_desde_visita = (data_pedido_atual - data_ultima_visita).days
        self.stdout.write(
            f"  - Verificação: Última visita registrada em {data_ultima_visita}. Dias desde a visita: {dias_desde_visita}")

        comissao_cliente = ComCliEsp.objects.using('sisven').filter(clicod=pedido.cliente_id).first()
        if comissao_cliente:
            if dias_desde_visita <= comissao_cliente.dias_max_sem_visita:
                return {'representante_subordinado': rep_subordinado_residual,
                        'percentual': comissao_cliente.percentual_comissao,
                        'origem': f'Comissão Residual por Cliente (Dentro do prazo de {comissao_cliente.dias_max_sem_visita} dias)'}
            else:
                self.stdout.write(
                    f"  - Verificação: Prazo de {comissao_cliente.dias_max_sem_visita} dias (cliente) expirou.")

        comissao_rep = ComRepSub.objects.using('sisven').filter(representante=rep_subordinado_residual).first()
        if comissao_rep:
            if dias_desde_visita <= comissao_rep.dias_max_sem_visita:
                return {'representante_subordinado': rep_subordinado_residual,
                        'percentual': comissao_rep.percentual_comissao,
                        'origem': f'Comissão Residual por Representante (Dentro do prazo de {comissao_rep.dias_max_sem_visita} dias)'}
            else:
                self.stdout.write(
                    f"  - Verificação: Prazo de {comissao_rep.dias_max_sem_visita} dias (representante) expirou.")

        return None

