from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from sisven_core.models import ListaPrecoItem
from .forms import PrecoSearchForm


class ConsultaPrecoView(LoginRequiredMixin, ListView):
    template_name = 'sisven_consulta_precos/lista_precos.html'
    model = ListaPrecoItem
    paginate_by = 20
    context_object_name = 'itens_preco' # Nome mais claro para a lista no template

    def get_queryset(self):
        # Inicia com um queryset vazio. A busca só ocorre se o formulário for válido.
        queryset = self.model.objects.none() 
        
        form = PrecoSearchForm(self.request.GET)
        if form.is_valid():
            artigo = form.cleaned_data.get('artigo')
            tamanho = form.cleaned_data.get('tamanho')
            moeda = form.cleaned_data.get('moeda')

            # O código da lista de preço é definido pela moeda selecionada
            # 2 = Real, 3 = Dólar (conforme sua lógica original)
            codigo_lista = 2 if moeda == 'real' else 3

            # A busca só é executada se pelo menos um campo (artigo ou tamanho) for preenchido
            if artigo or tamanho:
                # O filtro foi atualizado para usar o novo campo 'lista_preco_codigo'
                # que definimos como chave primária no modelo.
                filters = {'lista_preco_codigo': codigo_lista}
                
                if artigo:
                    filters['artigo__icontains'] = artigo
                if tamanho:
                    # --- CORREÇÃO DO ERRO ---
                    # Alterado de 'iexact' para 'icontains' para ser mais flexível
                    # com possíveis espaços em branco no banco de dados legado.
                    filters['tamanho__icontains'] = tamanho
                
                # Aplica os filtros e ordena
                queryset = self.model.objects.using('sisven').filter(**filters).order_by('artigo', 'tamanho')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa o formulário (preenchido ou não) para o template
        context['form'] = PrecoSearchForm(self.request.GET or None)
        
        # Define o símbolo da moeda para exibição na tabela de resultados
        moeda_selecionada = self.request.GET.get('moeda')
        if moeda_selecionada == 'dolar':
            context['simbolo_moeda'] = 'US$'
        else:
            # O padrão é Real
            context['simbolo_moeda'] = 'R$'
            
        return context
