from django.db import models

class Usuario(models.Model):
    # Chave primária única para o Django
    codigo = models.AutoField(primary_key=True, db_column='UsrCod')
    
    # Campos obrigatórios da tabela
    usrempcod = models.IntegerField(db_column='UserEmpCod', default=1)
    login = models.CharField(max_length=50, unique=True, db_column='UsrLogin')
    
    # Outros campos da tabela
    senha = models.CharField(max_length=50, db_column='UsrSenha', blank=True, null=True)
    nome = models.CharField(max_length=50, db_column='UsrNom', blank=True, null=True)
    email_pessoal = models.CharField(max_length=255, db_column='UsrEmailPes', default='', blank=True)
    usrema = models.CharField(max_length=100, db_column='UsrEma', default='sisven@ibg.ind.br', blank=True)
    usrsenema = models.CharField(max_length=30, db_column='UsrSenEma', default='sisven2903', blank=True)
    celular_sms = models.CharField(max_length=20, db_column='UsrSmsCel', blank=True, null=True)
    status = models.CharField(max_length=30, db_column='UsrSta', default='ATIVO')
    
    liberar_pedidos = models.CharField(max_length=1, db_column='UsrLibPed', default='N')
    exportar_pedidos_liberados = models.CharField(max_length=1, db_column='UsrPedLiberado', default='N')
    desbloquear_pedidos = models.CharField(max_length=1, db_column='DesbloqPed', default='N')
    alterar_pedidos_liberados = models.CharField(max_length=1, db_column='AltPedLibPro', default='N')
    alterar_previsao_entrega = models.CharField(max_length=1, db_column='AtlPrevEnt', default='N')
    alterar_info_financeira_pedido = models.CharField(max_length=1, db_column='AltInfFinPed', default='N')
    importar_pedidos_franquiados = models.CharField(max_length=1, db_column='ImportarPedidosFranquiados', default='N')
    digitar_orcamento = models.CharField(max_length=1, db_column='Orcamento', default='N')
    relatorio_pedidos = models.CharField(max_length=1, db_column='UsrRelPed', default='N')
    relatorio_pedidos_cliente = models.CharField(max_length=1, db_column='UsrRelPedCli', default='N')
    relatorio_pedidos_representante = models.CharField(max_length=1, db_column='UsrRelPedRep', default='N')
    consultar_ultima_compra_artigo = models.CharField(max_length=1, db_column='UsrConArtPedCli', default='N')
    relatorio_titulos_aberto = models.CharField(max_length=1, db_column='UsrRelTitAbe', default='N')
    mudar_cliente_provisorio = models.CharField(max_length=1, db_column='MudCliProvNorm', default='N')
    alterar_senha = models.CharField(max_length=1, db_column='AltSen', default='N')
    relatorio_titulos = models.CharField(max_length=1, db_column='RelTit', default='N')
    ver_margem_lucro = models.CharField(max_length=1, db_column='VerMargemLucro', default='N')
    configurar_grade_custo = models.CharField(max_length=1, db_column='GrdCusBot', default='N')
    consultar_grade_custo = models.CharField(max_length=1, db_column='GrdCusBotConsultar', default='N')
    adicionar_parametros_botao = models.CharField(max_length=1, db_column='AddParBot', default='N')
    alterar_parametros_botao = models.CharField(max_length=1, db_column='AltExcParBot', default='N')
    cadastrar_cod_gravacao = models.CharField(max_length=1, db_column='CadCodGravacao', default='N')
    consultar_preco_custo = models.CharField(max_length=1, db_column='ConsPrecCusto', default='N')
    relatorio_posicao_pedidos = models.CharField(max_length=1, db_column='RelPosPed', default='N')
    grafico_ranking_vendas = models.CharField(max_length=1, db_column='GrafRankVen', default='N')
    grafico_vendas_representante = models.CharField(max_length=1, db_column='GrafVenPorRepre', default='N')
    grafico_ranking_clientes = models.CharField(max_length=1, db_column='RelRankCli', default='N')
    alterar_celular_sms_cliente = models.CharField(max_length=1, db_column='InsAltNroCelSms', default='N')
    enviar_sms_pedido_cliente = models.CharField(max_length=1, db_column='EnvSMSPedCli', default='N')
    enviar_sms_representante = models.CharField(max_length=1, db_column='EnvSMSRepres', default='N')
    relatorio_pedidos_emitidos_ibg = models.CharField(max_length=1, db_column='RelPedEmiIBG', default='N')
    ver_valores_faturados = models.CharField(max_length=1, db_column='ValFaturados', default='N')
    cadastrar_lista_preco = models.CharField(max_length=1, db_column='CadListaPreco', default='N')
    gerar_lista_preco = models.CharField(max_length=1, db_column='GeraListPreco', default='N')
    imprimir_lista_preco = models.CharField(max_length=1, db_column='RelListPreco', default='N')
    consultar_dados_cliente = models.CharField(max_length=1, db_column='ConsDadosCliente', default='N')
    consultar_cod_personalizado = models.CharField(max_length=1, db_column='ConsCodPersonalizado', default='N')
    politica_vendas = models.CharField(max_length=1, db_column='PoliticaVendas', default='N')
    consultar_preco_venda = models.CharField(max_length=1, db_column='ConsPrecVenda', default='N')
    aceitar_arroba_50 = models.CharField(max_length=1, db_column='AceArrCinq', default='N')
    relatorio_drp = models.CharField(max_length=1, db_column='RelDRP', default='N')
    consultar_serasa = models.CharField(max_length=1, db_column='ConsultarSerasaDoPedido', default='N')
    cadastrar_comissao = models.CharField(max_length=1, db_column='ComissaoForm', default='N')
    excecao_comissao_cliente = models.CharField(max_length=1, db_column='ExcecoeDeComissaoPorClienteForm', default='N')
    cadastrar_obs_fixa_cliente = models.CharField(max_length=1, db_column='CadObsFixa', default='N')
    cadastrar_madeiras = models.CharField(max_length=1, db_column='CadMadeiras', default='N')
    grade_custo_botao_madeira = models.CharField(max_length=1, db_column='GradeCustoBotMad', default='N')
    rendimento_pastilha_madeira = models.CharField(max_length=1, db_column='RendPastBotMad', default='N')
    parametro_artigo_madeira = models.CharField(max_length=1, db_column='PrametroArtBotDeMad', default='N')
    alterar_dados_cliente = models.CharField(max_length=1, db_column='AltDadosCliente', default='N')
    excecao_comissao_pedido = models.CharField(max_length=1, db_column='ExcComissaoPorPedido', default='N')
    controle_oda = models.CharField(max_length=1, db_column='ControleOrdemAmostra', default='N')
    apontamento_final_oda = models.CharField(max_length=1, db_column='ApontamentoFinalOda', default='N')
    imprimir_apontamento_final_oda = models.CharField(max_length=1, db_column='ImprimirApontamentoFinalDeAmostra', default='N')
    apontamento_itens_oda_producao = models.CharField(max_length=1, db_column='ApontamentoDeItensDaOrdemAmostraNaProducao', default='N')
    imprimir_oda_producao_prazo = models.CharField(max_length=1, db_column='ImprimirOrdensAmostraEmProducaoPorPrazo', default='N')
    posicao_odas = models.CharField(max_length=1, db_column='PosicaoDeOrdensDeAmostra', default='N')
    limite_credito = models.CharField(max_length=1, db_column='LimiteCredito', default='N')
    consultar_limite_credito = models.CharField(max_length=1, db_column='ConsultaLimiteCredito', default='N')
    liberar_cliente_provisorio = models.CharField(max_length=1, db_column='LiberarClienteProv', default='N')
    historico_vendas_artigo = models.CharField(max_length=1, db_column='HistoricoVendasDoArtigo', default='N')
    espelho_nota_fiscal = models.CharField(max_length=1, db_column='EspelhoNotaFiscal', default='N')
    relatorio_pedidos_on_time = models.CharField(max_length=1, db_column='RelPedProdOnTime', default='N')
    gerir_relacionamento_cliente = models.CharField(max_length=1, db_column='GerirRelacCli', default='N')
    historico_conversas_cliente = models.CharField(max_length=1, db_column='CrmHistConvCli', default='N')
    criar_grupos_clientes = models.CharField(max_length=1, db_column='GruposClientes', default='N')
    consultar_grupos_clientes = models.CharField(max_length=1, db_column='GrupClienteConsulta', default='N')
    gerenciar_clientes_grupos = models.CharField(max_length=1, db_column='GruposVersusClientes', default='N')
    alterar_representante_cliente = models.CharField(max_length=1, db_column='AlterarRepDoCli', default='N')

    class Meta:
        managed = False
        db_table = 'usuarios'


