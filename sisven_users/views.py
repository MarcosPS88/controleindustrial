# sisven_users/views.py

from sisven_core.auth_mixins import SisvenAdminRequiredMixin# <-- Importe aqui

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from sisven_core.models import Usuario, Representante
from .forms import UsuarioForm, RepresentanteForm

# --- Views para Usuários ---

class UsuarioListView(SisvenAdminRequiredMixin, ListView):
    model = Usuario
    template_name = 'sisven_users/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 20

    def get_queryset(self):
        # O router direcionará esta leitura para o banco 'sisven' automaticamente
        queryset = Usuario.objects.order_by('nome')
        search_name = self.request.GET.get('search_name', None)

        if search_name:
            queryset = queryset.filter(nome__icontains=search_name)
            
        return queryset

class UsuarioCreateView(SisvenAdminRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'sisven_users/usuario_form.html'
    success_url = reverse_lazy('sisven_users:usuario_list')

    def form_valid(self, form):
        # A forma padrão e correta. O router direcionará o form.save()
        # para o banco de dados 'sisven' automaticamente.
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastro de Novo Usuário'
        return context

class UsuarioUpdateView(SisvenAdminRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'sisven_users/usuario_form.html'
    success_url = reverse_lazy('sisven_users:usuario_list')

    def get_queryset(self):
        # Garante que estamos buscando o objeto do banco de dados correto para editar
        return Usuario.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editando Usuário: {self.object.nome}'
        return context

# --- Views para Representantes ---

class RepresentanteListView(SisvenAdminRequiredMixin, ListView):
    model = Representante
    template_name = 'sisven_users/representante_list.html'
    context_object_name = 'representantes'
    paginate_by = 20

    def get_queryset(self):
        queryset = Representante.objects.order_by('nome')
        search_name = self.request.GET.get('search_name', None)

        if search_name:
            queryset = queryset.filter(nome__icontains=search_name)
            
        return queryset

class RepresentanteCreateView(SisvenAdminRequiredMixin, CreateView):
    model = Representante
    form_class = RepresentanteForm
    template_name = 'sisven_users/representante_form.html'
    success_url = reverse_lazy('sisven_users:representante_list')

    def form_valid(self, form):
        print("\n--- DIAGNÓSTICO: Entrou em RepresentanteCreateView.form_valid ---")
        print("O formulário foi considerado válido pela verificação inicial.")
        
        # Imprime os dados limpos que serão enviados ao banco
        print("\n[DEBUG] Dados do formulário (form.cleaned_data):")
        print(form.cleaned_data)
        
        try:
            print("\n[DEBUG] Tentando salvar o objeto no banco de dados...")
            # A chamada super().form_valid(form) executa o form.save()
            response = super().form_valid(form)
            print(f"[SUCESSO] Objeto salvo com sucesso! ID: {self.object.pk}")
            print(f"[DEBUG] Redirecionando para: {response.url}")
            return response
        except Exception as e:
            # Se ocorrer qualquer erro durante o save, ele será capturado e impresso aqui
            print(f"\n!!!!!!!!!! ERRO AO SALVAR NO BANCO DE DADOS !!!!!!!!!!")
            print(f"Exceção: {e}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            form.add_error(None, f"Ocorreu um erro inesperado ao salvar: {e}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("\n--- DIAGNÓSTICO: Entrou em RepresentanteCreateView.form_invalid ---")
        print("O formulário foi considerado INVÁLIDO.")
        print("\n[DEBUG] Erros do formulário (form.errors):")
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastro de Novo Representante'
        return context

class RepresentanteUpdateView(SisvenAdminRequiredMixin, UpdateView):
    model = Representante
    form_class = RepresentanteForm
    template_name = 'sisven_users/representante_form.html'
    success_url = reverse_lazy('sisven_users:representante_list')

    def get_queryset(self):
        return Representante.objects.all()

    def form_valid(self, form):
        print(f"\n--- DIAGNÓSTICO: Entrou em RepresentanteUpdateView.form_valid para o objeto ID: {self.object.pk} ---")
        print("O formulário foi considerado válido.")
        
        print("\n[DEBUG] Dados do formulário (form.cleaned_data):")
        print(form.cleaned_data)

        try:
            print("\n[DEBUG] Tentando salvar as alterações no banco de dados...")
            response = super().form_valid(form)
            print(f"[SUCESSO] Alterações salvas com sucesso para o objeto ID: {self.object.pk}")
            print(f"[DEBUG] Redirecionando para: {response.url}")
            return response
        except Exception as e:
            print(f"\n!!!!!!!!!! ERRO AO ATUALIZAR NO BANCO DE DADOS !!!!!!!!!!")
            print(f"Exceção: {e}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            form.add_error(None, f"Ocorreu um erro inesperado ao atualizar: {e}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        print(f"\n--- DIAGNÓSTICO: Entrou em RepresentanteUpdateView.form_invalid para o objeto ID: {self.object.pk} ---")
        print("O formulário foi considerado INVÁLIDO.")
        print("\n[DEBUG] Erros do formulário (form.errors):")
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editando Representante: {self.object.nome}'
        return context