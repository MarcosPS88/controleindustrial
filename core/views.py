# core/views.py

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


# Importe os mixins que acabamos de criar
# ATENÇÃO: Se você renomeou o arquivo para auth_mixins.py, o import deve refletir isso.
from .auth_mixins import ControleIBGRequiredMixin



class HomeIBGView(ControleIBGRequiredMixin, TemplateView):
    """
    View para a página inicial (dashboard) do portal Controle IBG.
    """
    template_name = 'core/base_templates/home_ibg.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_sistema'] = 'Controle de Fluxo de Produção IBG'
        return context


class CustomLogoutView(BaseLogoutView):
    """
    View de Logout customizada que redireciona o usuário para a tela de login
    do sistema em que ele estava navegando.
    """
    def get_success_url(self):
        """
        CORREÇÃO: Sobrescrevemos get_success_url para alinhar com o traceback.
        Este método é chamado após o logout para decidir para onde redirecionar.
        """
        # Pega a URL da página em que o usuário estava antes de clicar em "Sair"
        referer_url = self.request.META.get('HTTP_REFERER')

        if referer_url:
            if '/sisven-vendas/' in referer_url:
                return reverse_lazy('login_sisven_vendas')
            elif '/sisven-admin/' in referer_url:
                return reverse_lazy('login_sisven_admin')
            elif '/controle-ibg/' in referer_url:
                return reverse_lazy('login_ibg')
        
        # Se não conseguir identificar a origem, redireciona para um login padrão.
        return reverse_lazy('login_ibg')

