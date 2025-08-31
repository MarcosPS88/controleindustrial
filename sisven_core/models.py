from email.policy import default

from django.db import models


# ==============================================================================
# Modelos Base (Usuário, Representante, Cliente, etc.)
# ==============================================================================

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

    # ... (todos os campos de permissão de Usuario)
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
    imprimir_apontamento_final_oda = models.CharField(max_length=1, db_column='ImprimirApontamentoFinalDeAmostra',
                                                      default='N')
    apontamento_itens_oda_producao = models.CharField(max_length=1,
                                                      db_column='ApontamentoDeItensDaOrdemAmostraNaProducao',
                                                      default='N')
    imprimir_oda_producao_prazo = models.CharField(max_length=1, db_column='ImprimirOrdensAmostraEmProducaoPorPrazo',
                                                   default='N')
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

class RepTipoChoices(models.TextChoices):
    TELEVENDAS = 'TELEVENDAS', 'Televendas'
    PRESENCIAL = 'PRESENCIAL', 'Presencial'

class Representante(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.IntegerField(db_column='RepCod')
    repempcod = models.IntegerField(db_column='RepEmpCod', default=1)
    login = models.CharField(max_length=20, unique=True, db_column='RepLogin')
    codigo_lista_preco = models.IntegerField(db_column='Lis1Cod')
    status = models.CharField(max_length=30, db_column='RepSta', default='ATIVO')
    nome = models.CharField(max_length=50, db_column='RepNom', blank=True, null=True)
    senha = models.CharField(max_length=20, db_column='RepSen', default='', blank=True)
    email_pessoal = models.CharField(max_length=255, db_column='RepEmaPes', default='', blank=True)
    repema = models.CharField(max_length=80, db_column='RepEma', default='sisven@ibg.ind.br', blank=True)
    repemasen = models.CharField(max_length=20, db_column='RepEmaSen', default='sisven2903', blank=True)
    celular = models.CharField(max_length=20, db_column='RepNroCel', default='', blank=True)
    lis1internacionalcod = models.IntegerField(db_column='Lis1InternacionalCod', default=0)
    reptipven = models.IntegerField(db_column='RepTipVen')

    # ... (todos os campos de permissão de Representante)
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
    rep_tipo = models.CharField(
        max_length=50, choices=RepTipoChoices.choices, default=RepTipoChoices.TELEVENDAS
    )

    def __str__(self):
        return f'{self.codigo} - {self.nome} - {self.rep_tipo}'

    class Meta:
        managed = False
        db_table = 'representantes'


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


# ... (outros modelos como Cliente02, ListaPreco, etc. permanecem aqui)

# ==============================================================================
# Modelos de Pedido (Ped01, Ped02, Ped03, Ped04) - CORRIGIDOS E COMPLETOS
# ==============================================================================

class Ped01(models.Model):
    pedcod = models.AutoField(db_column='PedCod', primary_key=True)
    uuid = models.CharField(max_length=255, blank=True, null=True)

    # --- Relacionamentos Corrigidos ---
    pedempcod = models.IntegerField(db_column='PedEmpCod')
    cliente = models.ForeignKey(
        Cliente,
        models.DO_NOTHING,
        db_column='PedCliCod',
        related_name='pedidos',
        blank=True,
        null=True
    )
    representante = models.ForeignKey(
        'Representante',
        models.DO_NOTHING,
        db_column='PedRepId',
        related_name='pedidos',
        blank=True,
        null=True
    )

    # --- Todos os outros campos mantidos ---
    pedordcomp = models.CharField(db_column='PedOrdComp', max_length=20, blank=True, null=True,
                                  db_comment='Ordem de compra')
    peddat = models.DateField(db_column='PedDat', blank=True, null=True)
    peddatacedata = models.DateField(db_column='PedDatAceData', blank=True, null=True,
                                     db_comment='Data do pedido que ira para o Ace-Data quando exportar o pedido')
    peddatfin = models.DateField(db_column='PedDatFin', blank=True, null=True)
    peddatutifin = models.DateField(db_column='PedDatUtiFin', blank=True, null=True)
    pedhorafin = models.TimeField(db_column='PedHoraFin', blank=True, null=True)
    peddatprevent = models.DateField(db_column='PedDatPrevEnt', blank=True, null=True)
    pedtipven = models.CharField(db_column='PedTipVen', max_length=30, blank=True, null=True)
    pedclinom = models.CharField(db_column='PedCliNom', max_length=100, blank=True, null=True)
    pedclinov = models.CharField(db_column='PedCliNov', max_length=3, blank=True, null=True)
    pedrepcod = models.IntegerField(db_column='PedRepCod', blank=True, null=True)
    pedrepnom = models.CharField(db_column='PedRepNom', max_length=50, blank=True, null=True)
    pedsta = models.CharField(db_column='PedSta', max_length=20, blank=True, null=True,
                              db_comment='Status do pedido, ôATIVO ou INATIVOö')
    pedstafin = models.CharField(db_column='PedStaFin', max_length=3, blank=True, null=True)
    pedstalib = models.CharField(db_column='PedStaLib', max_length=3, blank=True, null=True)
    pedimportado = models.CharField(db_column='PedImportado', max_length=3, blank=True, null=True,
                                    db_comment='controla se ja foi gerado o arquivo txt do pedido')
    pedstalido = models.CharField(db_column='PedStaLido', max_length=3, blank=True, null=True,
                                  db_comment='status que controla se o pedido ja foi lido pelas meninas que irao digitar o pedido')
    pednotificado = models.CharField(db_column='PedNotificado', max_length=3, blank=True, null=True,
                                     db_comment='indica se o pedido teve alguma notificacao')
    pedtotbru = models.FloatField(db_column='PedTotBru', blank=True, null=True)
    pedtotliq = models.FloatField(db_column='PedTotLiq', blank=True, null=True)
    pedmod = models.CharField(db_column='PedMod', max_length=20, blank=True, null=True)
    pedpordes = models.FloatField(db_column='PedPorDes', blank=True, null=True)
    pedvaldes = models.FloatField(db_column='PedValDes', blank=True, null=True)
    pedobs = models.TextField(db_column='PedObs', blank=True, null=True)
    pedobsfixa = models.TextField(db_column='PedObsFixa')
    peddescfinpedaltpor = models.CharField(db_column='PedDescFinPedAltPor', max_length=50,
                                           db_comment='nome da pessoa que autorizou o representante a dar o desconto no final do pedido')
    peddescfinpedmot = models.TextField(db_column='PedDescFinPedMot', blank=True, null=True,
                                        db_comment='o motivo que o represntante teve que dar um desconto no final do pedido')
    pedcpgcod = models.IntegerField(db_column='PedCpgCod', blank=True, null=True,
                                    db_comment='codigo da condicao de pagamento no ace-data')
    pedcpgdesc = models.CharField(db_column='PedCpgDesc', max_length=255, blank=True, null=True,
                                  db_comment='Descricao da forma de pagamento, esse valor Ú pego na tabela do mysql do sisven')
    pedcpgpra = models.CharField(db_column='PedCpgPra', max_length=30, blank=True, null=True,
                                 db_comment='Condicao de pagamento, valor pego do banco de dados do sisven')
    pedcodformpagto = models.IntegerField(db_column='PedCodFormPagto', blank=True, null=True,
                                          db_comment='codigo forma de pagamento no ace data')
    pedformpagto = models.CharField(db_column='PedFormPagto', max_length=30, blank=True, null=True)
    pedporlucmed = models.FloatField(db_column='PedPorLucMed', blank=True, null=True,
                                     db_comment='lucro medio do pedido')
    pedluctotpor = models.FloatField(db_column='PedLucTotPor', blank=True, null=True,
                                     db_comment='lucro total do pedido em porcentagem (o valor total do pedido / pelo valor de custo total do pedido)')
    pedluctotrea = models.FloatField(db_column='PedLucTotRea', blank=True, null=True,
                                     db_comment='lucro total do pedido em valor')
    pedvlrtotprevendeprocomcus = models.FloatField(db_column='PedVlrTotPreVenDeProComCus', blank=True, null=True,
                                                   db_comment='valor total de preco de venda de produto com custo - inclui somente os produtos que tem o custo cadastrado')
    pedvlrtotliqprecovenprocomcus = models.FloatField(db_column='PedVlrTotLiqPrecoVenProComCus', blank=True, null=True,
                                                      db_comment='valor total liquido do preco de venda de produtos que possui o custo cadastrado')
    pedvlrtotprecusdeprocomcus = models.FloatField(db_column='PedVlrTotPreCusDeProComCus', blank=True, null=True,
                                                   db_comment='valor total de preco de custo de produtos com custo - inclui somente os produtos que tem o custo cadastrado')
    peddatlib = models.DateField(db_column='PedDatLib', blank=True, null=True, db_comment='data de liberaþao do pedido')
    pedbloqueado = models.CharField(db_column='PedBloqueado', max_length=3, blank=True, null=True,
                                    db_comment='Se o pedido esta bloqueado ou nao esta bloqueado - tem que desbloquear para o fernando poder liberar')
    peddesblpor = models.CharField(db_column='PedDesblPor', max_length=50, blank=True, null=True,
                                   db_comment='usuario que desbloqueou o pedido')
    pedrebloqueado = models.CharField(db_column='PedRebloqueado', max_length=3, blank=True, null=True,
                                      db_comment='se o fernando rebloquear o pedido, nao aceitar o desbloqueio que a tatiane fez')
    pedinspor = models.CharField(db_column='PedInsPor', max_length=50, blank=True, null=True,
                                 db_comment='Usuario que inserio o pedido')
    pedaltpor = models.CharField(db_column='PedAltPor', max_length=50, blank=True, null=True,
                                 db_comment='usuario que alterou o pedido')
    pedcancelpor = models.CharField(db_column='PedCancelPor', max_length=50, blank=True, null=True,
                                    db_comment='quem cancelou o pedido')
    pedcancelmot = models.TextField(db_column='PedCanCelMot', blank=True, null=True,
                                    db_comment='motivo da qual o pedido foi cancelado')
    pedsistema = models.CharField(db_column='PedSistema', max_length=50, blank=True, null=True,
                                  db_comment='sistema usado para criar o pedido - DESKTOP ou WEB')
    pedsistemaenviado = models.CharField(db_column='PedSistemaEnviado', max_length=255, blank=True, null=True,
                                         db_comment='sistema usado para enviar o  pedido - DESKTOP ou WEB')
    pedjaenvumavez = models.CharField(db_column='PedJaEnvUmaVez', max_length=3, blank=True, null=True,
                                      db_comment='salva SIM quando o pedido for enviado pela primeira vez, uma vez alterado ele nunca mais Ú alterado (usada para saber se o pedido esta sendo alterado ou se esta sendo digitado pela primeira vez)')
    pedcomreppor = models.FloatField(db_column='PedComRepPor', blank=True, null=True,
                                     db_comment='valor porcentual da comissao que sera para o representantante referente a este pedido')
    pedidempexp = models.IntegerField(db_column='PedIdEmpExp',
                                      db_comment='Codigo da empresa que o pedido sera exportado')
    rotina_gera_com_rep = models.CharField(db_column='rotina_gera_com_rep',
                                          max_length=50, db_comment='Flag que indica se a rotina que gera comissão já verificou o pedido',
                                          default='N')

    class Meta:
        managed = False
        db_table = 'ped01'


class Ped02(models.Model):
    ped2id = models.AutoField(db_column='Ped2Id', primary_key=True)
    uuid = models.CharField(max_length=255, blank=True, null=True)
    pedido = models.ForeignKey(Ped01, models.DO_NOTHING, db_column='Ped2Cod', related_name='itens')
    ped2itm = models.IntegerField(db_column='Ped2Itm', blank=True, null=True)
    ped2procod = models.IntegerField(db_column='Ped2ProCod', blank=True, null=True)
    ped2pronom = models.CharField(db_column='Ped2ProNom', max_length=300, blank=True, null=True)
    ped2proart = models.CharField(db_column='Ped2ProArt', max_length=20, blank=True, null=True)
    ped2protam = models.CharField(db_column='Ped2ProTam', max_length=20, blank=True, null=True)
    ped2univen = models.CharField(db_column='Ped2UniVen', max_length=10, blank=True, null=True)
    ped2fur = models.CharField(db_column='Ped2Fur', max_length=20, blank=True, null=True)
    ped2aca = models.CharField(db_column='Ped2Aca', max_length=20, blank=True, null=True)
    ped2opccor = models.CharField(db_column='Ped2OpcCor', max_length=20, blank=True, null=True)
    ped2cor = models.CharField(db_column='Ped2Cor', max_length=20, blank=True, null=True)
    ped2embcod = models.IntegerField(db_column='Ped2EmbCod', blank=True, null=True)
    ped2emb = models.CharField(db_column='Ped2Emb', max_length=50, blank=True, null=True)
    ped2emb2 = models.CharField(db_column='Ped2Emb2', max_length=50, blank=True, null=True)
    ped2qtditm = models.IntegerField(db_column='Ped2QtdItm', blank=True, null=True)
    ped2valuni = models.FloatField(db_column='Ped2ValUni', blank=True, null=True)
    ped2valtotitm = models.FloatField(db_column='Ped2ValTotItm', blank=True, null=True)
    ped2obsitm = models.CharField(db_column='Ped2ObsItm', max_length=30, blank=True, null=True)
    ped2personalizado = models.CharField(db_column='Ped2Personalizado', max_length=3, blank=True, null=True)
    ped2tipolaser = models.CharField(db_column='Ped2TipoLaser', max_length=20)
    ped2fontpersonal = models.CharField(db_column='Ped2FontPersonal', max_length=50, blank=True, null=True,
                                        db_comment='tipo da font - NORNAL, COLORIDA')
    ped2valpersonalizacao = models.FloatField(db_column='Ped2ValPersonalizacao', blank=True, null=True)
    ped2proartreal = models.CharField(db_column='Ped2ProArtReal', max_length=20, blank=True, null=True,
                                      db_comment='Artigo real quando o botao for personalizado ')
    ped2precocusto = models.FloatField(db_column='Ped2PrecoCusto', blank=True, null=True,
                                       db_comment='Preco de custo do item incluindo a personalizacao')
    ped2pormarluc = models.FloatField(db_column='Ped2PorMarLuc', blank=True, null=True,
                                      db_comment='Margem de lucro em porcentagem do produto incluindo a personalizacao')
    ped2gravacao = models.CharField(db_column='Ped2Gravacao', max_length=50, blank=True, null=True,
                                    db_comment='gravacao que ira ser personalizada no botao')
    ped2gravobs = models.CharField(db_column='Ped2GravObs', max_length=50, blank=True, null=True,
                                   db_comment='observacao da personalizacao')
    ped2prcvenda = models.FloatField(db_column='Ped2PrcVenda', blank=True, null=True,
                                     db_comment='preco do artigo na lista de preco')
    ped2prcvendido = models.FloatField(db_column='Ped2PrcVendido', blank=True, null=True,
                                       db_comment='Preco que foi vendido o botao (sem considerar a personalizacao, somente o botao)')
    ped2descreal = models.FloatField(db_column='Ped2DescReal', blank=True, null=True,
                                     db_comment='valor do desconto dado no artigo')
    ped2descpor = models.FloatField(db_column='Ped2DescPor', blank=True, null=True,
                                    db_comment='porcentagem de desconto dado no artigo')
    ped2prccustoprosemperso = models.FloatField(db_column='Ped2PrcCustoProSemPerso', blank=True, null=True,
                                                db_comment='preco de custo sem incluir a personalizacao, se o botao for personalizo, esse eh o custo somente do botao')
    ped2pormarlucprosemperso = models.FloatField(db_column='Ped2PorMarLucProSemPerso', blank=True, null=True,
                                                 db_comment='porcentual de lucro do produto sem incluir a personalizacao, somente do produto mesmo')

    class Meta:
        managed = False
        db_table = 'ped02'
        unique_together = (
            ('pedido', 'ped2proart', 'ped2protam', 'ped2fur', 'ped2aca', 'ped2opccor', 'ped2cor', 'ped2emb2',
             'ped2personalizado', 'ped2tipolaser'),)


class Ped03(models.Model):
    ped3id = models.AutoField(db_column='Ped3Id', primary_key=True)
    pedido = models.ForeignKey(Ped01, models.DO_NOTHING, db_column='Ped3Cod', related_name='parcelas')
    ped3nroparc = models.PositiveIntegerField(db_column='Ped3NroParc', blank=True, null=True)
    ped3parc = models.PositiveIntegerField(db_column='Ped3Parc', blank=True, null=True)
    ped3qtddiasvenc = models.IntegerField(db_column='Ped3QtdDiasVenc', blank=True, null=True)
    ped3datvenc = models.DateTimeField(db_column='Ped3DatVenc', blank=True, null=True)
    ped3valparc = models.FloatField(db_column='Ped3ValParc', blank=True, null=True)
    ped3formpagto = models.CharField(db_column='Ped3FormPagto', max_length=45, blank=True, null=True)
    ped3condpagto = models.CharField(db_column='Ped3CondPagto', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ped03'


class Ped04(models.Model):
    id = models.AutoField(primary_key=True)  # Chave primária para o Django
    pedido = models.ForeignKey(Ped01, models.DO_NOTHING, db_column='Ped4Cod', related_name='anexos')
    representante = models.ForeignKey(Representante, models.DO_NOTHING, db_column='Ped4RepCod',
                                      related_name='anexos_pedidos')
    ped4itm = models.IntegerField(db_column='Ped4Itm')
    ped4pathanexo = models.CharField(db_column='Ped4PathAnexo', max_length=500)
    ped4arqanexo = models.CharField(db_column='Ped4ArqAnexo', max_length=100)
    ped4msganexo = models.CharField(db_column='Ped4MsgAnexo', max_length=500)
    ped4copemarep = models.CharField(db_column='Ped4CopEmaRep', max_length=5,
                                     db_comment='envia copia do email para o representante')

    class Meta:
        managed = False
        db_table = 'ped04'
        unique_together = (('pedido', 'ped4itm', 'representante'),)


# ==============================================================================
# Modelo de Log de Comissão - CORRIGIDO
# ==============================================================================

class ComLogPedRepCli(models.Model):
    id = models.AutoField(primary_key=True)
    # --- Relacionamento Corrigido ---
    pedido = models.ForeignKey(
        Ped01,
        on_delete=models.CASCADE,
        db_column='pedidocod',
        related_name='logs_comissao'
    )
    representante_principal = models.ForeignKey(Representante, on_delete=models.RESTRICT,
                                                related_name='logs_como_principal')
    representante_subordinado = models.ForeignKey(Representante, on_delete=models.SET_NULL,
                                                  related_name='logs_como_subordinado', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, db_column='clicod')
    data_pedido = models.DateField()

    def __str__(self):
        return f"Log do Pedido {self.pedido.pedcod}"

    class Meta:
        managed = False
        db_table = 'com_log_ped_rep_cli'
        verbose_name = 'Log de Vínculo de Representantes'
        verbose_name_plural = 'Logs de Vínculos de Representantes'

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
    clicod = models.IntegerField(unique=True, verbose_name='Código do Cliente')
    clinom = models.CharField(max_length=100, blank=True, null=True)
    dias_max_sem_visita = models.IntegerField(default=60)
    percentual_comissao = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        # A representação em string agora usa o nome ou o código do cliente.
        return f"Configuração Específica para {self.clinom or f'Cliente Cód: {self.clicod}'}"

    class Meta:
        managed = False
        db_table = 'com_cli_esp'
        verbose_name = 'Configuração de Comissão por Cliente'
        verbose_name_plural = 'Configurações de Comissão por Cliente'


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