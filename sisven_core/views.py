from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect
from django.urls import reverse

from core.auth_mixins import SisvenVendasRequiredMixin, SisvenAdminRequiredMixin


class HomeVendasView(SisvenVendasRequiredMixin, TemplateView):
    """
    View para a página inicial do portal Sisven Vendas.
    """
    template_name = 'sisven_core/base_templates/home_vendas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_sistema'] = 'Sistema de Vendas'
        return context

class HomeAdminView(SisvenAdminRequiredMixin, TemplateView):
    """
    View para a página inicial  do portal Sisven Admin.
    """
    template_name = 'sisven_core/base_templates/home_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_sistema'] = 'Sistema de Vendas Administração'
        return context