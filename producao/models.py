from django.db import models
from cadastros.models import Maquina, Operador
import decimal
import math
from django.db.models import Sum
from django.conf import settings

# Choices para uso nos modelos
class Setor(models.TextChoices):
    QUIMICA = 'QUIMICA', 'Química'
    PASTILHA = 'PASTILHA', 'Controle de Pastilha'
    TORNOS = 'TORNOS', 'Tornos'
    LASER = 'LASER', 'Laser'
    LASER_2 = 'LASER_2', 'Laser 2'
    POLIMENTO = 'POLIMENTO', 'Polimento'
    TINGIMENTO = 'TINGIMENTO', 'Tingimento'
    ESCOLHA_FINAL = 'ESCOLHA_FINAL', 'Escolha Final'
    CONTAGEM = 'CONTAGEM', 'Contagem'
    ESTEIRA = 'ESTEIRA', 'Esteira'
    KANBAN = 'KANBAN', 'Kanban'
    FINALIZADO = 'FINALIZADO', 'Finalizado'
    REPROGRAMADO = 'REPROGRAMADO', 'Reprogramado'

class OrdemProducaoStatus(models.TextChoices):
    PENDENTE_CONFERENCIA = 'PENDENTE_CONFERENCIA', 'Pendente de Conferência PCP'
    PENDENTE = 'PENDENTE', 'Pendente'
    EM_PRODUCAO = 'EM_PRODUCAO', 'Em Produção'
    AGUARDANDO_CORTE = 'AGUARDANDO_CORTE', 'Aguardando Corte'
    PARCIALMENTE_FINALIZADO = 'PARCIALMENTE_FINALIZADO', 'Parcialmente Finalizado'
    PAUSADO = 'PAUSADO', 'Pausado'
    FINALIZADO = 'FINALIZADO', 'Finalizado'
    CANCELADO = 'CANCELADO', 'Cancelado'
    REPROGRAMADO = 'REPROGRAMADO', 'Reprogramado'
    AGUARDANDO_PASTILHA = 'AGUARDANDO_PASTILHA', 'Aguardando Pastilha'

class ItemDemandaStatus(models.TextChoices):
    AGUARDANDO_PRODUCAO = 'AGUARDANDO_PRODUCAO', 'Aguardando Produção'
    AGUARDANDO_TINGIMENTO = 'AGUARDANDO_TINGIMENTO', 'Aguardando Tingimento'
    AGUARDANDO_CONTROLE_QUALIDADE = 'AGUARDANDO_CONTROLE_QUALIDADE', 'Aguardando Controle de Qualidade'
    EM_TINGIMENTO = 'EM_TINGIMENTO', 'Em Tingimento'
    FINALIZADO = 'FINALIZADO', 'Finalizado'
    CANCELADO = 'CANCELADO', 'Cancelado'


class MotivoParada(models.Model):
    codigo = models.IntegerField(primary_key=True)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

class MotivoReprogramacao(models.Model):
    descricao = models.CharField(max_length=255)
    setor_responsavel = models.CharField(max_length=50, choices=Setor.choices)

    def __str__(self):
        return self.descricao


# --- Modelos para Fórmulas Químicas ---
class FormulaQuimica(models.Model):
    codigo_formula = models.CharField(max_length=50, unique=True, db_index=True, help_text="Código da Fórmula (FTC01.FtcACod)")
    nome_formula = models.CharField(max_length=255, help_text="Nome descritivo da fórmula (FTC01.FtcANom)")

    class Meta:
        verbose_name = "Fórmula Química"
        verbose_name_plural = "Fórmulas Químicas"

    def __str__(self):
        return f"{self.codigo_formula} - {self.nome_formula}"

class ComponenteFormula(models.Model):
    formula = models.ForeignKey(FormulaQuimica, on_delete=models.CASCADE, related_name="componentes")
    item_sequencia = models.PositiveIntegerField(null=True, help_text="Sequência do item na receita do ERP")
    componente_codigo = models.CharField(max_length=50, db_index=True, help_text="Código da matéria-prima (FTC02.FtcProCod)")
    componente_qtd_base = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        help_text="Quantidade do componente para a receita base (FTC02.FtcQtd)"
    )
    
    class Meta:
        verbose_name = "Componente de Fórmula"
        verbose_name_plural = "Componentes de Fórmulas"
        unique_together = ('formula', 'componente_codigo')
        ordering = ['item_sequencia']

    def __str__(self):
        return f"Componente {self.componente_codigo} na fórmula {self.formula.codigo_formula}"

class FormulaPorCamada(models.Model):
    ordem_producao = models.ForeignKey('OrdemProducao', on_delete=models.CASCADE, related_name='formulas_por_camada')
    formula = models.ForeignKey(FormulaQuimica, on_delete=models.PROTECT)
    camada = models.PositiveIntegerField(help_text="Número da camada (FTD02.FdtItm)")
    porcentagem = models.DecimalField(max_digits=10, decimal_places=4, help_text="Porcentagem ou Peso Fixo da camada (FTM05.FtmBPor)")
    quantidade_fixa = models.BooleanField(default=False, help_text="Peso fixo em vez de percentual? (FTM05.FtmBFix = 'S')")

    class Meta:
        verbose_name = "Fórmula por Camada"
        verbose_name_plural = "Fórmulas por Camada"
        unique_together = ('ordem_producao', 'camada')
        ordering = ['camada']

    def __str__(self):
        tipo = "fixa" if self.quantidade_fixa else "percentual"
        return f"OP {self.ordem_producao.numero_op}: Fórmula {self.formula.codigo_formula} (Camada {self.camada}, {tipo})"

