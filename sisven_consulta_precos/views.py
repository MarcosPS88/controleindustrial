from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from sisven_core.models import ListaPrecoItem
from .forms import PrecoSearchForm
from sisven_core.auth_mixins import ContextualSisvenAccessMixin
from django.shortcuts import render
from django.views import View
from django.db.models import Q




class ConsultaPrecoView(ContextualSisvenAccessMixin, ListView):
    template_name = 'sisven_consulta_precos/lista_precos.html'
    model = ListaPrecoItem
    paginate_by = 20
    context_object_name = 'itens_preco'

    def get_queryset(self):

        form = PrecoSearchForm(self.request.GET)

        if not form.is_valid() or not form.cleaned_data.get('artigo') and not form.cleaned_data.get('tamanho'):
            return self.model.objects.none()

        artigo = form.cleaned_data.get('artigo')
        tamanho = form.cleaned_data.get('tamanho')
        moeda = form.cleaned_data.get('moeda', 'real') # Padrão para 'real' se não for fornecido

        # Mapeamento de moeda para o código da lista de preço
        codigo_lista_map = {'real': 2, 'dolar': 3}
        codigo_lista = codigo_lista_map.get(moeda, 2) # Usa 2 (Real) como padrão

        # Constrói os filtros dinamicamente
        filters = Q(lista_preco_codigo=codigo_lista)
        if artigo:
            filters &= Q(artigo__icontains=artigo)
        if tamanho:
            filters &= Q(tamanho__icontains=tamanho)

        return self.model.objects.using('sisven').filter(filters).order_by('artigo', 'tamanho')

    def get_context_data(self, **kwargs):
        """
        Adiciona dados extras ao contexto para serem usados no template.
        """
        # Chama a implementação base primeiro para obter o contexto
        context = super().get_context_data(**kwargs)

        # 1. Adiciona o formulário de busca ao contexto
        # Instancia com request.GET para que os campos permaneçam preenchidos após a busca
        context['form'] = PrecoSearchForm(self.request.GET or None)

        # 2. Adiciona o símbolo da moeda ao contexto
        moeda_selecionada = self.request.GET.get('moeda', 'real')
        context['simbolo_moeda'] = 'US$' if moeda_selecionada == 'dolar' else 'R$'

        # 3. VERIFICAÇÃO DE PERMISSÃO: Adiciona a flag para o grupo 'gerencia'
        # O template usará esta variável para decidir se mostra a coluna de custo.
        if self.request.user.is_authenticated:
            context['usuario_e_gerencia'] = self.request.user.groups.filter(name='Sisven Gerencia').exists()
        else:
            context['usuario_e_gerencia'] = False
        print(f'Usuario é gerencia: {context["usuario_e_gerencia"]}')
        print(f'Usuario é gerencia: {self.request.user.groups}')
            
        return context

class ConsultaRendimentoView(ContextualSisvenAccessMixin, View):
    """
    Esta view lida com a consulta de rendimentos de materiais,
    usando dados definidos diretamente no código.
    """
    template_name = 'sisven_consulta_precos/consulta_rendimento.html'

    # --- DADOS DEFINIDOS DIRETAMENTE NO CÓDIGO ---

    # Dados para Plaquinha, Botão Poliéster e Botão Madeira
    DADOS_BOTAO = [
        {'tamanho': 14, 'quantidade': 123.00}, {'tamanho': 16, 'quantidade': 95.00},
        {'tamanho': 18, 'quantidade': 76.00}, {'tamanho': 20, 'quantidade': 61.00},
        {'tamanho': 22, 'quantidade': 51.00}, {'tamanho': 24, 'quantidade': 43.00},
        {'tamanho': 26, 'quantidade': 35.00}, {'tamanho': 28, 'quantidade': 31.00},
        {'tamanho': 30, 'quantidade': 27.00}, {'tamanho': 32, 'quantidade': 24.00},
        {'tamanho': 34, 'quantidade': 20.00}, {'tamanho': 36, 'quantidade': 18.00},
        {'tamanho': 40, 'quantidade': 15.00}, {'tamanho': 45, 'quantidade': 12.00},
        {'tamanho': 48, 'quantidade': 9.00}, {'tamanho': 54, 'quantidade': 8.00},
        {'tamanho': 60, 'quantidade': 7.00}, {'tamanho': 64, 'quantidade': 6.00},
        {'tamanho': 72, 'quantidade': 5.00},
    ]

    # Dados para Fivela
    DADOS_FIVELA = [
        {'tamanho': '2CM', 'quantidade': 9}, {'tamanho': '4CM', 'quantidade': 3},
        {'tamanho': '3CM', 'quantidade': 5}, {'tamanho': '5CM', 'quantidade': 2},
    ]

    # Dados para Bastão (mesmos tamanhos dos botões, quantidade fixa)
    DADOS_BASTAO = [
        {'tamanho': item['tamanho'], 'quantidade': 200} for item in DADOS_BOTAO
    ]

    # Mapeamento das escolhas para os dados correspondentes
    ESCOLHAS_MAP = {
        'plaquinha': ('Plaquinha', DADOS_BOTAO, "grosas"),
        'botao_poliester': ('Botão Poliéster', DADOS_BOTAO, "grosas"),
        'botao_madeira': ('Botão Madeira', DADOS_BOTAO, "grosas"),
        'fivela': ('Fivela', DADOS_FIVELA, "grosas"),
        'bastao': ('Bastão', DADOS_BASTAO, "grosas"),
    }

    def get(self, request, *args, **kwargs):
        context = {
            'opcoes': {key: val[0] for key, val in self.ESCOLHAS_MAP.items()}
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        escolha_key = request.POST.get('material')
        context = {
            'opcoes': {key: val[0] for key, val in self.ESCOLHAS_MAP.items()},
            'escolha_selecionada': escolha_key,
        }

        if escolha_key in self.ESCOLHAS_MAP:
            titulo, dados, unidade = self.ESCOLHAS_MAP[escolha_key]
            context['titulo_tabela'] = f"Rendimento para: {titulo}"
            context['cabecalhos'] = ["Tamanho", f"Quantidade Mínima ({unidade})"]
            context['resultados'] = dados

        return render(request, self.template_name, context)
    