class Representante(models.Model):
    # Chave primária única para o Django
    id = models.AutoField(primary_key=True)
    
    # Outras partes da chave composta tratadas como campos normais
    codigo = models.IntegerField(db_column='RepCod')
    repempcod = models.IntegerField(db_column='RepEmpCod', default=1)
    login = models.CharField(max_length=20, unique=True, db_column='RepLogin')
    codigo_lista_preco = models.IntegerField(db_column='Lis1Cod')

    # Outros campos da tabela
    status = models.CharField(max_length=30, db_column='RepSta', default='ATIVO')
    nome = models.CharField(max_length=50, db_column='RepNom', blank=True, null=True)
    senha = models.CharField(max_length=20, db_column='RepSen', default='', blank=True)
    email_pessoal = models.CharField(max_length=255, db_column='RepEmaPes', default='', blank=True)
    repema = models.CharField(max_length=80, db_column='RepEma', default='sisven@ibg.ind.br', blank=True)
    repemasen = models.CharField(max_length=20, db_column='RepEmaSen', default='sisven2903', blank=True)
    celular = models.CharField(max_length=20, db_column='RepNroCel', default='', blank=True)
    lis1internacionalcod = models.IntegerField(db_column='Lis1InternacionalCod', default=0)
    reptipven = models.IntegerField(db_column='RepTipVen')
    
    # Permissões
    digitar_pedidos = models.CharField(max_length=1, db_column='RepDigPed', default='S')
    cancelar_pedidos = models.CharField(max_length=1, db_column='RepCanPedEnv', default='S')
    relatorio_pedidos_cliente = models.CharField(max_length=1, db_column='RepRelPed', default='S')
    relatorio_pedidos_data = models.CharField(max_length=1, db_column='RepRelPedCli', default='S')
    historico_compras_cliente = models.CharField(max_length=1, db_column='RepConArtPedCli', default='S')
    historico_vendas_artigo = models.CharField(max_length=1, db_column='HistVendaArtigo', default='S')
    ver_titulos_aberto = models.CharField(max_length=1, db_column='RepRelTitAbe', default='S')
    enviar_pedido_email_cliente = models.CharField(max_length=1, db_column='EnvPedEmaCli', default='S')
    alterar_senha = models.CharField(max_length=1, db_column='AltSen', default='S')
    relatorio_titulos = models.CharField(max_length=1, db_column='RelTit', default='S')
    posicao_pedidos = models.CharField(max_length=1, db_column='RelPosPed', default='S')
    grafico_vendas_representante = models.CharField(max_length=1, db_column='GrafVenPorRepre', default='S')
    ranking_clientes = models.CharField(max_length=1, db_column='RelRankCli', default='S')
    relatorio_titulos_baixados = models.CharField(max_length=1, db_column='RelTitBai', default='S')
    alterar_celular_sms_cliente = models.CharField(max_length=1, db_column='InsAltNroCelSms', default='S')
    enviar_sms_pedido_cliente = models.CharField(max_length=1, db_column='EnvSMSPedCli', default='S')
    imprimir_lista_preco = models.CharField(max_length=1, db_column='RelListPreco', default='S')
    consultar_dados_cliente = models.CharField(max_length=1, db_column='ConsDadosCliente', default='S')
    consultar_cod_personalizado = models.CharField(max_length=1, db_column='ConsCodPersonalizado', default='S')
    consultar_preco_venda = models.CharField(max_length=1, db_column='ConsPrecVenda', default='S')
    aceitar_arroba_50 = models.CharField(max_length=1, db_column='AceArrCinq', default='N')
    alterar_dados_cliente = models.CharField(max_length=1, db_column='AltDadosCliente', default='S')
    gerenciar_oda = models.CharField(max_length=1, db_column='OdaRepForm', default='S')
    imprimir_oda_prazo = models.CharField(max_length=1, db_column='OdaImprimirPorPrazoForm', default='S')
    imprimir_oda_virou_pedido = models.CharField(max_length=1, db_column='OdaImprimirSeVirouPedidoForm', default='S')
    apontar_oda_producao = models.CharField(max_length=1, db_column='OdaApontOdaProducaoForm', default='S')
    espelho_nota_fiscal = models.CharField(max_length=1, db_column='EspelhoNotaFiscal', default='S')
    gerir_relacionamento_cliente = models.CharField(max_length=1, db_column='GerirRelacCli', default='S')
    historico_conversas_cliente = models.CharField(max_length=1, db_column='CrmHistConvCli', default='S')
    consultar_grupos_clientes = models.CharField(max_length=1, db_column='GrupClienteConsulta', default='S')

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


    class Meta:
        managed = False
        db_table = 'representantes'