# --- Modelo Central: A Ordem de Produção (Refatorado) ---
class OrdemProducao(models.Model):
    TARJA_CHOICES = (
        ('AZUL', 'Azul'), ('AMARELO', 'Amarelo'), ('VERMELHO', 'Vermelho'),
        ('PRETO', 'Preto'), ('VERDE', 'Verde'), ('ROSA', 'Rosa'),
    )
    numero_op = models.CharField(max_length=50, unique=True, help_text="Código da OP (opracod)")
    numero_agrupamento = models.CharField(max_length=50, blank=True, null=True, help_text="Código de Agrupamento da OP (OprAAgr)") 
    artigo = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    tamanho = models.CharField(max_length=50)
    cor = models.CharField(max_length=100, help_text="Cor base da matéria-prima (OPR01.opragddcod1)")
    furacao = models.CharField(max_length=100)
    acabamento = models.CharField(max_length=100)
    espessura_bruta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    aproveitamento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Percentual de Aproveitamento (FtmDApr)")
    rendimento = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True, help_text="Rendimento em grosas por placa (FtmDRen)")
    espessura_acabada = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantidade_programada_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Soma das quantidades de todas as demandas do lote.")
    unidade = models.CharField(max_length=10)
    data_emissao = models.DateField()
    peso_placa = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True, help_text="Peso da Placa para base da receita (OPRAPESCJT)")
    quantidade_placas = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True, help_text="Quantidade de Camadas")
    peso_previsto = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True, help_text="Peso Previsto TOTAL da OP (OPRAPESPRV)")
    peso_liquido_grosa = models.DecimalField(
        max_digits=19, 
        decimal_places=6, 
        null=True, blank=True,
        help_text="Peso líquido de 1 grosa do produto (do ERP: PRO01.ProPesLiq)"
    )
    peso_bruto_grosa = models.DecimalField(
        max_digits=19, 
        decimal_places=6, 
        null=True, blank=True,
        help_text="Campo preparado para receber peso do apontamento da Pastilhas para fazermos termos um padrão do peso bruto da pastilha"
    )
    tarja = models.CharField(max_length=20, choices=TARJA_CHOICES, blank=True, null=True, help_text="Tarja de prioridade da programação")
    nome_equipamento = models.CharField(max_length=255, blank=True, null=True, help_text="Nome do equipamento (TEQ01.TeqNom)")
    observacao_ficha_tecnica = models.TextField(blank=True, null=True)
    observacao_material = models.TextField(blank=True, null=True)
    observacao_pedido_venda = models.TextField(blank=True, null=True)
    observacao_op = models.TextField(blank=True, null=True)
    
    status = models.CharField(
        max_length=50, choices=OrdemProducaoStatus.choices, default=OrdemProducaoStatus.PENDENTE_CONFERENCIA
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    sequencia_pcp = models.IntegerField(null=True, blank=True, db_index=True, help_text="Ordem da sequência de produção importada da planilha do PCP (mantém a primeira ocorrência)")
    artigo_base = models.CharField(max_length=100, null=True, blank=True, db_index=True, help_text="Código do artigo base (ProBArtCodBas) para conciliação")
    data_qmc = models.DateField(null=True, blank=True, db_index=True, help_text="Data de produção da Química importada da planilha do PCP (mantém a primeira ocorrência)")
    is_kanban = models.BooleanField(default=False, db_index=True, help_text="Indica se a OP segue o fluxo contínuo Kanban")
    requer_tingimento = models.BooleanField(default=False, help_text="Indica se o produto (Kanban ou não) passará pelo processo de tingimento")

    @property
    def quantidade_total_alvo_com_retrabalho(self):
        """
        Calcula a quantidade total alvo em grosas, somando a quantidade original
        com todas as quantidades de reprogramações (retrabalhos).
        Esta propriedade deve ser usada como a meta final de produção.
        """
        total_alvo = self.quantidade_programada_total or decimal.Decimal('0.0')
        
        # Soma as grosas de todas as reprogramações associadas
        if self.reprogramacoes.exists():
            # A OP precisa ter um peso de grosa bruto definido para o cálculo ser possível
            if self.peso_bruto_grosa and self.peso_bruto_grosa > 0:
                peso_bruto_grosa_kg = self.peso_bruto_grosa / 1000
                
                total_peso_reprogramado = self.reprogramacoes.aggregate(
                    total=Sum('peso_reprogramado')
                )['total'] or decimal.Decimal('0.0')
                
                if total_peso_reprogramado > 0:
                    grosas_de_retrabalho = total_peso_reprogramado / peso_bruto_grosa_kg
                    total_alvo += grosas_de_retrabalho

        return total_alvo

    def get_info_retrabalho(self):
        """
        Verifica se a OP tem um retrabalho pendente e calcula os dados necessários.
        Retorna um dicionário com as informações ou None.
        """
        # Busca a última reprogramação para esta OP que ainda está pendente
        retrabalho_pendente = self.reprogramacoes.filter(
            ordem_producao__status=OrdemProducaoStatus.PENDENTE
        ).order_by('-data_reprogramacao').first()

        if not retrabalho_pendente or not retrabalho_pendente.peso_reprogramado:
            return None

        # Calcula as grôsas do retrabalho
        grosas_retrabalho = decimal.Decimal('0.0')
        if self.peso_bruto_grosa and self.peso_bruto_grosa > 0:
            peso_bruto_grosa_kg = self.peso_bruto_grosa / 1000
            grosas_retrabalho = retrabalho_pendente.peso_reprogramado / peso_bruto_grosa_kg
        
        # Calcula a borracha adicional para o retrabalho
        borracha_cm = None
        if self.rendimento and self.rendimento > 0 and grosas_retrabalho > 0:
            placas_retrabalho = grosas_retrabalho / self.rendimento
            fracao_placa, _ = math.modf(placas_retrabalho)
            if fracao_placa > 0:
                TAMANHO_PLACA_CM = decimal.Decimal('57.0')
                cm = decimal.Decimal(fracao_placa) * TAMANHO_PLACA_CM
                borracha_cm = int(cm.to_integral_value(rounding=decimal.ROUND_HALF_UP))

        return {
            'grosas': grosas_retrabalho,
            'borracha_cm': borracha_cm,
            'motivo': retrabalho_pendente.motivo.descricao,
        }

    def get_cores_finais_display(self):
        """ Concatena as cores finais distintas das demandas associadas. """
        cores = self.demandas.values_list('cor_final', flat=True).distinct()
        return ', '.join(filter(None, cores)) or "-"

    @property
    def quantidade_grosas_produzida(self):
        total_produzido = self.contribuicoes_op.aggregate(
            total=Sum('quantidade_grosas_produzida')
        )['total']
        return total_produzido or decimal.Decimal('0.0')

    @property
    def quantidade_alvo_producao(self):
        """
        Determina a quantidade alvo para a produção atual.
        Para OPs Kanban, é a soma das solicitações atendidas pela Química.
        Para OPs normais, é a quantidade total programada.
        """
        if self.is_kanban:
            # A quantidade a ser produzida é a soma de tudo que a Química já atendeu
            total_solicitado = self.solicitacoes_quimica_kanban.filter(
                status='ATENDIDA'
            ).aggregate(
                total=Sum('quantidade_solicitada')
            )['total']
            return total_solicitado or decimal.Decimal('0.0')
        return self.quantidade_programada_total

    @property
    def quantidade_placas_calculada(self):
        # --- CORREÇÃO ---
        # Usa a nova propriedade para determinar a quantidade base
        quantidade_prog = self.quantidade_alvo_producao
        rendimento_placa = self.rendimento
        if quantidade_prog is not None and rendimento_placa and rendimento_placa > 0:
            return quantidade_prog / rendimento_placa
        return None
    
    @property
    def _cm_borracha_nao_arredondado(self):
        placas_necessarias = self.quantidade_placas_calculada
        if not placas_necessarias:
            return None
        
        fracao_placa, _ = math.modf(placas_necessarias)
        if fracao_placa == 0:
            return None

        TAMANHO_PLACA_CM = decimal.Decimal('57.0')
        return decimal.Decimal(fracao_placa) * TAMANHO_PLACA_CM

    @property
    def etiqueta_borracha(self):
        placas_necessarias = self.quantidade_placas_calculada
        if not placas_necessarias or placas_necessarias % 1 == 0:
            return None
        
        if placas_necessarias < 1:
            return "Borracha"
        else:
            return "Borracha Adicional"

    @property
    def valor_borracha_adicional(self):
        cm_borracha = self._cm_borracha_nao_arredondado
        if cm_borracha is None:
            return None
        
        return int(cm_borracha.to_integral_value(rounding=decimal.ROUND_HALF_UP))

    @property
    def peso_bruto_para_receita(self):
        # Este método agora depende de 'quantidade_placas_calculada', que já está corrigido
        numero_de_placas = self.quantidade_placas_calculada
        peso_unitario_placa = self.peso_placa

        if numero_de_placas and peso_unitario_placa and numero_de_placas > 0 and peso_unitario_placa > 0:
            return numero_de_placas * peso_unitario_placa
        
        return self.peso_previsto or decimal.Decimal('0')

    @property
    def peso_liquido_calculado(self):
        peso_bruto = self.peso_bruto_para_receita
        if peso_bruto and self.aproveitamento and self.aproveitamento > 0:
            return peso_bruto * (self.aproveitamento / 100)
        return None

    def get_numeros_pedido_display(self):
        pedidos = self.demandas.values_list('pedido__numero_pedido', flat=True).distinct()
        return ', '.join(filter(None, pedidos)) or "-"

    def get_clientes_display(self):
        clientes = self.demandas.values_list('pedido__cliente_nome', flat=True).distinct()
        return ', '.join(filter(None, clientes)) or "-"

    def get_tarja_css_color(self):
        cores = {
            'AZUL': '#cce5ff', 'AMARELO': '#fff3cd', 'VERMELHO': '#f8d7da',
            'PRETO': '#d6d8d9', 'VERDE': '#d4edda', 'ROSA': '#f8d7f8',
        }
        return cores.get(self.tarja, '')

    def get_tarja_font_color(self):
        cores = {
            'AZUL': '#004085', 'AMARELO': '#856404', 'VERMELHO': '#721c24',
            'PRETO': '#1b1e21', 'VERDE': '#155724', 'ROSA': '#721c72',
        }
        return cores.get(self.tarja, '#000000')

    def get_receita_calculada(self, quantidade_alvo_grosas=None):
        """
        Calcula a receita. Se 'quantidade_alvo_grosas' for fornecida (caso do Kanban),
        usa essa quantidade como base. Caso contrário, usa a quantidade total da OP.
        """
        receitas_finais = {}
        
        # Determina o número de placas com base na quantidade alvo ou no total da OP
        if quantidade_alvo_grosas is not None and self.rendimento and self.rendimento > 0:
            numero_de_placas = decimal.Decimal(quantidade_alvo_grosas) / self.rendimento
        else:
            # --- CORREÇÃO ---
            # Usa a propriedade que já contém a lógica correta
            numero_de_placas = self.quantidade_placas_calculada

        peso_total_de_uma_placa = self.peso_placa

        if not all([self.formulas_por_camada.exists(), numero_de_placas, peso_total_de_uma_placa]):
            return {}

        soma_kg_aditivos_por_placa = self.formulas_por_camada.filter(quantidade_fixa=True).aggregate(
            soma=Sum('porcentagem')
        )['soma'] or decimal.Decimal('0')
        
        base_para_percentual = peso_total_de_uma_placa - soma_kg_aditivos_por_placa
        
        for formula_por_camada in self.formulas_por_camada.all():
            camada_key = f"camada_{formula_por_camada.camada}"
            formula = formula_por_camada.formula
            receita_camada = []
            peso_alvo_camada = decimal.Decimal('0')

            if formula_por_camada.quantidade_fixa:
                kg_por_placa = formula_por_camada.porcentagem or decimal.Decimal('0')
                peso_alvo_camada = numero_de_placas * kg_por_placa
            else:
                porcentagem_da_camada = formula_por_camada.porcentagem or decimal.Decimal('0')
                peso_camada_uma_placa = base_para_percentual * (porcentagem_da_camada / 100)
                peso_alvo_camada = peso_camada_uma_placa * numero_de_placas

            soma_componentes_base_g = formula.componentes.aggregate(soma_total=Sum('componente_qtd_base'))['soma_total'] or 0
            if soma_componentes_base_g > 0:
                for componente in formula.componentes.order_by('item_sequencia'):
                    gramas_base = componente.componente_qtd_base
                    proporcao = gramas_base / soma_componentes_base_g
                    quantidade_necessaria_kg = proporcao * peso_alvo_camada
                    quantidade_necessaria_g = quantidade_necessaria_kg * 1000

                    receita_camada.append({
                        'item_sequencia': componente.item_sequencia,
                        'codigo_componente': componente.componente_codigo,
                        # NOTA: O nome do componente precisa ser buscado a partir de um modelo de Matéria-Prima.
                        # Este é um placeholder para que o template não quebre.
                        'nome_componente': 'NOME DA MATÉRIA-PRIMA',
                        'qtd_por_kg': round(gramas_base, 3),
                        'quantidade_necessaria': round(quantidade_necessaria_g, 3)
                    })

            receitas_finais[camada_key] = {
                'peso_alvo': round(peso_alvo_camada, 4),
                'formula': formula,
                'receita': receita_camada,
            }
        return receitas_finais

class Representante(models.Model):
    """
    Representa um representante comercial, centralizando suas informações.
    """
    codigo_representante = models.CharField(max_length=50, unique=True, db_index=True)
    nome = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Representante"
        verbose_name_plural = "Representantes"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    """
    Representa um cliente, centralizando a informação que antes estava no Pedido.
    """
    representante = models.ForeignKey(
        Representante,
        on_delete=models.PROTECT,
        related_name="clientes",
        null=True, blank=True
    )
    codigo_cliente = models.CharField(max_length=50, unique=True, db_index=True)
    nome = models.CharField(max_length=255, verbose_name="Nome Fantasia")
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    cpf_cnpj = models.CharField(max_length=20, blank=True, null=True, verbose_name="CPF/CNPJ")
    cidade = models.CharField(max_length=100, null=True, blank=True)
    cep = models.CharField(max_length=10, blank=True, null=True, verbose_name="CEP")
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

    def __str__(self):
        return f"{self.codigo_cliente} - {self.nome}"

# --- MODELO REFATORADO ---
class Pedido(models.Model):
    """
    O modelo Pedido foi refatorado para se conectar ao novo modelo Cliente.
    Os campos de cliente e representante foram removidos para evitar duplicidade de dados.
    """
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.PROTECT, 
        related_name="pedidos",
        null=True, 
        blank=True,
    )
    numero_pedido = models.CharField(max_length=50, unique=True, db_index=True)
    data_emissao = models.DateField(null=True, blank=True)
    observacao_detalhada = models.TextField(blank=True, null=True, verbose_name="Observação Detalhada do Pedido")

    class Meta:
        verbose_name = "Pedido de Venda"
        verbose_name_plural = "Pedidos de Venda"
        ordering = ['-data_emissao', '-numero_pedido']

    def __str__(self):
        return f"{self.numero_pedido} - {self.cliente.nome}"


