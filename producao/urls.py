from django.urls import path
from . import views

app_name = 'producao'



urlpatterns = [
    # Views de Importação
    path('producao/importar/', views.ImportarOpsView.as_view(), name='importar_ops_view'),
    path('producao/importar-individual/', views.ImportarOpIndividualView.as_view(), name='importar_op_individual'),

    # Views de Lista e Detalhes do PCP
    path('pcp/ordens/', views.PcpListOrdemProducaoView.as_view(), name='pcp_list_ordem_producao'),
    path('pcp/ordens-financeiro/', views.PcpListOrdemProducaoFinanView.as_view(), name='pcp_list_ordem_producao_finan'),
    path('pcp/pedido/<str:numero_pedido>/detalhes/', views.DetalhesPedidoView.as_view(), name='pcp_detalhes_pedido'),
    path('pcp/ordem-producao/<int:pk>/editar/', views.OrdemProducaoPCPUpdateView.as_view(), name='ordem_producao_pcp_editar'),
    
    # Views das Conferencias do PCP
    # URL para quando um pedido específico é selecionado para conferência
    path('pcp/conferencia/<str:numero_pedido>/', views.PainelConferenciaPCPView.as_view(), name='pcp_conferencia_detalhe'),
    # URL para a página principal de conferência (mostra apenas a lista)
    path('pcp/conferencia/', views.PainelConferenciaPCPView.as_view(), name='pcp_conferencia'),
    
    # Views de Filas de Produção e Apontamentos
    path('producao/quimica/', views.ListaOpsQuimicaView.as_view(), name='lista_ops_quimica'),
    path('producao/quimica/<int:op_id>/', views.ApontamentoQuimicaView.as_view(), name='apontamento_quimica'),
    path('producao/pastilha/', views.ListaOpsPastilhaView.as_view(), name='lista_ops_pastilha'),
    path('producao/pastilha/<int:op_id>/apontar/', views.ApontamentoPastilhaView.as_view(), name='apontamento_pastilha'),

    # Paineis e Ações da Química (já estavam em CBV)
    path('producao/painel-quimica/', views.PainelQuimicaView.as_view(), name='painel_quimica'),
    path('lote-quimico/gerar/<int:formula_id>/', views.GerarLoteQuimicoView.as_view(), name='gerar_lote_quimico'),
    path('lote-quimico/produzir/<int:formula_id>/', views.MarcarLoteProduzidoView.as_view(), name='marcar_lote_produzido'),
    path('producao/receita-agrupada/<int:formula_id>/<str:data_programacao>/', views.ReceitaAgrupadaView.as_view(), name='receita_agrupada_quimica'),
    path('lancamento/selecao/', views.PainelSelecaoOPLancamentoView.as_view(), name='lancamento-painel-selecao'),
    path('lancamento/apontamento/<int:agrupamento_pk>/', views.ApontamentoLancamentoAgrupadoView.as_view(), name='lancamento-apontamento-agrupado'),
    path('op/<int:op_pk>/finalizar-quimica/', views.FinalizarOPQuimicaView.as_view(), name='op-finalizar-quimica'),
    path('kanban/solicitacao/<int:solicitacao_pk>/atender/', views.AtenderDemandaKanbanView.as_view(), name='atender_demanda_kanban'),
    path('op/<int:op_pk>/receita/', views.ReceitaOPView.as_view(), name='ver_receita_op'),
    path('lote/<int:lote_id>/cancelar/', views.CancelarLoteQuimicoView.as_view(), name='cancelar_lote_quimico'),
    path('retrabalho/<int:reprogramacao_pk>/iniciar/', views.IniciarRetrabalhoView.as_view(), name='iniciar_retrabalho_quimica'),
    path('corte/fila/', views.ListaOpsAguardandoCorteView.as_view(), name='lista_ops_aguardando_corte'),


    #Reprogramação
    path('op/<int:op_pk>/criar-retrabalho/', views.CriarRetrabalhoPastilhaView.as_view(), name='op-criar-retrabalho-pastilha'),

    # -- Apontamento Torno/Laser/Kanban
    #path('setor/<str:setor>/', views.ListaOpsTornoLaserKanbanView.as_view(), name='lista_ops_torno_laser_kanban'),
    path('lista-ops/tornos/', views.ListaOpsTornoLaserView.as_view(), {'setor': 'tornos'}, name='lista_ops_torno'),
    path('lista-ops/laser/', views.ListaOpsTornoLaserView.as_view(), {'setor': 'laser'}, name='lista_ops_laser'),
    path('setor/<str:setor>/op/<int:op_id>/apontar/', views.ApontamentoTornoLaserKanbanView.as_view(), name='apontamento_torno_laser_kanban'),
    path('kanban/op/<int:op_pk>/solicitar-quimica/', views.SolicitarQuimicaKanbanView.as_view(), name='kanban_solicitar_quimica'),
    path('lista-ops/kanban/', views.ListaOpsKanbanView.as_view(), name='lista_ops_kanban'),
    path('lista-ops/<str:setor>/', views.ListaOpsTornoLaserView.as_view(), name='lista_ops_torno_laser'),


    # -- Controle de Estoque Kanban
    path('kanban/estoque/', views.PainelEstoqueKanbanView.as_view(), name='kanban_estoque_painel'),
    path('kanban/estoque/solicitar/', views.CriarSolicitacaoReposicaoView.as_view(), name='kanban_criar_solicitacao'),
    path('kanban/reposicao/<int:solicitacao_pk>/liberar-para-cilindro/', views.LiberarReposicaoParaCilindroView.as_view(), name='kanban_liberar_para_cilindro'),
    path('kanban/reposicao/<int:solicitacao_pk>/apontamento/', views.ApontamentoReposicaoKanbanView.as_view(), name='kanban_apontamento_reposicao'),
    path('lancamento/kanban/confirmar-corte/<int:solicitacao_pk>/', views.ConfirmarCorteReposicaoKanbanView.as_view(), name='kanban_confirmar_corte'),
    path('kanban/apontamento-pastilha/<int:solicitacao_pk>/', views.ApontamentoPastilhaKanbanView.as_view(), name='kanban_apontamento_pastilha'),

    # --- URLs para o Setor de Polimento ---
    path('polimento/fila/', views.ListaOpsPolimentoView.as_view(), name='lista_ops_polimento'),
    path('polimento/apontamento/novo/', views.ApontamentoPolimentoView.as_view(), name='apontamento_polimento_novo'),
    path('polimento/apontamento/<int:apontamento_id>/', views.ApontamentoPolimentoView.as_view(), name='apontamento_polimento'),

    # - Detalhes da Ordem de Produção
    path('op/<int:op_id>/detalhes/', views.OrdemProducaoDetailView.as_view(), name='detalhes_op'),

    # - Escolha Final
    path('escolha-final/', views.ListaOpsConferenciaView.as_view(), name='lista_ops_conferencia'),
    path('escolha-final/apontamento/<int:item_id>/', views.ApontamentoConferenciaView.as_view(), name='apontamento_conferencia'),
    path('controle-qualidade/', views.ListaOpsControleQualidadeView.as_view(), name='lista_ops_controle_qualidade'),
    path('apontamento-cq/<int:item_id>/', views.ApontamentoControleQualidadeView.as_view(), name='apontamento_controle_qualidade'),

    #- Contagem Final
    path('contagem/lista/', views.ListaOpsContagemView.as_view(), name='lista_ops_contagem'),
    path('contagem/apontamento/<int:item_id>/<path:setor_origem>/', views.ApontamentoContagemView.as_view(), name='apontamento_contagem'),

    # - Tingimento
    path('tingimento/lista/', views.ListaOpsTingimentoView.as_view(), name='lista_ops_tingimento'), 
    path('tingimento/apontamento/<int:lote_id>/', views.ApontamentoTingimentoView.as_view(), name='apontamento_tingimento'),

    # - Embalagem
    # --- FILA DE EMBALAGEM (LISTA DE CLIENTES) ---
    path('embalagem/fila/', views.FilaEmbalagemView.as_view(), name='fila_embalagem'),

    # --- PAINEL DE APONTAMENTO DE UM CLIENTE ESPECÍFICO ---
    path('embalagem/cliente/<int:cliente_id>/', views.ApontamentoClienteEmbalagemView.as_view(), name='apontamento_cliente_embalagem'),

    # --- AÇÕES DENTRO DO PAINEL DE EMBALAGEM ---
    path('embalagem/cliente/<int:cliente_id>/abrir-caixa/', views.AbrirCaixaView.as_view(), name='abrir_caixa'),
    path('embalagem/adicionar-item/', views.AdicionarItemACaixaView.as_view(), name='adicionar_item_caixa'),
    path('embalagem/caixa/<int:caixa_id>/fechar/', views.FecharCaixaView.as_view(), name='fechar_caixa'),

    # --- FILA DE EXPEDIÇÃO (LISTA DE CLIENTES COM CAIXAS FECHADAS) ---
    path('expedicao/fila/', views.FilaExpedicaoView.as_view(), name='fila_expedicao'),

    # --- PAINEL DE CONFERÊNCIA DE UM CLIENTE ESPECÍFICO ---
    path('expedicao/cliente/<int:cliente_id>/', views.DetalheClienteExpedicaoView.as_view(), name='detalhe_cliente_expedicao'),

    # --- AÇÃO DE CONFERIR UMA CAIXA ---
    path('expedicao/caixa/<int:caixa_id>/conferir/', views.ConferenciaCaixaView.as_view(), name='conferencia_caixa'),

]

