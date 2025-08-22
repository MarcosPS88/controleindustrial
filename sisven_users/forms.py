# sisven_users/forms.py

from django import forms
from sisven_core.models import Usuario, Representante

CHOICES_SIM_NAO = (
     
    ('N', 'Não'),
    ('S', 'Sim'),
)

CHOICES_STATUS = (
    ('', 'Todos'),
    ('ATIVO', 'Ativo'),
    ('INATIVO', 'Inativo'),
)

# Atributos comuns para os widgets para evitar repetição
WIDGET_ATTRS = {'class': 'form-select form-select-sm'}

class UsuarioForm(forms.ModelForm):
    # --- Declaração Explícita para garantir o tipo e as opções ---
    # Usamos required=False para campos que podem ser nulos ou em branco no modelo
    
    senha = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control form-control-sm'}), required=False)
    status = forms.ChoiceField(choices=CHOICES_STATUS, widget=forms.Select(attrs=WIDGET_ATTRS), required=False)

    # Permissões
    liberar_pedidos = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    exportar_pedidos_liberados = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    # ... (todos os outros campos de permissão declarados explicitamente)
    desbloquear_pedidos = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    alterar_pedidos_liberados = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    alterar_previsao_entrega = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    alterar_info_financeira_pedido = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    importar_pedidos_franquiados = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    digitar_orcamento = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_pedidos = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_pedidos_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_pedidos_representante = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_ultima_compra_artigo = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_titulos_aberto = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    mudar_cliente_provisorio = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    alterar_senha = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_titulos = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    ver_margem_lucro = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    configurar_grade_custo = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_grade_custo = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    adicionar_parametros_botao = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    alterar_parametros_botao = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    cadastrar_cod_gravacao = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_preco_custo = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_posicao_pedidos = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    grafico_ranking_vendas = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    grafico_vendas_representante = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    grafico_ranking_clientes = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    alterar_celular_sms_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    enviar_sms_pedido_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    enviar_sms_representante = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_pedidos_emitidos_ibg = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    ver_valores_faturados = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    cadastrar_lista_preco = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    gerar_lista_preco = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    imprimir_lista_preco = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_dados_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_cod_personalizado = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    politica_vendas = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_preco_venda = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    aceitar_arroba_50 = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_drp = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_serasa = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    cadastrar_comissao = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    excecao_comissao_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    cadastrar_obs_fixa_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    cadastrar_madeiras = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    grade_custo_botao_madeira = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    rendimento_pastilha_madeira = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    parametro_artigo_madeira = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    alterar_dados_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    excecao_comissao_pedido = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    controle_oda = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    apontamento_final_oda = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    imprimir_apontamento_final_oda = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    apontamento_itens_oda_producao = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    imprimir_oda_producao_prazo = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    posicao_odas = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    limite_credito = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_limite_credito = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    liberar_cliente_provisorio = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    historico_vendas_artigo = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    espelho_nota_fiscal = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_pedidos_on_time = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    gerir_relacionamento_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    historico_conversas_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    criar_grupos_clientes = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_grupos_clientes = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    gerenciar_clientes_grupos = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    alterar_representante_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            for field_name, field in self.fields.items():
                if isinstance(field, forms.ChoiceField) and field_name != 'status':
                    field.initial = 'N'

    class Meta:
        model = Usuario
        fields = '__all__'
        exclude = ['usrempcod', 'usrema', 'usrsenema']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'login': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email_pessoal': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'celular_sms': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

class RepresentanteForm(forms.ModelForm):
    # --- Declaração Explícita ---
    senha = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control form-control-sm'}), required=False)
    status = forms.ChoiceField(choices=CHOICES_STATUS, widget=forms.Select(attrs=WIDGET_ATTRS), required=False)
    
    # Permissões
    digitar_pedidos = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    cancelar_pedidos = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_pedidos_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_pedidos_data = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    historico_compras_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    historico_vendas_artigo = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    ver_titulos_aberto = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    enviar_pedido_email_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    alterar_senha = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_titulos = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    posicao_pedidos = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    grafico_vendas_representante = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    ranking_clientes = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    relatorio_titulos_baixados = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    alterar_celular_sms_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    enviar_sms_pedido_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    imprimir_lista_preco = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_dados_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_cod_personalizado = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_preco_venda = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    aceitar_arroba_50 = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    alterar_dados_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    gerenciar_oda = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    imprimir_oda_prazo = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    imprimir_oda_virou_pedido = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    apontar_oda_producao = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    espelho_nota_fiscal = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    gerir_relacionamento_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    historico_conversas_cliente = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))
    consultar_grupos_clientes = forms.ChoiceField(choices=CHOICES_SIM_NAO, widget=forms.Select(attrs=WIDGET_ATTRS))

    def __init__(self, *args, **kwargs):
        super(RepresentanteForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            for field_name, field in self.fields.items():
                if isinstance(field, forms.ChoiceField) and field_name != 'status':
                    field.initial = 'N'

    class Meta:
        model = Representante
        fields = '__all__'
        # CORREÇÃO: Exclui todos os campos que não devem ser editados pelo usuário
        exclude = ['repempcod', 'repema', 'repemasen', 'lis1internacionalcod']
        widgets = {
            'codigo': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'login': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'nome': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email_pessoal': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'celular': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'codigo_lista_preco': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'reptipven': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
        }

class UsuarioFilterForm(forms.Form):
    """Formulário para filtrar a lista de Usuários."""
    search_name = forms.CharField(
        label='Nome do Usuário',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pesquisar por nome...'
        })
    )
    status = forms.ChoiceField(
        label='Status',
        choices=CHOICES_STATUS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class RepresentanteFilterForm(forms.Form):
    """Formulário para filtrar a lista de Representantes."""
    search_name = forms.CharField(
        label='Nome do Representante',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pesquisar por nome...'
        })
    )
    status = forms.ChoiceField(
        label='Status',
        choices=CHOICES_STATUS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )