import logging
from django.db import transaction
from datetime import datetime, time
from django.utils import timezone
from django.db.models.functions import Cast
from django.db.models import CharField, Sum
import decimal

# Seus modelos locais, incluindo os novos Cliente e Representante
from .models import (
    Pedido, ItemDemandaProducao, OrdemProducao, OrdemProducaoStatus,
    FormulaQuimica, FormulaPorCamada, ComponenteFormula, RegraKanban,
    Cliente, Representante
)
# Seus modelos espelho do ERP
from .models_erp import (
    Opr01, Ftm01, Ftm02, Pdv02, Pdv01, Pro01, Ftm04, Ftm05, Ftm06,
    Pdv06, Ftd02, Ftc01, Ftc02, Teq01, Emb01, Cid01
)

logger = logging.getLogger(__name__)


@transaction.atomic
def importar_ops_do_erp(op_especifica=None, limit=None, data_inicio=None, tarja=None, cliente_override=None, data_quimica=None):
    """
    Serviço para importar Ordens de Produção do banco de dados do ERP,
    com lógica refatorada para criar/atualizar Clientes e Representantes.
    """
    CODIGO_EMPRESA = '9'
    db_alias = 'acedata'
    ops_erp_query = Opr01.objects.using(db_alias).filter(opraempcod=CODIGO_EMPRESA)

    # --- Filtros para a consulta de OPs no ERP ---
    if op_especifica:
        ops_erp_query = ops_erp_query.filter(opracod=op_especifica)
    else:
        op_codes_com_pdv_str = Pdv02.objects.using(db_alias).filter(
            pdvempcod=CODIGO_EMPRESA
        ).exclude(pdvoprcod='').values_list('pdvoprcod', flat=True).distinct()
        
        numeric_op_codes = [code for code in op_codes_com_pdv_str if str(code).strip().isdigit()]
        ops_erp_query = ops_erp_query.filter(opracod__in=numeric_op_codes)
        
        existing_ops = OrdemProducao.objects.values_list('numero_op', flat=True)
        ops_erp_query = ops_erp_query.exclude(opracod__in=list(existing_ops))

    if data_inicio:
        start_of_day_naive = datetime.combine(data_inicio, time.min)
        start_of_day_utc = timezone.make_aware(start_of_day_naive, timezone.get_default_timezone())
        ops_erp_query = ops_erp_query.filter(opradatemi__gte=start_of_day_utc)

    if limit:
        ops_erp_query = ops_erp_query[:limit]

    # --- Contadores e variáveis de retorno ---
    ops_importadas_count = 0
    ops_com_erro_count = 0
    op_local_retorno = None

    # --- Pré-carregamento de regras de Kanban para otimização ---
    regras_kanban_map = {r.artigo: r for r in RegraKanban.objects.all()}
    logger.info(f"Carregadas {len(regras_kanban_map)} regras de Kanban para a importação.")
    logger.info(f"Iniciando importação de OPs. {len(ops_erp_query)} OPs encontradas para processar.")

    # --- Loop principal de processamento de OPs ---
    for op_erp in ops_erp_query:
        op_local = None 
        try:
            logger.info(f"\n--- Processando OP: {op_erp.opracod} ---")
            
            pedidos_info_qs = Pdv02.objects.using(db_alias).select_related('embalagem').filter(pdvoprcod=op_erp.opracod, pdvempcod=CODIGO_EMPRESA)

            if not pedidos_info_qs.exists():
                logger.warning(f"AVISO para OP {op_erp.opracod}: Nenhuma demanda (item de pedido) encontrada. OP será ignorada.")
                ops_com_erro_count += 1
                continue
            
            # --- Coleta de dados mestre do ERP ---
            total_quantidade_programada = pedidos_info_qs.aggregate(total=Sum('pdvqtdpro'))['total'] or decimal.Decimal('0')
            produto_erp = Pro01.objects.using(db_alias).get(procod=op_erp.opraprocod)
            tamanho_produto = str(produto_erp.probarttam).strip()
            ficha_tecnica = Ftm02.objects.using(db_alias).get(ftmacod=op_erp.opraftmcod, ftmdtam=tamanho_produto)
            material = Ftm01.objects.using(db_alias).get(ftmacod=op_erp.opraftmcod)
            
            # --- Lógica de negócio para definir flags (Kanban e Tingimento) ---
            artigo_op = str(produto_erp.probartcod).strip() if produto_erp.probartcod else None
            artigo_base_op = str(produto_erp.proartcodbas).strip() if produto_erp.proartcodbas else None
            cor_base_op = str(op_erp.opragddcod1).strip()
            material_codigo_op = str(material.ftmamtgcod).strip()
            
            is_kanban_flag = False
            if artigo_base_op in regras_kanban_map:
                is_kanban_flag = False
            elif artigo_op in regras_kanban_map:
                regra = regras_kanban_map[artigo_op]
                if (regra.material_codigo_erp == material_codigo_op and 
                    regra.cor_base_neutra == cor_base_op and
                    tamanho_produto == '18'):
                    is_kanban_flag = True
            
            cores_finais_distintas = {str(p.pdvgddcod1).strip() for p in pedidos_info_qs if p.pdvgddcod1 and str(p.pdvgddcod1).strip()}
            
            requer_tingimento_flag = False
            if len(cores_finais_distintas) > 1:
                requer_tingimento_flag = True
            elif len(cores_finais_distintas) == 1:
                unica_cor_final = cores_finais_distintas.pop()
                if unica_cor_final != cor_base_op:
                    requer_tingimento_flag = True
            
            logger.info(f"INFO para OP {op_erp.opracod}: Verificação de Fluxo: is_kanban={is_kanban_flag}, requer_tingimento={requer_tingimento_flag}")

            # --- Busca de informações adicionais (Equipamento, Observações) ---
            nome_equipamento_erp = None
            if material.ftmateqcod and material.ftmateqemp:
                try:
                    codigo_equipamento = str(material.ftmateqcod).strip()
                    codigo_empresa_equip = str(material.ftmateqemp).strip()
                    equipamento_erp = Teq01.objects.using(db_alias).get(teqcod=codigo_equipamento, mstcod=codigo_empresa_equip)
                    nome_equipamento_erp = str(equipamento_erp.teqnom).strip()
                except Teq01.DoesNotExist:
                    logger.warning(f"AVISO para OP {op_erp.opracod}: Equipamento com código '{material.ftmateqcod}' e empresa '{material.ftmateqemp}' não encontrado.")
            
            obs_ftm04_obj = Ftm04.objects.using(db_alias).annotate(ftmacod_str=Cast('ftmacod', CharField(max_length=50)), ftmeart_str=Cast('ftmeart', CharField(max_length=255))).filter(ftmacod_str=op_erp.opraftmcod, ftmeart_str=produto_erp.prorprcod.strip()).first()
            observacao_ftm04 = str(obs_ftm04_obj.ftmeobs).strip() if obs_ftm04_obj and obs_ftm04_obj.ftmeobs else None
            obs_ftm06_obj = Ftm06.objects.using(db_alias).annotate(ftmacod_str=Cast('ftmacod', CharField(max_length=50))).filter(ftmacod_str=op_erp.opraftmcod).first()
            observacao_ftm06 = str(obs_ftm06_obj.ftmhobs).strip() if obs_ftm06_obj and obs_ftm06_obj.ftmhobs else None
            data_emissao_op = op_erp.opradatemi.date() if op_erp.opradatemi else None
            
            # --- Cálculos baseados nos dados do ERP ---
            rendimento_erp = ficha_tecnica.ftmdren
            placas_calculadas_para_salvar = decimal.Decimal('0')
            if rendimento_erp and rendimento_erp > 0 and total_quantidade_programada > 0:
                placas_calculadas_para_salvar = total_quantidade_programada / rendimento_erp

            # --- Criação ou atualização da Ordem de Produção local ---
            op_local, created = OrdemProducao.objects.update_or_create(
                numero_op=str(op_erp.opracod),
                defaults={
                    'status': OrdemProducaoStatus.PENDENTE_CONFERENCIA,
                    'artigo': artigo_op,
                    'artigo_base': artigo_base_op,
                    'material': str(material.ftmanom).strip(),
                    'tamanho': str(ficha_tecnica.ftmdtam).strip(),
                    'cor': cor_base_op,
                    'is_kanban': is_kanban_flag,
                    'requer_tingimento': requer_tingimento_flag,
                    'numero_agrupamento': str(op_erp.opraagr) if op_erp.opraagr is not None else None,
                    'furacao': str(op_erp.opragddcod2).strip(),
                    'acabamento': str(op_erp.opragddcod3).strip(),
                    'espessura_bruta': ficha_tecnica.ftmdespbru,
                    'espessura_acabada': ficha_tecnica.ftmdespaca,
                    'aproveitamento': ficha_tecnica.ftmdapr,
                    'rendimento': rendimento_erp,
                    'quantidade_programada_total': total_quantidade_programada,
                    'quantidade_placas': placas_calculadas_para_salvar,
                    'unidade': str(op_erp.oprauniest).strip(),
                    'data_emissao': data_emissao_op,
                    'tarja': tarja,
                    'observacao_ficha_tecnica': observacao_ftm04,
                    'observacao_material': observacao_ftm06,
                    'peso_placa': op_erp.oprapesjt,
                    'peso_previsto': op_erp.oprapesprv,
                    'peso_liquido_grosa': produto_erp.propesliq,
                    'nome_equipamento': nome_equipamento_erp,
                    'data_qmc': data_quimica,
                }
            )
            logger.info(f"INFO para OP {op_erp.opracod}: Ordem de Produção local {'criada' if created else 'atualizada'}.")

            # --- Processamento dos itens de demanda (pedidos) ---
            for pedido_info in pedidos_info_qs:
                numero_pedido_erp = str(pedido_info.pdvcod)
                
                # ===== INÍCIO DA REATORAÇÃO PONTUAL =====
                
                if cliente_override:
                    representante_obj, _ = Representante.objects.get_or_create(codigo_representante="AVULSO", defaults={'nome': "Avulso"})
                    cliente_obj, _ = Cliente.objects.get_or_create(codigo_cliente=f"AVULSO-{op_erp.opracod}", defaults={'nome': cliente_override, 'representante': representante_obj})
                    pedido_obj, _ = Pedido.objects.get_or_create(numero_pedido=f"AVULSO-{op_erp.opracod}", defaults={'cliente': cliente_obj})
                else:
                    try:
                        cabecalho_pedido_erp = Pdv01.objects.using(db_alias).select_related('cliente', 'representante').get(pdvcod=numero_pedido_erp, pdvempcod=CODIGO_EMPRESA)
                    except Pdv01.DoesNotExist:
                        logger.error(f"ERRO CRÍTICO para OP {op_erp.opracod}: Cabeçalho do pedido {numero_pedido_erp} não encontrado. Ignorando item.")
                        continue
                    
                    # 1. Cria ou atualiza o Representante
                    representante_obj = None
                    if cabecalho_pedido_erp.representante:
                        codigo_rep_erp = str(cabecalho_pedido_erp.representante.repdoc).strip()
                        nome_rep_erp = str(cabecalho_pedido_erp.representante.repnom).strip()
                        representante_obj, _ = Representante.objects.update_or_create(
                            codigo_representante=codigo_rep_erp,
                            defaults={'nome': nome_rep_erp}
                        )
                    
                    # 2. Cria ou atualiza o Cliente
                    cliente_erp = cabecalho_pedido_erp.cliente
                    if not cliente_erp:
                        logger.error(f"ERRO CRÍTICO para OP {op_erp.opracod}: Cliente não encontrado para o pedido {numero_pedido_erp}.")
                        continue
                        
                    cidade_nome = None
                    if cliente_erp.tercidcodf:
                        try:
                            cidade_erp = Cid01.objects.using(db_alias).get(cidcod=cliente_erp.tercidcodf)
                            cidade_nome = f"{str(cidade_erp.cidnom).strip()} - {str(cidade_erp.estcod).strip()}"
                        except Cid01.DoesNotExist:
                            logger.warning(f"AVISO: Cidade com código '{cliente_erp.tercidcodf}' não encontrada para o cliente '{cliente_erp.ternom}'.")

                    cliente_obj, _ = Cliente.objects.update_or_create(
                        codigo_cliente=str(cliente_erp.terdoc).strip(),
                        defaults={
                            'representante': representante_obj,
                            'nome': str(cliente_erp.ternom).strip(),
                            'razao_social': str(cliente_erp.terraz).strip() if cliente_erp.terraz else None,
                            'cpf_cnpj': str(cliente_erp.tercpf).strip() if cliente_erp.tercpf else None,
                            'cidade': cidade_nome,
                            'cep': str(cliente_erp.tercepfat).strip() if cliente_erp.tercepfat else None,
                            'telefone': str(cliente_erp.terfon1).strip() if cliente_erp.terfon1 else None,
                            'email': str(cliente_erp.terema).strip() if cliente_erp.terema else None,
                        }
                    )
                    
                    # 3. Cria ou atualiza o Pedido
                    observacao_pedido = None
                    try:
                        obs_obj = Pdv06.objects.using(db_alias).get(pdvcod=numero_pedido_erp, pdvempcod=CODIGO_EMPRESA)
                        if obs_obj.pdvobsdet: observacao_pedido = str(obs_obj.pdvobsdet).strip()
                    except Pdv06.DoesNotExist: pass

                    pedido_obj, _ = Pedido.objects.update_or_create(
                        numero_pedido=numero_pedido_erp,
                        defaults={
                            'cliente': cliente_obj,
                            'data_emissao': cabecalho_pedido_erp.pdvemi,
                            'observacao_detalhada': observacao_pedido,
                        }
                    )
                
                # ===== FIM DA REATORAÇÃO PONTUAL =====

                item_do_pedido = str(pedido_info.pdvitmpro).strip() if pedido_info.pdvitmpro else None
                _, item_created = ItemDemandaProducao.objects.update_or_create(
                    ordem_producao=op_local,
                    pedido=pedido_obj,
                    item_pedido_erp=item_do_pedido,
                    defaults={
                        'cor_final': str(pedido_info.pdvgddcod1).strip() if pedido_info.pdvgddcod1 else None,
                        'quantidade': pedido_info.pdvboriproqtd,
                        'quantidade_producao': pedido_info.pdvqtdpro,
                        'preco_venda': pedido_info.pdvprcven,
                        'data_entrega': pedido_info.pdvprvent,
                        'numero_pedido_cliente': pedido_info.pdvpedcli,
                        'unidade': pedido_info.pdvunicod,
                        'embalagem': str(pedido_info.embalagem.embnom).strip() if pedido_info.embalagem else None,
                        'observacao_item_pedido': str(pedido_info.observacao_item).strip() if hasattr(pedido_info, 'observacao_item') and pedido_info.observacao_item else None,
                    }
                )
                logger.info(f"INFO para OP {op_erp.opracod}: Item de demanda do pedido {numero_pedido_erp} {'criado' if item_created else 'atualizado'}.")

            # --- Processamento das Fórmulas Químicas por Camada (Lógica inalterada) ---
            codigo_cor_erp = op_erp.opragddcod1.strip()
            codigo_ftm_erp = op_erp.opraftmcod
            codigo_mtg_erp = material.ftmamtgcod
            if not codigo_cor_erp or not codigo_mtg_erp: raise ValueError("Cor ou Grupo de Material não definidos para esta OP.")
            
            regras_de_peso = list(Ftm05.objects.using(db_alias).filter(ftmacod=codigo_ftm_erp).order_by('ftmbitm'))
            if not regras_de_peso: raise ValueError(f"Nenhuma regra de peso (Porcentagens) encontrada na FTM05 para a ficha {codigo_ftm_erp}.")
            
            numero_camadas_a_processar = len(regras_de_peso)
            try:
                formulas_da_cor = list(Ftd02.objects.using(db_alias).filter(gddcod=codigo_cor_erp, mtgcod=codigo_mtg_erp).order_by('ftditm'))
                if not formulas_da_cor: raise ValueError(f"NENHUMA fórmula encontrada no ERP (tabela Ftd02) para a cor '{codigo_cor_erp}' e grupo de material '{codigo_mtg_erp}'.")
                
                formulas_por_item_map = {f.ftditm: f.ftcacod.strip() for f in formulas_da_cor}
                regras_por_item_map = {r.ftmbitm: r for r in regras_de_peso}
                formula_fallback = formulas_da_cor[0].ftcacod.strip()

                for i in range(1, numero_camadas_a_processar + 1):
                    camada_num = i
                    codigo_formula = formulas_por_item_map.get(camada_num, formula_fallback)
                    regra_peso = regras_por_item_map.get(camada_num)
                    if not regra_peso: raise ValueError(f"Inconsistência de dados: Regra de peso para a camada {camada_num} não encontrada.")
                    if codigo_formula == formula_fallback and i > 1: logger.warning(f"AVISO para OP {op_erp.opracod}: Fórmula para camada {camada_num} não encontrada. Reutilizando a fórmula de fallback ('{formula_fallback}').")
                    
                    formula_obj, created = FormulaQuimica.objects.get_or_create(codigo_formula=codigo_formula,defaults={'nome_formula': f'Fórmula {codigo_formula} (importando...)'})
                    if created:
                        logger.info(f"INFO: Fórmula '{codigo_formula}' não encontrada localmente. Importando do ERP...")
                        try:
                            formula_header_erp = Ftc01.objects.using(db_alias).get(ftcacod=codigo_formula)
                            formula_obj.nome_formula = str(formula_header_erp.ftcanom).strip()
                            formula_obj.save()
                            componentes_erp = Ftc02.objects.using(db_alias).filter(ftcacod=codigo_formula).order_by('ftcbitm')
                            if not componentes_erp.exists(): logger.info(f"AVISO: Fórmula '{codigo_formula}' importada sem componentes, pois não foram encontrados no ERP (Ftc02).")
                            
                            for comp_erp in componentes_erp: 
                                ComponenteFormula.objects.update_or_create(
                                    formula=formula_obj,
                                    componente_codigo=str(comp_erp.ftcprocod).strip(),
                                    defaults={
                                        'item_sequencia': comp_erp.ftcbitm,
                                        'componente_qtd_base': comp_erp.ftcqtd
                                    }
                                )
                            logger.info(f"INFO: Fórmula '{codigo_formula}' e seus {len(componentes_erp)} componentes importados com sucesso.")
                        except Ftc01.DoesNotExist: raise ValueError(f"Cabeçalho da fórmula '{codigo_formula}' não encontrado no ERP (tabela Ftc01).")
                        except Exception as import_error:
                            formula_obj.delete()
                            raise import_error
                    
                    FormulaPorCamada.objects.create(ordem_producao=op_local,formula=formula_obj,camada=camada_num,porcentagem=regra_peso.ftmbpor,quantidade_fixa=(regra_peso.ftmbfix == 'S'))
                
                logger.info(f"INFO: OP {op_erp.opracod}, Fórmulas associadas com sucesso.")

            except Exception as e:
                ops_com_erro_count += 1
                logger.error(f"ERRO CRÍTICO ao processar fórmulas da OP {op_erp.opracod}: {e}")
                if op_local and op_local.pk:
                    logger.info(f"INFO: Revertendo criação da OP {op_erp.opracod} devido ao erro nas fórmulas.")
                    op_local.delete()
                continue

            ops_importadas_count += 1
            if op_especifica:
                op_local_retorno = op_local
            logger.info(f"--- SUCESSO: OP {op_erp.opracod} importada completamente. ---")
        
        except (Pro01.DoesNotExist, Ftm01.DoesNotExist, Ftm02.DoesNotExist) as e:
            ops_com_erro_count += 1
            logger.error(f"ERRO ao processar OP {op_erp.opracod}: Faltam dados mestre no ERP. Detalhes: {e}")
        
        except Exception as e:
            ops_com_erro_count += 1
            logger.error(f"ERRO INESPERADO ao processar a OP {op_erp.opracod}: {e}")
            if op_local and op_local.pk:
                op_local.delete()

    logger.info(f"\n--- Fim da importação ---")
    logger.info(f"Total de OPs importadas com sucesso: {ops_importadas_count}")
    logger.info(f"Total de OPs com erro/ignoradas: {ops_com_erro_count}")

    if op_especifica:
        return (op_local_retorno, ops_com_erro_count)
    else:
        return (ops_importadas_count, ops_com_erro_count)