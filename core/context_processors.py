def menu_processor(request):
    """
    Este processador de contexto define qual menu será exibido na barra lateral
    de forma ACUMULATIVA, com base nos grupos do usuário logado.
    """
    menu_itens = []

    if not request.user.is_authenticated:
        return {'menu_principal': menu_itens}

    grupos_usuario = set(request.user.groups.values_list('name', flat=True))

    # --- MENU PARA USUÁRIOS DO SISVEN (Permissões de Consulta) ---
    if 'Sisven Usuarios' in grupos_usuario:
        menu_consultas = [
            {
                'id': 'consultasSubmenu', 'label': 'Consultas', 'icon': 'fa-search',
                'sub_itens': [
                    {'url_name': 'sisven_consulta_precos:consulta', 'label': 'Consultar Preços'},
                ]
            },
        ]
        menu_itens.extend(menu_consultas)

    # --- MENU PARA USUÁRIOS DO SISVEN (ADMINISTRATIVO) ---
    if 'Sisven Admin' in grupos_usuario:
        menu_admin = [
            {
                'id': 'gerenciamentoSubmenu', 'label': 'Gerenciamento', 'icon': 'fa-users-cog',
                'sub_itens': [
                    {'url_name': 'sisven_users:usuario_list', 'label': 'Usuários'},
                    {'url_name': 'sisven_users:representante_list', 'label': 'Representantes'},
                ]
            },

             {
                'id': 'comissoesSubmenu', 'label': 'Configurar Comissões', 'icon': 'fa-percent',
                'sub_itens': [
                    {'url_name': 'sisven_conf_comissoes:com_rep_sub_list', 'label': 'Por Representante'},
                    {'url_name': 'sisven_conf_comissoes:com_cli_esp_list', 'label': 'Por Cliente'},
                ]
            },
        ]
        menu_itens.extend(menu_admin)

    # --- MENU PARA REPRESENTANTES DO SISVEN ---
    if 'Sisven Representantes' in grupos_usuario:
        menu_representante = [
            {
                'id': 'pedidosRepSubmenu', 'label': 'Pedidos', 'icon': 'fa-shopping-cart',
                'sub_itens': [
                    # {'url_name': 'vendas:novo_pedido', 'label': 'Digitar Pedido'},
                ]
            },
            {
                'id': 'catalogoRepSubmenu', 'label': 'Catálogo', 'icon': 'fa-book-open',
                'sub_itens': [
                    {'url_name': 'sisven_consulta_precos:consulta', 'label': 'Consultar Preços de Venda'},
                ]
            },
            {
                'id': 'financeiroRepSubmenu', 'label': 'Financeiro', 'icon': 'fa-file-invoice-dollar',
                'sub_itens': [
                    # {'url_name': 'financeiro:titulos_aberto', 'label': 'Títulos em Aberto'},
                ]
            },
        ]
        menu_itens.extend(menu_representante)
    
    # --- MENU PARA O CONTROLE DE PRODUÇÃO ---
    if 'Producao' in grupos_usuario or 'PCP' in grupos_usuario:
        menu_producao = [
            {
                'id': 'fichaTecnicaSubmenu', 'label': 'Ficha Técnica', 'icon': 'fa-clipboard-list',
                'sub_itens': [
                    {'url_name': 'ibgcontrole:artigo_list', 'label': 'Artigo'},
                    {'url_name': 'ibgcontrole:amostra_list', 'label': 'Amostra'},
                    {'url_name': 'ibgcontrole:cor_list', 'label': 'Cor'},
                    {'url_name': 'ibgcontrole:ficha_tecnica_list', 'label': 'Ficha Técnica'},
                ]
            },
            {
                'id': 'ferramentariaSubmenu', 'label': 'Ferramentaria', 'icon': 'fa-tools',
                'sub_itens': [
                    {'url_name': 'ibgcontrole:peca_list', 'label': 'Peça'},
                    {'url_name': 'ibgcontrole:ferramenta_list', 'label': 'Ferramenta'},
                    {'url_name': 'ibgcontrole:emprestimo_list', 'label': 'Empréstimo'},
                    {'url_name': 'ibgcontrole:ordemproducaoferramenta_list', 'label': 'Produção Ferramenta'},
                    {'url_name': 'ibgcontrole:ordemproducaoamostra_list', 'label': 'Produção Amostra'},
                ]
            },
            {
                'id': 'organizacaoSubmenu', 'label': 'Organização', 'icon': 'fa-boxes',
                'sub_itens': [
                    {'url_name': 'ibgcontrole:conteiner_list', 'label': 'Contêiner'},
                    {'url_name': 'ibgcontrole:tipoconteiner_list', 'label': 'Tipo Contêiner'},
                    {'url_name': 'ibgcontrole:itemestocado_search', 'label': 'Itens Estocados'},
                ]
            },
            {
                'id': 'relatoriosSubmenu', 'label': 'Relatórios', 'icon': 'fa-chart-pie',
                'sub_itens': [
                    {'url_name': 'ibgcontrole:relatorio_producao_ferramenta', 'label': 'Produção Ferramenta'},
                    {'url_name': 'ibgcontrole:relatorio_programacao_pcp', 'label': 'Programação PCP'},
                    {'url_name': 'ibgcontrole:relatorio_producao_amostra', 'label': 'Produção Amostras'},
                    {'url_name': 'ibgcontrole:relatorio_oda', 'label': 'Produção Mostruário'},
                ]
            },
            {
                'id': 'pcpSubmenu', 'label': 'PCP', 'icon': 'fa-calendar-alt',
                'sub_itens': [
                    {'url_name': 'producao:pcp_conferencia', 'label': 'Conf. Ped/Ops'},
                    {'url_name': 'producao:pcp_list_ordem_producao', 'label': 'Controle OPs'},
                    {'url_name': 'producao:pcp_list_ordem_producao_finan', 'label': 'Controle OPs Fin'},
                    {'url_name': 'ibgcontrole:programacao_pcp_list', 'label': 'Imp. Planilha Prog'},
                    {'url_name': 'producao:importar_ops_view', 'label': 'Imp. OPs em massa'},
                    {'url_name': 'producao:importar_op_individual', 'label': 'Imp. OPs individual'},
                ]
            },
            {
                'id': 'mostruarioSubmenu', 'label': 'Mostruário', 'icon': 'fa-swatchbook',
                'sub_itens': [
                    {'url_name': 'ibgcontrole:oda_list', 'label': 'Produção Mostruário'},
                ]
            },
            {
                'id': 'quimicaSubmenu', 'label': 'Química', 'icon': 'fa-flask',
                'sub_itens': [
                    {'url_name': 'producao:lista_ops_quimica', 'label': 'Lista OPs'},
                    {'url_name': 'producao:painel_quimica', 'label': 'Painel Agr. Fórmulas'},
                    {'url_name': 'producao:lancamento-painel-selecao', 'label': 'Painel Lanc. Cil. Ops'},
                ]
            },
            {
                'id': 'pastilhasSubmenu', 'label': 'Pastilhas', 'icon': 'fa-circle',
                'sub_itens': [
                    {'url_name': 'producao:lista_ops_pastilha', 'label': 'Apont. Pastilhas'},
                ]
            },
            {
                'id': 'tornoLaserSubmenu', 'label': 'Torno/Laser', 'icon': 'fa-compact-disc',
                'sub_itens': [
                    {'url_name': 'producao:lista_ops_torno', 'label': 'Lista OPs Torno'},
                    {'url_name': 'producao:lista_ops_laser', 'label': 'Lista OPs Laser'},
                    {'url_name': 'producao:lista_ops_kanban', 'label': 'Lista OPs Kanban'},
                    {'url_name': 'producao:kanban_estoque_painel', 'label': 'Estoque Kanban'},
                ]
            },
            {
                'id': 'polimentoSubmenu', 'label': 'Polimento', 'icon': 'fa-gem',
                'sub_itens': [
                    {'url_name': 'producao:lista_ops_polimento', 'label': 'Lista OPs Polimento'},
                ]
            },
            {
                'id': 'tingimentoSubmenu', 'label': 'Tingimento', 'icon': 'fa-palette',
                'sub_itens': [
                    {'url_name': 'producao:lista_ops_tingimento', 'label': 'Fila de Tingimento'},
                ]
            },
            {
                'id': 'escolhaFinalSubmenu', 'label': 'Escolha Final', 'icon': 'fa-check-double',
                'sub_itens': [
                    {'url_name': 'producao:lista_ops_conferencia', 'label': 'Fila de Conferência'},
                    {'url_name': 'producao:lista_ops_controle_qualidade', 'label': 'Fila C. Qualidade'},
                ]
            },
            {
                'id': 'embalagemExpedicaoSubmenu', 'label': 'Embalagem e Expedição', 'icon': 'fa-box-open',
                'sub_itens': [
                    {'url_name': 'producao:lista_ops_contagem', 'label': 'Fila de Contagem'},
                    {'url_name': 'producao:fila_embalagem', 'label': 'Fila de Embalagem'},
                    {'url_name': 'producao:fila_expedicao', 'label': 'Fila de Expedição'},
                ]
            },
        ]
        menu_itens.extend(menu_producao)

    return {'menu_principal': menu_itens}