class ItemDemandaProducao(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens", null=True)
    ordem_producao = models.ForeignKey(
        OrdemProducao, 
        on_delete=models.CASCADE, 
        related_name="demandas",
        verbose_name="Lote de Fabricação (OP)"
    )
    numero_pedido_cliente = models.CharField(max_length=50, null=True, blank=True, help_text="Número do pedido do cliente (Ex: 006/25)")
    cor_final = models.CharField(max_length=100, help_text="Cor final do tingimento (PDV02.pdvgddcod1)")
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantidade desta demanda específica (PDV02.pdvboriproqtd)")
    preco_venda = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True, help_text="Preço de Venda do item no Pedido (PDV02.PdvPrcVen)")
    unidade = models.CharField(max_length=10, null=True, blank=True)
    embalagem = models.CharField(max_length=50, null=True, blank=True)
    observacao_item_pedido = models.TextField(blank=True, null=True, verbose_name="Observação (Item do Pedido)")
    data_entrega = models.DateField(null=True, blank=True, help_text="Data de Entrega Prevista (PDV02.pdvprvent)")
    quantidade_producao = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text="Quantidade de Produção para cálculo financeiro (PDV02.pdvqtdpro)"
    )
    item_programacao = models.ForeignKey(
        'ibgcontrole.ItemProgramacao',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="demandas_vinculadas",
        help_text="Vínculo com o item da planilha de programação do PCP. Múltiplas demandas podem se vincular a um item."
    )
    status_item = models.CharField(
        max_length=50,
        choices=ItemDemandaStatus.choices,
        default=ItemDemandaStatus.AGUARDANDO_PRODUCAO,
        verbose_name="Status da Demanda"
    )
    item_pedido_erp = models.CharField(max_length=10, help_text="Número do item original do pedido no ERP (PDV02.pdvitmpro)", null=True, blank=True)
    observacao_pcp = models.TextField(
        blank=True, null=True, 
        verbose_name="Observação do PCP"
    )
    conferido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        verbose_name="Conferido por"
    )
    conferido_em = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Conferido em"
    )

    @property
    def valor_total_item(self):
        if self.quantidade_producao is not None and self.preco_venda is not None:
            return self.quantidade_producao * self.preco_venda
        return 0

    class Meta:
        verbose_name = "Item de Demanda de Produção"
        verbose_name_plural = "Itens de Demanda de Produção"
        unique_together = ('ordem_producao', 'pedido', 'cor_final', 'item_pedido_erp')
        ordering = ['ordem_producao', 'pedido']

# --- Modelos de Apontamento para cada Setor ---
class BaseApontamento(models.Model):
    responsavel = models.ForeignKey(Operador, on_delete=models.PROTECT, null=True, blank=True)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField(null=True, blank=True)
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class BaseApontamentoIndividualOP(BaseApontamento):
    ordem_producao = models.ForeignKey(
        'OrdemProducao', 
        on_delete=models.CASCADE, 
        related_name="%(class)s_apontamentos"
    )

    class Meta:
        abstract = True


class BaseApontamentoAgrupadoOP(BaseApontamento):
    ordens_producao_agrupadas = models.ManyToManyField(
        'OrdemProducao', 
        related_name="%(class)s_apontamentos"
    )

    class Meta:
        abstract = True


# Modelos para controle da Química
class LoteQuimico(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        PRODUZIDO = 'PRODUZIDO', 'Produzido'

    formula = models.ForeignKey('FormulaQuimica', on_delete=models.PROTECT, related_name="lotes_produzidos")
    data_programacao = models.DateField(db_index=True, help_text="Data da programação para agrupar as OPs")
    quantidade_total_necessaria = models.DecimalField(max_digits=19, decimal_places=4)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    data_producao = models.DateTimeField(null=True, blank=True, help_text="Data/hora em que foi marcado como produzido")
    
    ordens_producao = models.ManyToManyField('OrdemProducao', related_name="lotes_quimicos_associados")

    class Meta:
        verbose_name = "Lote Químico"
        verbose_name_plural = "Lotes Químicos"
        unique_together = ('formula', 'data_programacao')

    def __str__(self):
        return f"Lote de {self.formula.nome_formula} para {self.data_programacao.strftime('%Y-%m-%d')}"

# --- NOVOS MODELOS PARA APONTAMENTO DA PRODUÇÃO DE PLACAS (QUÍMICA) ---

class RendimentoGrosaPorTamanho(models.Model):
    """
    Tabela de referência que armazena o rendimento padrão (em grosas)
    de uma placa inteira para um determinado tamanho de botão/produto.
    """
    tamanho = models.PositiveIntegerField(unique=True, help_text="Tamanho do produto (ex: 14, 16, 18).")
    rendimento_grosas_por_placa = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Quantidade de grosas que uma placa inteira rende para este tamanho."
    )

    class Meta:
        verbose_name = "Rendimento de Grosa por Tamanho"
        verbose_name_plural = "Rendimentos de Grosas por Tamanho"
        ordering = ['tamanho']

    def __str__(self):
        return f"Tamanho {self.tamanho}: {self.rendimento_grosas_por_placa} grosas/placa"


class AgrupamentoLancamento(models.Model):
    """
    Representa o AGRUPAMENTO de uma ou mais OPs que serão produzidas juntas.
    Este é o objeto "pai" que une múltiplos lançamentos no cilindro.
    """
    ordens_producao = models.ManyToManyField(OrdemProducao, related_name="agrupamentos")
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Agrupamento para Lançamento"
        verbose_name_plural = "Agrupamentos para Lançamento"
        ordering = ['-data_criacao']

    def __str__(self):
        op_count = self.ordens_producao.count()
        return f"Agrupamento {self.id} com {op_count} OP(s) criado em {self.data_criacao.strftime('%d/%m/%Y')}"


class LancamentoCilindro(models.Model):
    """
    Registra um ÚNICO evento de produção no cilindro (um lançamento).
    Vários lançamentos podem pertencer ao mesmo Agrupamento.
    """
    agrupamento = models.ForeignKey(
        AgrupamentoLancamento, 
        on_delete=models.CASCADE, 
        related_name="lancamentos",
        null=True, blank=True # Permite que este campo seja nulo
    )
    solicitacao_reposicao = models.ForeignKey(
        'SolicitacaoReposicaoKanban',
        on_delete=models.CASCADE,
        related_name="lancamentos_cilindro",
        null=True, blank=True,
        help_text="Vínculo com a solicitação de reposição Kanban, se aplicável."
    )
    operador = models.ForeignKey(Operador, on_delete=models.PROTECT)
    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT, verbose_name="Cilindro")
    
    quantidade_placas_total = models.DecimalField(
        max_digits=10, decimal_places=4,
        help_text="Soma total de placas produzidas NESTE lançamento."
    )
    quantidade_grosas_total = models.DecimalField(
        max_digits=10, decimal_places=4, default=0,
        help_text="Soma total de grosas produzidas NESTE lançamento. Calculado automaticamente."
    )

    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField(null=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Lançamento no Cilindro"
        verbose_name_plural = "Lançamentos no Cilindro"
        ordering = ['-data_hora_inicio']

    def __str__(self):
        """
        Retorna uma representação em string do lançamento, adaptando-se
        se for para um agrupamento de OPs ou para uma solicitação Kanban.
        """
        if self.agrupamento:
            return f"Lançamento {self.id} (Agrup. {self.agrupamento.id}) no Cilindro {self.maquina.nome_maq_erp}"
        elif self.solicitacao_reposicao:
            return f"Lançamento {self.id} (Kanban: {self.solicitacao_reposicao.item_estoque}) no Cilindro {self.maquina.nome_maq_erp}"
        else:
            return f"Lançamento {self.id} no Cilindro {self.maquina.nome_maq_erp} (sem vínculo)"
    
    def atualizar_total_grosas(self):
        """Soma as grosas de todas as contribuições deste lançamento e atualiza o total."""
        total = self.contribuicoes_op.aggregate(
            total_grosas=Sum('quantidade_grosas_produzida')
        )['total_grosas'] or decimal.Decimal('0.0')
        self.quantidade_grosas_total = total
        self.save(update_fields=['quantidade_grosas_total'])


class ContribuicaoOP(models.Model):
    """
    Tabela 'through' que conecta um LançamentoCilindro a uma OrdemProducao,
    especificando a quantidade de placas que a OP contribuiu naquele lançamento.
    """
    lancamento = models.ForeignKey(LancamentoCilindro, on_delete=models.CASCADE, related_name="contribuicoes_op")
    ordem_producao = models.ForeignKey(OrdemProducao, on_delete=models.PROTECT, related_name="contribuicoes_op")
    
    quantidade_placas_contribuida = models.DecimalField(
        max_digits=10, decimal_places=4,
        help_text="Quantidade de placas que esta OP específica contribuiu neste lançamento."
    )
    quantidade_grosas_produzida = models.DecimalField(
        max_digits=10, decimal_places=4, default=0, editable=False,
        help_text="Quantidade de grosas calculada para esta contribuição."
    )

    class Meta:
        unique_together = ('lancamento', 'ordem_producao')
        verbose_name = "Contribuição de OP no Lançamento"
        verbose_name_plural = "Contribuições de OPs nos Lançamentos"

    def __str__(self):
        return f"{self.quantidade_placas_contribuida} placas da OP {self.ordem_producao.numero_op} no Lançamento {self.lancamento.id}"

    def save(self, *args, **kwargs):
        try:
            tamanho_op = int(self.ordem_producao.tamanho) 
            rendimento_info = RendimentoGrosaPorTamanho.objects.get(tamanho=tamanho_op)
            rendimento_por_placa = rendimento_info.rendimento_grosas_por_placa
            
            self.quantidade_grosas_produzida = self.quantidade_placas_contribuida * rendimento_por_placa
        except (RendimentoGrosaPorTamanho.DoesNotExist, AttributeError, ValueError):
            self.quantidade_grosas_produzida = decimal.Decimal('0.0')
        super().save(*args, **kwargs)


class ParadaLancamentoAgrupado(models.Model):
    """
    Registra uma parada que ocorreu durante um Lançamento no Cilindro.
    """
    lancamento = models.ForeignKey(
        LancamentoCilindro,
        on_delete=models.CASCADE,
        related_name="paradas",
        null=True
    )
    motivo = models.ForeignKey(MotivoParada, on_delete=models.PROTECT)
    duracao_minutos = models.PositiveIntegerField()

    def __str__(self):
        return f"Parada de {self.duracao_minutos} min no Lançamento {self.lancamento.id}"


# Medelos para o Apontamento dos setores a seguir

class ControlePastilha(BaseApontamentoIndividualOP):
    class Tipo(models.TextChoices):
        NORMAL = 'NORMAL', 'Normal'
        FINA = 'FINA', 'Mais Fina'
        GROSSA = 'GROSSA', 'Mais Grossa'
        REAPROVEITADA = 'REAPROVEITADA', 'Reaproveitada'
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    peso = models.DecimalField(max_digits=10, decimal_places=3)
    quantidade_grosas = models.DecimalField(max_digits=10, decimal_places=2)

class ControleProducaoTornoLaser(BaseApontamentoIndividualOP):
    class Estado(models.TextChoices):
        OP_1 = 'OP_1', '1ª Operação'
        OP_2 = 'OP_2', '2ª Operação'
        RETRABALHO = 'RETRABALHO', 'Retrabalho'
        AMOSTRA = 'AMOSTRA', 'Amostra'
        ACABADO = 'ACABADO', 'Acabado'
    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=Estado.choices)
    botoes_por_minuto = models.IntegerField(null=True, blank=True)
    producao_peso = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    quebra_peso = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    check_espessura_cabecote1 = models.CharField(max_length=50, blank=True)
    check_espessura_cabecote2 = models.CharField(max_length=50, blank=True)
    check_broca = models.CharField(max_length=50, blank=True)
    check_abertura = models.CharField(max_length=50, blank=True)
    check_carregador = models.BooleanField(default=False)
    check_botao = models.BooleanField(default=False)
    check_troca = models.BooleanField(default=False)
    producao_grosas = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Produção em Grôsas, calculada a partir do peso."
    )

class Parada(models.Model):
    apontamento_producao = models.ForeignKey(ControleProducaoTornoLaser, on_delete=models.CASCADE, related_name="paradas")
    motivo = models.ForeignKey(MotivoParada, on_delete=models.PROTECT)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField(null=True, blank=True)

class Afiacao(models.Model):
    class Tipo(models.TextChoices):
        FERRAMENTA = 'FERRAMENTA', 'Afiação de Ferramenta'
        BROCA = 'BROCA', 'Afiação de Broca'
    apontamento_producao = models.ForeignKey(ControleProducaoTornoLaser, on_delete=models.CASCADE, related_name="afiacoes")
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField(null=True, blank=True)

class ControlePolimento(BaseApontamento):
    """
    Modelo refatorado para o apontamento de Polimento.
    Agora se relaciona com Itens de Demanda através de um modelo 'through'.
    """
    itens_demanda_agrupados = models.ManyToManyField(
        ItemDemandaProducao,
        through='ItemPolimento',
        related_name="apontamentos_polimento_agrupados"
    )
    tambor = models.ForeignKey(
        Maquina, 
        on_delete=models.PROTECT, 
        limit_choices_to={'setor__nome': 'POLIMENTO'},
        null=True, 
        blank=True
    )

    @property
    def peso_total_carregado(self):
        """Calcula o peso total carregado no tambor somando os pesos dos itens."""
        if self.pk:
            total = self.itens_no_tambor.aggregate(
                total=Sum('peso_carregado')
            )['total']
            return total or decimal.Decimal('0.0')
        return decimal.Decimal('0.0')

    def __str__(self):
        return f"Apontamento de Polimento #{self.id}"


class ItemPolimento(models.Model):
    """
    Modelo 'through' que conecta um apontamento de Polimento a um Item de Demanda,
    registrando o peso específico daquele item que foi carregado no tambor.
    """
    apontamento = models.ForeignKey(ControlePolimento, on_delete=models.CASCADE, related_name="itens_no_tambor")
    item_demanda = models.ForeignKey(ItemDemandaProducao, on_delete=models.PROTECT, related_name="apontamentos_polimento")
    peso_carregado = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        help_text="Peso (Kg) deste item específico."
    )

    class Meta:
        unique_together = ('apontamento', 'item_demanda')

    def __str__(self):
        return f"{self.peso_carregado}Kg do item {self.item_demanda.id} no Apontamento {self.apontamento.id}"

class LoteTingimento(models.Model):
    class Status(models.TextChoices):
        EM_ANDAMENTO = 'EM_ANDAMENTO', 'Em Andamento'
        FINALIZADO = 'FINALIZADO', 'Finalizado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    itens_demanda = models.ManyToManyField(
        ItemDemandaProducao,
        through='ItemTingimento',
        related_name="lotes_de_tingimento"
    )
    cor_final_alvo = models.CharField(max_length=100, help_text="A cor final que este lote de tingimento deve atingir.")
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.EM_ANDAMENTO)
    observacao_final = models.TextField(blank=True, null=True, help_text="Observações gerais ao finalizar o lote.")

    class Meta:
        verbose_name = "Lote de Tingimento"
        verbose_name_plural = "Lotes de Tingimento"
        ordering = ['-data_criacao']

    def __str__(self):
        return f"Lote de Tingimento #{self.id} - Cor: {self.cor_final_alvo}"


class LancamentoTingimento(models.Model):
    lote = models.ForeignKey(LoteTingimento, on_delete=models.CASCADE, related_name="lancamentos")
    responsavel = models.ForeignKey(Operador, on_delete=models.PROTECT)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField(null=True, blank=True)
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Lançamento de Tingimento"
        verbose_name_plural = "Lançamentos de Tingimento"
        ordering = ['-data_hora_inicio']

    def __str__(self):
        return f"Lançamento #{self.id} para o Lote #{self.lote.id}"


class ItemTingimento(models.Model):
    """
    Modelo 'through' que define QUAIS ITENS pertencem a um Lote de Tingimento
    e qual o seu destino final.
    """
    lote = models.ForeignKey(LoteTingimento, on_delete=models.CASCADE, related_name="itens_no_lote", null=True)
    item_demanda = models.ForeignKey(ItemDemandaProducao, on_delete=models.PROTECT, related_name="apontamentos_tingimento")
    proximo_setor = models.ForeignKey(
        'cadastros.Setor',
        on_delete=models.PROTECT,
        null=True, blank=True,
        limit_choices_to={'nome__in': ['ESCOLHA FINAL', 'TORNO', 'LASER', 'POLIMENTO']},
        help_text="Destino do item após o tingimento."
    )

    class Meta:
        unique_together = ('lote', 'item_demanda')
        verbose_name = "Item do Lote de Tingimento"
        verbose_name_plural = "Itens nos Lotes de Tingimento"

    def __str__(self):
        return f"Item {self.item_demanda.id} no Lote de Tingimento #{self.lote.id}"

    @property
    def peso_total_processado(self):
        """Soma o peso processado para este item em todos os lançamentos do lote."""
        total = self.cargas.aggregate(total=Sum('peso_carregado'))['total']
        return total or decimal.Decimal('0.0')


class CargaLancamentoTingimento(models.Model):
    """
    Registra o peso de um item específico que foi carregado
    em um lançamento de tingimento específico.
    """
    lancamento = models.ForeignKey(LancamentoTingimento, on_delete=models.CASCADE, related_name="cargas")
    item_tingimento = models.ForeignKey(ItemTingimento, on_delete=models.CASCADE, related_name="cargas")
    peso_carregado = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    class Meta:
        verbose_name = "Carga de Lançamento de Tingimento"
        verbose_name_plural = "Cargas de Lançamentos de Tingimento"
        unique_together = ('lancamento', 'item_tingimento')


class ParadaTingimento(models.Model):
    lancamento_tingimento = models.ForeignKey(LancamentoTingimento, on_delete=models.CASCADE, related_name="paradas")
    motivo = models.ForeignKey(MotivoParada, on_delete=models.PROTECT)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Parada no Lançamento de Tingimento #{self.lancamento_tingimento.id}"

class BaseApontamentoItemDemanda(BaseApontamento):
    """ Nova classe base para apontamentos vinculados a um ItemDemandaProducao. """
    item_demanda = models.ForeignKey(
        'ItemDemandaProducao', 
        on_delete=models.CASCADE, 
        related_name="%(class)s_apontamentos",
        null=True, 
        blank=True
    )

    class Meta:
        abstract = True

class ContagemFinal(BaseApontamentoIndividualOP):
    class TipoEmbalagem(models.TextChoices):
        NEUTRA = 'NEUTRA', 'Neutra'
        IMPRESSA = 'IMPRESSA', 'Impressa'
    class TipoPesagem(models.TextChoices):
        G_1 = 'G_1', '1 Grosas'
        G_3 = 'G_3', '3 Grosas'
        G_5 = 'G_5', '5 Grosas'
        G_10 = 'G_10', '10 Grosas'
        KG_PC = 'KG_PC', 'KG(PÇ)'

    # --- CORREÇÃO APLICADA AQUI ---
    # O campo foi tornado opcional no banco de dados com null=True e blank=True.
    maquina_contagem = models.ForeignKey(
        Maquina, 
        on_delete=models.PROTECT, 
        limit_choices_to={'setor__nome': 'ESCOLHA FINAL'},
        null=True,
        blank=True
    )
    
    tipo_embalagem = models.CharField(max_length=20, choices=TipoEmbalagem.choices)
    pesagem = models.CharField(max_length=20, choices=TipoPesagem.choices)
    total_embalagem = models.IntegerField()

class ControleEsteira(BaseApontamentoIndividualOP):
    class Unidade(models.TextChoices):
        KG = 'KG', 'Kg'
        GROSA = 'GROSA', 'Grosa'
        UN = 'UN', 'Unidade'
    quantidade_defeito = models.DecimalField(max_digits=10, decimal_places=3)
    unidade_defeito = models.CharField(max_length=10, choices=Unidade.choices)

class ReprogramacaoOP(models.Model):
    ordem_producao = models.ForeignKey(OrdemProducao, on_delete=models.CASCADE, related_name="reprogramacoes")
    motivo = models.ForeignKey(MotivoReprogramacao, on_delete=models.PROTECT)
    setor_origem = models.ForeignKey('cadastros.Setor', on_delete=models.PROTECT)
    data_reprogramacao = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)
    responsavel = models.ForeignKey(Operador, on_delete=models.PROTECT)
    
    # --- NOVO CAMPO PARA QUANTIDADE PARCIAL ---
    peso_reprogramado = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True,
        help_text="Peso (Kg) a ser reprogramado. Se nulo, reprograma a OP inteira."
    )

class TransferenciaEntreSetores(models.Model):
    """ Registra o movimento de uma quantidade de material de uma OP entre dois setores. """
    ordem_producao = models.ForeignKey(OrdemProducao, on_delete=models.CASCADE, related_name="transferencias")
    setor_origem = models.ForeignKey('cadastros.Setor', on_delete=models.PROTECT, related_name="transferencias_saida")
    setor_destino = models.ForeignKey('cadastros.Setor', on_delete=models.PROTECT, related_name="transferencias_entrada")
    
    peso_transferido = models.DecimalField(max_digits=10, decimal_places=4)
    data_transferencia = models.DateTimeField(auto_now_add=True)
    responsavel = models.ForeignKey(Operador, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.peso_transferido} Kg da OP {self.ordem_producao.numero_op} movido de {self.setor_origem} para {self.setor_destino}"

class SaldoOPSetor(models.Model):
    """ Armazena o saldo de peso de uma OP em um determinado setor para otimizar consultas. """
    ordem_producao = models.ForeignKey(OrdemProducao, on_delete=models.CASCADE, related_name="saldos_por_setor")
    setor = models.ForeignKey('cadastros.Setor', on_delete=models.CASCADE)
    saldo_peso = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    class Meta:
        unique_together = ('ordem_producao', 'setor')

    def __str__(self):
        return f"Saldo de {self.saldo_peso} Kg para OP {self.ordem_producao.numero_op} no setor {self.setor.nome}"

class RegraKanban(models.Model):
    artigo = models.CharField(max_length=100, unique=True, help_text="Código do Artigo que pode ser Kanban")
    material_nome = models.CharField(max_length=100, help_text="Nome do material (ex: Sumatra, PEC)", null=True)
    material_codigo_erp = models.CharField(max_length=20, help_text="Código do material no ERP (ex: 9, 28, 8)", null=True)
    cor_base_neutra = models.CharField(max_length=20, help_text="A cor base 'neutra' para este material (ex: 200, 100, 500)", null=True)

    class Meta:
        verbose_name = "Regra de Kanban"
        verbose_name_plural = "Regras de Kanban"

    def __str__(self):
        return f"Kanban: Artigo {self.artigo} ({self.material_nome})"

class SolicitacaoQuimicaKanban(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        ATENDIDA = 'ATENDIDA', 'Atendida'
        CANCELADA = 'CANCELADA', 'Cancelada'

    ordem_producao = models.ForeignKey(
        OrdemProducao, 
        on_delete=models.CASCADE, 
        related_name="solicitacoes_quimica_kanban", 
        limit_choices_to={'is_kanban': True}
    )
    quantidade_solicitada = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantidade em grosas que o Torno precisa")
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    solicitado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    data_atendimento = models.DateTimeField(null=True, blank=True, help_text="Data e hora em que a Química finalizou a produção")
    
    class Meta:
        verbose_name = "Solicitação Química para Kanban"
        verbose_name_plural = "Solicitações Químicas para Kanban"
        ordering = ['-data_solicitacao']

    def __str__(self):
        return f"Solicitação de {self.quantidade_solicitada} grosas para OP Kanban {self.ordem_producao.numero_op}"
    
# Models de controle de Kanban
class ItemEstoqueKanban(models.Model):
    """
    Define um tipo de pastilha que pode ser estocada no Kanban.
    A chave única é a combinação de material, cor e tamanho.
    """
    material = models.CharField(max_length=100, help_text="Ex: Sumatra, PEC, Cristal")
    cor = models.CharField(max_length=100, help_text="Cor base da matéria-prima, ex: 200, 100, 500")
    tamanho = models.CharField(max_length=50, default="18", help_text="Tamanho padrão para Kanban, geralmente '18'")
    
    peso_bruto_grosa_medio = models.DecimalField(
        max_digits=19, 
        decimal_places=6, 
        null=True, blank=True,
        help_text="Média ou último valor registrado do peso bruto por grôsa (em gramas). Usado como referência."
    )

    class Meta:
        verbose_name = "Item de Estoque Kanban"
        verbose_name_plural = "Itens de Estoque Kanban"
        unique_together = ('material', 'cor', 'tamanho')
        ordering = ['material', 'cor']

    def __str__(self):
        return f"{self.material} | Cor {self.cor} | Tam {self.tamanho}"


class EstoqueKanban(models.Model):
    """
    Armazena o saldo atual de um ItemEstoqueKanban.
    Os saldos de peso e grôsas são atualizados por transações (MovimentoEstoqueKanban).
    """
    item_estoque = models.OneToOneField(
        ItemEstoqueKanban, 
        on_delete=models.PROTECT, 
        related_name="estoque"
    )
    saldo_peso_kg = models.DecimalField(
        max_digits=10, 
        decimal_places=4, 
        default=0,
        verbose_name="Saldo em Peso (Kg)"
    )
    saldo_grosas_aproximado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name="Saldo em Grôsas (Aproximado)"
    )
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Estoque Kanban"
        verbose_name_plural = "Estoques Kanban"

    def __str__(self):
        return f"Estoque de {self.item_estoque}: {self.saldo_peso_kg} Kg"