class ListaPrecoCabecalho(models.Model):
    """
    Representa o cabeçalho de uma lista de preços (tabela lispre01).
    Define o nome da lista e a moeda utilizada.
    """
    codigo = models.AutoField(primary_key=True, db_column='Lis1Cod')
    moeda = models.CharField(max_length=15, db_column='Lis1Moeda')
    nome = models.CharField(max_length=50, db_column='Lis1Nom')
    margem_lucro_padrao = models.FloatField(db_column='Lis1PorcMargLucr')

    class Meta:
        managed = False
        db_table = 'lispre01'
        verbose_name = 'Cabeçalho da Lista de Preço'
        verbose_name_plural = 'Cabeçalhos das Listas de Preços'

    def __str__(self):
        return f"{self.nome} ({self.moeda})"


class ListaPrecoItem(models.Model):
     
    lista_preco_codigo = models.IntegerField(primary_key=True, db_column='Lis1Cod')
    
    data_geracao = models.DateField(db_column='Lis2DtaGerada')
    artigo = models.CharField(max_length=20, db_column='Lis2Artigo', blank=True, null=True)
    tamanho = models.CharField(max_length=10, db_column='Lis2Tam', blank=True, null=True)
    
    # Preços para @100
    preco_venda_100 = models.FloatField(db_column='LisPreVendaArr100', blank=True, null=True)
    preco_custo_100 = models.FloatField(db_column='Lis2PreCustoArr100', blank=True, null=True)
    
    # Preços para @50
    preco_venda_50 = models.FloatField(db_column='Lis2PreVendaArr50', blank=True, null=True)
    preco_custo_50 = models.FloatField(db_column='Lis2PreCustoArr50', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lispre02'
        verbose_name = 'Item da Lista de Preço'
        verbose_name_plural = 'Itens da Lista de Preços'
        ordering = ['artigo', 'tamanho']

    def __str__(self):
        return f"Artigo {self.artigo} - Tam {self.tamanho}"

class Cliente(models.Model):
    clicod = models.AutoField(primary_key=True, db_column='CliCod')
    uuid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    clidatcad = models.DateField(db_column='CliDatCad', blank=True, null=True)
    clicnpj = models.CharField(max_length=30, unique=True, db_column='CliCnpj', blank=True, null=True)
    cliinsest = models.CharField(max_length=30, db_column='CliInsEst', blank=True, null=True)
    clinom = models.CharField(max_length=100, db_column='CliNom', blank=True, null=True)
    clinomfan = models.CharField(max_length=100, db_column='CliNomFan', blank=True, null=True)
    cliendrua = models.CharField(max_length=50, db_column='CliEndRua', blank=True, null=True)
    cliendnro = models.CharField(max_length=50, db_column='CliEndNro', blank=True, null=True)
    cliendbai = models.CharField(max_length=50, db_column='CliEndBai', blank=True, null=True)
    cliendcep = models.CharField(max_length=50, db_column='CliEndCep', blank=True, null=True)
    cliendcidcod = models.IntegerField(db_column='CliEndCidCod', blank=True, null=True)
    cliendcidnom = models.CharField(max_length=50, db_column='CliEndCidNom', blank=True, null=True)
    cliendcidest = models.CharField(max_length=15, db_column='CliEndCidEst', blank=True, null=True)
    cliendcidpais = models.CharField(max_length=50, db_column='CliEndCidPais', blank=True, null=True)
    clicon = models.CharField(max_length=50, db_column='CliCon', blank=True, null=True)
    clicar = models.CharField(max_length=50, db_column='CliCar', blank=True, null=True)
    cliema = models.CharField(max_length=50, db_column='CliEma', blank=True, null=True)
    clitel = models.CharField(max_length=30, db_column='CliTel', blank=True, null=True)
    clitel2 = models.CharField(max_length=30, db_column='CliTel2', blank=True, null=True)
    clifax = models.CharField(max_length=30, db_column='CliFax', blank=True, null=True)
    clicel = models.CharField(max_length=30, db_column='CliCel', blank=True, null=True)
    
    representante = models.ForeignKey(
        Representante, 
        on_delete=models.SET_NULL, 
        db_column='RepId', 
        blank=True, 
        null=True,
        related_name='clientes'
    )
    
    clirepcod = models.IntegerField(db_column='CliRepCod', blank=True, null=True)
    clirepnom = models.CharField(max_length=50, db_column='CliRepNom', blank=True, null=True)
    cliemanfe = models.CharField(max_length=51, db_column='CliEmaNFE', blank=True, null=True)

    def __str__(self):
        return f'{self.clinom} - {self.clicnpj}'

    class Meta:
        managed = False
        db_table = 'clientes'


class Cliente02(models.Model):
    # Chave primária da própria tabela clientes02
    cli2id = models.AutoField(primary_key=True, db_column='Cli2Id')
    
    # Relação OneToOne com a tabela principal 'clientes', usando a coluna Cli2Cod para a junção.
    cliente = models.OneToOneField(
        Cliente, 
        on_delete=models.CASCADE, 
        db_column='Cli2Cod', 
        related_name='dados_adicionais'
    )
    
    # Campos reais da tabela clientes02
    cliacedata = models.CharField(max_length=3, db_column='CliAceData', blank=True, null=True)
    clisisven = models.CharField(max_length=3, db_column='CliSisVen', blank=True, null=True)
    clicelsms = models.CharField(max_length=20, db_column='CliCelSms', blank=True, null=True)
    envpedsms = models.CharField(max_length=3, db_column='EnvPedSms', blank=True, null=True)

    def __str__(self):
        return f"Dados Adicionais para Cliente Cód: {self.cliente.clicod}"

    class Meta:
        managed = False
        db_table = 'clientes02'

# Modelo para a tabela: com_rep_sub
class ComRepSub(models.Model):
    id = models.AutoField(primary_key=True)
    # Relação OneToOne porque cada representante só pode ter uma configuração padrão.
    representante = models.OneToOneField(Representante, on_delete=models.CASCADE, db_column='representante_id')
    repcod = models.IntegerField()
    dias_max_sem_visita = models.IntegerField(default=60)
    percentual_comissao = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Configuração para {self.representante.nome}"

    class Meta:
        managed = False
        db_table = 'com_rep_sub'
        verbose_name = 'Configuração de Comissão por Representante'
        verbose_name_plural = 'Configurações de Comissão por Representante'

# Modelo para a tabela: com_cli_esp
class ComCliEsp(models.Model):
    id = models.AutoField(primary_key=True)
    # Relação OneToOne porque cada cliente só pode ter uma configuração específica.
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, db_column='clicod')
    clinom = models.CharField(max_length=100, blank=True, null=True)
    dias_max_sem_visita = models.IntegerField(default=60)
    percentual_comissao = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Configuração Específica para {self.clinom}"

    class Meta:
        managed = False
        db_table = 'com_cli_esp'
        verbose_name = 'Configuração de Comissão por Cliente'
        verbose_name_plural = 'Configurações de Comissão por Cliente'

# Modelo para a tabela: com_log_ped_rep_cli
class ComLogPedRepCli(models.Model):
    id = models.AutoField(primary_key=True)
    pedidocod = models.IntegerField() # Idealmente, seria uma ForeignKey para um modelo Pedido
    representante_principal = models.ForeignKey(Representante, on_delete=models.RESTRICT, related_name='logs_como_principal')
    representante_subordinado = models.ForeignKey(Representante, on_delete=models.SET_NULL, related_name='logs_como_subordinado', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, db_column='clicod')
    data_pedido = models.DateField()

    def __str__(self):
        return f"Log do Pedido {self.pedidocod}"

    class Meta:
        managed = False
        db_table = 'com_log_ped_rep_cli'
        verbose_name = 'Log de Vínculo de Representantes'
        verbose_name_plural = 'Logs de Vínculos de Representantes'
