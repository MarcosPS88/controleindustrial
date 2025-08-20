# sisven_conf_comissoes/views.py

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from sisven_core.models import ComRepSub, ComCliEsp
from .forms import ComRepSubForm, ComCliEspForm

from sisven_core.auth_mixins import SisvenAdminRequiredMixin 

# --- Views para Configuração de Comissão por Representante ---

class ComRepSubListView(SisvenAdminRequiredMixin, ListView):
    model = ComRepSub
    template_name = 'sisven_conf_comissoes/com_rep_sub_list.html'
    context_object_name = 'configs'
    paginate_by = 20

    def get_queryset(self):
        queryset = ComRepSub.objects.select_related('representante').order_by('representante__nome')
        search_name = self.request.GET.get('search_name', None)
        if search_name:
            queryset = queryset.filter(representante__nome__icontains=search_name)
        return queryset

class ComRepSubCreateView(SisvenAdminRequiredMixin, CreateView):
    model = ComRepSub
    form_class = ComRepSubForm
    template_name = 'sisven_conf_comissoes/com_form.html'
    success_url = reverse_lazy('sisven_conf_comissoes:com_rep_sub_list')

    def form_valid(self, form):
        # Preenche os campos repcod e repnom automaticamente antes de salvar
        config = form.save(commit=False)
        config.repcod = config.representante.codigo
        # config.repnom = config.representante.nome # Descomente se tiver este campo no modelo
        config.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nova Configuração por Representante'
        context['list_url'] = reverse_lazy('sisven_conf_comissoes:com_rep_sub_list')
        return context

class ComRepSubUpdateView(SisvenAdminRequiredMixin, UpdateView):
    model = ComRepSub
    form_class = ComRepSubForm
    template_name = 'sisven_conf_comissoes/com_form.html'
    success_url = reverse_lazy('sisven_conf_comissoes:com_rep_sub_list')

    def form_valid(self, form):
        config = form.save(commit=False)
        config.repcod = config.representante.codigo
        # config.repnom = config.representante.nome # Descomente se tiver este campo no modelo
        config.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editando Configuração: {self.object.representante.nome}'
        context['list_url'] = reverse_lazy('sisven_conf_comissoes:com_rep_sub_list')
        return context

class ComRepSubDeleteView(SisvenAdminRequiredMixin, DeleteView):
    model = ComRepSub
    template_name = 'sisven_conf_comissoes/com_confirm_delete.html'
    success_url = reverse_lazy('sisven_conf_comissoes:com_rep_sub_list')
    context_object_name = 'config'


# --- Views para Configuração de Comissão por Cliente ---

class ComCliEspListView(SisvenAdminRequiredMixin, ListView):
    model = ComCliEsp
    template_name = 'sisven_conf_comissoes/com_cli_esp_list.html'
    context_object_name = 'configs'
    paginate_by = 20

    def get_queryset(self):
        queryset = ComCliEsp.objects.select_related('cliente').order_by('cliente__clinom')
        search_name = self.request.GET.get('search_name', None)
        if search_name:
            queryset = queryset.filter(cliente__clinom__icontains=search_name)
        return queryset

class ComCliEspCreateView(SisvenAdminRequiredMixin, CreateView):
    model = ComCliEsp
    form_class = ComCliEspForm
    template_name = 'sisven_conf_comissoes/com_form.html'
    success_url = reverse_lazy('sisven_conf_comissoes:com_cli_esp_list')

    def form_valid(self, form):
        config = form.save(commit=False)
        config.clinom = config.cliente.clinom
        config.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nova Configuração por Cliente'
        context['list_url'] = reverse_lazy('sisven_conf_comissoes:com_cli_esp_list')
        return context

class ComCliEspUpdateView(SisvenAdminRequiredMixin, UpdateView):
    model = ComCliEsp
    form_class = ComCliEspForm
    template_name = 'sisven_conf_comissoes/com_form.html'
    success_url = reverse_lazy('sisven_conf_comissoes:com_cli_esp_list')

    def form_valid(self, form):
        config = form.save(commit=False)
        config.clinom = config.cliente.clinom
        config.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editando Configuração: {self.object.cliente.clinom}'
        context['list_url'] = reverse_lazy('sisven_conf_comissoes:com_cli_esp_list')
        return context

class ComCliEspDeleteView(SisvenAdminRequiredMixin, DeleteView):
    model = ComCliEsp
    template_name = 'sisven_conf_comissoes/com_confirm_delete.html'
    success_url = reverse_lazy('sisven_conf_comissoes:com_cli_esp_list')
    context_object_name = 'config'