class SolicitacaoReposicaoKanban(models.Model):
    """
    Representa o "cartão Kanban" digital, uma ordem de produção interna
    para reabastecer o estoque de um item específico.
    """
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        EM_PRODUCAO = 'EM_PRODUCAO', 'Em Produção'
        AGUARDANDO_CORTE = 'AGUARDANDO_CORTE', 'Aguardando Corte' # <-- ADICIONADO
        AGUARDANDO_PASTILHA = 'AGUARDANDO_PASTILHA', 'Aguardando Medição na Pastilha'
        CONCLUIDA = 'CONCLUIDA', 'Concluída'
        CANCELADA = 'CANCELADA', 'Cancelada'

    item_estoque = models.ForeignKey(
        ItemEstoqueKanban, 
        on_delete=models.PROTECT,
        related_name="solicitacoes_reposicao"
    )
    quantidade_placas_solicitada = models.PositiveIntegerField(
        help_text="Quantidade de placas solicitadas, conforme o cartão Kanban físico."
    )
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDENTE)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    solicitado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True
    )
    observacao = models.TextField(blank=True, null=True)
    
    # Campo para vincular um lançamento de cilindro a esta solicitação
    lancamento_cilindro = models.OneToOneField(
        'LancamentoCilindro', 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name="solicitacao_kanban_atendida"
    )

    class Meta:
        verbose_name = "Solicitação de Reposição Kanban"
        verbose_name_plural = "Solicitações de Reposição Kanban"
        ordering = ['-data_solicitacao']

    def __str__(self):
        return f"Solicitação de {self.quantidade_placas_solicitada} placas para {self.item_estoque}"


class MovimentoEstoqueKanban(models.Model):
    """
    Registra cada transação de entrada, saída ou ajuste no EstoqueKanban,
    garantindo a rastreabilidade completa.
    """
    class Tipo(models.TextChoices):
        ENTRADA_PRODUCAO = 'ENTRADA_PRODUCAO', 'Entrada por Produção'
        SAIDA_CONSUMO = 'SAIDA_CONSUMO', 'Saída por Consumo em OP'
        AJUSTE_POSITIVO = 'AJUSTE_POSITIVO', 'Ajuste de Inventário (Positivo)'
        AJUSTE_NEGATIVO = 'AJUSTE_NEGATIVO', 'Ajuste de Inventário (Negativo)'

    item_estoque = models.ForeignKey(
        ItemEstoqueKanban, 
        on_delete=models.PROTECT, 
        related_name="movimentos"
    )
    tipo_movimento = models.CharField(max_length=20, choices=Tipo.choices)
    peso_movimentado_kg = models.DecimalField(
        max_digits=10, 
        decimal_places=4,
        help_text="Peso em Kg que entrou ou saiu do estoque."
    )
    peso_bruto_grosa_no_momento = models.DecimalField(
        max_digits=19, 
        decimal_places=6, 
        null=True, blank=True,
        help_text="Peso bruto por grôsa (em gramas) real, medido no momento da transação."
    )
    grosas_movimentadas = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Quantidade em grôsas, calculada no momento da transação."
    )
    data_movimento = models.DateTimeField(auto_now_add=True)
    responsavel = models.ForeignKey(
        Operador, 
        on_delete=models.PROTECT, 
        null=True, blank=True
    )
    
    # Campos para rastreabilidade
    ordem_producao_consumo = models.ForeignKey(
        'OrdemProducao', 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        help_text="OP de cliente que consumiu este estoque (para saídas)."
    )
    solicitacao_atendida = models.ForeignKey(
        SolicitacaoReposicaoKanban, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        help_text="Solicitação de reposição que gerou esta entrada no estoque."
    )
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Movimento de Estoque Kanban"
        verbose_name_plural = "Movimentos de Estoque Kanban"
        ordering = ['-data_movimento']

    def __str__(self):
        return f"{self.get_tipo_movimento_display()} de {self.peso_movimentado_kg} Kg para {self.item_estoque}"

class ParadaPolimento(models.Model):
    """ Registra uma parada que ocorreu durante um apontamento de Polimento. """
    apontamento_polimento = models.ForeignKey(ControlePolimento, on_delete=models.CASCADE, related_name="paradas")
    motivo = models.ForeignKey(MotivoParada, on_delete=models.PROTECT)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Parada no Apontamento de Polimento #{self.apontamento_polimento.id}"

class ConferenciaEscolhaFinal(BaseApontamentoItemDemanda):
    """
    Representa a etapa de CONFERÊNCIA na Escolha Final.
    Refatorado para incluir a medição da espessura.
    """
    peso_10_botoes = models.DecimalField(max_digits=10, decimal_places=3, help_text="Peso de 10 botões em gramas")
    peso_aferido = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        help_text="Peso total do lote recebido em Kg", 
        null=True, 
        blank=True, 
        default=0.0
    )
    # --- NOVO CAMPO ADICIONADO ---
    espessura_conferida = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, blank=True,
        help_text="Espessura em mm conferida pela operadora."
    )
    quantidade_grosas_calculada = models.DecimalField(max_digits=10, decimal_places=2, editable=False, help_text="Cálculo automático")

    def save(self, *args, **kwargs):
        # Recalcula o peso da grosa na OP principal antes de salvar
        if self.item_demanda and self.peso_10_botoes and self.peso_10_botoes > 0:
            op = self.item_demanda.ordem_producao
            op.peso_liquido_grosa = (self.peso_10_botoes / 10) * 144
            op.save(update_fields=['peso_liquido_grosa'])
        
        # Calcula a quantidade em grosas com base no peso aferido
        if self.item_demanda and self.item_demanda.ordem_producao.peso_liquido_grosa and self.peso_aferido:
            peso_grosa_g = self.item_demanda.ordem_producao.peso_liquido_grosa
            if peso_grosa_g > 0:
                self.quantidade_grosas_calculada = (self.peso_aferido * 1000) / peso_grosa_g
        super().save(*args, **kwargs)

class ControleQualidadeEsteira(BaseApontamentoItemDemanda):
    """
    Representa o apontamento na ESTEIRA do Controle de Qualidade.
    Atualizado para incluir um segundo operador e a máquina utilizada.
    """
    # O campo 'responsavel' (Operador 1) é herdado de BaseApontamento
    responsavel_2 = models.ForeignKey(
        Operador, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
        related_name='apontamentos_cq_operador2',
        verbose_name="Operador 2 (Opcional)"
    )
    maquina = models.ForeignKey(
        Maquina, 
        on_delete=models.PROTECT,
        null=True, # Definido como nulo para evitar erros em migrações com dados existentes
        verbose_name="Esteira"
    )
    peso_total_aprovado = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        help_text="Peso total dos botões aprovados em Kg",
        null=True,
        default=0
    )
    peso_defeito_tipo_a = models.DecimalField(max_digits=10, decimal_places=3, default=0, help_text="Peso de defeitos visuais em Kg")
    peso_defeito_tipo_b = models.DecimalField(max_digits=10, decimal_places=3, default=0, help_text="Peso de defeitos de medida em Kg")

    def save(self, *args, **kwargs):
        # Renomeia o campo 'peso_total_apontado' para 'peso_total_aprovado' se ele existir no kwargs
        # para manter a compatibilidade com o form antigo, se necessário.
        if 'peso_total_apontado' in kwargs:
            kwargs['peso_total_aprovado'] = kwargs.pop('peso_total_apontado')
        super().save(*args, **kwargs)

class SaldoItemEmbalagem(models.Model):
    """ Armazena o saldo de um item específico em GROSAS no setor de Embalagem. """
    item_demanda = models.OneToOneField(ItemDemandaProducao, on_delete=models.CASCADE, related_name="saldo_embalagem")
    saldo_grosas = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Saldo de {self.saldo_grosas} GRS para o item {self.item_demanda.id}"

class ApontamentoEmbalagem(models.Model):
    """ Registra um apontamento de embalagem para um item de demanda. """
    class TamanhoCaixa(models.TextChoices):
        T1 = '1', 'Tamanho 1'
        T2 = '2', 'Tamanho 2'
        T3 = '3', 'Tamanho 3'
        T4 = '4', 'Tamanho 4'
    
    class TipoCaixa(models.TextChoices):
        LISA = 'LISA', 'Lisa'
        IMPRESSA = 'IMPRESSA', 'Impressa'

    item_demanda = models.ForeignKey(ItemDemandaProducao, on_delete=models.PROTECT, related_name="apontamentos_embalagem")
    responsavel = models.ForeignKey(Operador, on_delete=models.PROTECT)
    quantidade_embalada = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantidade em Grosas")
    numero_caixa = models.PositiveIntegerField()
    tam_cx = models.CharField(max_length=2, choices=TamanhoCaixa.choices, verbose_name="Tamanho da Caixa")
    tipo_caixa = models.CharField(max_length=10, choices=TipoCaixa.choices, default=TipoCaixa.LISA)
    peso_caixa = models.DecimalField(max_digits=10, decimal_places=3, help_text="Peso final da caixa em Kg")
    data_apontamento = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Apontamento de Embalagem"
        verbose_name_plural = "Apontamentos de Embalagem"
        ordering = ['item_demanda__pedido', 'numero_caixa']

    def __str__(self):
        return f"Caixa {self.numero_caixa} - {self.quantidade_embalada} GRS do item {self.item_demanda.id}"

class Caixa(models.Model):
    """
    Representa uma caixa física que agrupa itens para um cliente.
    Uma caixa tem um ID único global e pertence a um cliente, podendo conter itens de vários pedidos.
    """
    class Status(models.TextChoices):
        EM_EMBALAGEM = 'EM_EMBALAGEM', 'Em Embalagem'
        AGUARDANDO_CONFERENCIA = 'AGUARDANDO_CONFERENCIA', 'Aguardando Conferência'
        CONFERIDA = 'CONFERIDA', 'Conferida'
        EM_REMESSA = 'EM_REMESSA', 'Em Remessa' 

    class TamanhoCaixa(models.TextChoices):
        T1 = '1', 'Tamanho 1'
        T2 = '2', 'Tamanho 2'
        T3 = '3', 'Tamanho 3'
        T4 = '4', 'Tamanho 4'
    
    class TipoCaixa(models.TextChoices):
        LISA = 'LISA', 'Lisa'
        IMPRESSA = 'IMPRESSA', 'Impressa'

    id = models.AutoField(primary_key=True, verbose_name="Nº da Caixa")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="caixas")
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.EM_EMBALAGEM)
    
    # Detalhes da Embalagem
    responsavel_embalagem = models.ForeignKey(Operador, on_delete=models.PROTECT, related_name="caixas_embaladas", null=True, blank=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)
    tam_cx = models.CharField(max_length=2, choices=TamanhoCaixa.choices, verbose_name="Tamanho da Caixa")
    tipo_caixa = models.CharField(max_length=10, choices=TipoCaixa.choices)

    # Detalhes da Expedição
    responsavel_expedicao = models.ForeignKey(Operador, on_delete=models.PROTECT, related_name="caixas_conferidas", null=True, blank=True)
    peso_final_caixa = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    data_conferencia = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Caixa de Embalagem"
        verbose_name_plural = "Caixas de Embalagem"
        ordering = ['-id']

    def __str__(self):
        return f"Caixa #{self.id} - {self.cliente.nome}"

class ItemCaixa(models.Model):
    """ Detalha o conteúdo de cada caixa (relação Many-to-Many). """
    caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE, related_name="itens_na_caixa")
    item_demanda = models.ForeignKey('ItemDemandaProducao', on_delete=models.PROTECT, related_name="itens_em_caixas")
    quantidade_embalada = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantidade em Grosas")
    conferido_expedicao = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Item na Caixa"
        verbose_name_plural = "Itens na Caixa"
        unique_together = ('caixa', 'item_demanda')

class Remessa(models.Model):
    """ Representa um envio físico para o cliente, agrupando uma ou mais caixas. """
    class Status(models.TextChoices):
        EM_ABERTO = 'EM_ABERTO', 'Em Aberto'
        ENVIADA = 'ENVIADA', 'Enviada'

    id = models.AutoField(primary_key=True, verbose_name="Nº da Remessa")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="remessas")
    caixas = models.ManyToManyField(Caixa, related_name="remessas", help_text="Caixas incluídas neste envio.")
    data_envio = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.EM_ABERTO)

    class Meta:
        verbose_name = "Remessa de Expedição"
        verbose_name_plural = "Remessas de Expedição"
        ordering = ['-data_envio']

    def __str__(self):
        return f"Remessa #{self.id} para {self.cliente.nome}"

class ConferenciaCaixaExpedicao(models.Model):
    """ Representa a conferência de uma única caixa de um pedido. """
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        EM_CONFERENCIA = 'EM_CONFERENCIA', 'Em Conferência'
        FINALIZADA = 'FINALIZADA', 'Finalizada'

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="conferencias_caixa")
    numero_caixa = models.PositiveIntegerField()
    responsavel = models.ForeignKey(Operador, on_delete=models.PROTECT, null=True, blank=True)
    peso_conferido = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, help_text="Peso final da caixa em Kg")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    data_inicio_conferencia = models.DateTimeField(null=True, blank=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Conferência de Caixa para Expedição"
        verbose_name_plural = "Conferências de Caixas para Expedição"
        unique_together = ('pedido', 'numero_caixa')
        ordering = ['pedido', 'numero_caixa']

    def __str__(self):
        return f"Conferência Caixa #{self.numero_caixa} do Pedido {self.pedido.numero_pedido}"

class ItemConferenciaCaixa(models.Model):
    """ Vincula um item embalado a uma conferência de caixa, registrando se foi checado. """
    conferencia_caixa = models.ForeignKey(ConferenciaCaixaExpedicao, on_delete=models.CASCADE, related_name="itens_conferidos")
    apontamento_embalagem = models.OneToOneField(ApontamentoEmbalagem, on_delete=models.CASCADE, related_name="item_conferido")
    conferido = models.BooleanField(default=False)

    def __str__(self):
        return f"Item {self.apontamento_embalagem.id} na conferência da Caixa #{self.conferencia_caixa.numero_caixa}"
