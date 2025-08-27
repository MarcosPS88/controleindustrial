# core/auth_mixins.py

from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy

class SisvenVendasRequiredMixin(AccessMixin):
    """
    Mixin de segurança para o portal Sisven Vendas.

    Verifica se o usuário está logado e pertence ao grupo 'Sisven Representantes'.
    Se não estiver logado, redireciona para a tela de login de vendas.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Se não estiver logado, chama o método que redireciona para o login
            return self.handle_no_permission()
        
        # Se estiver logado, verifica se pertence ao grupo correto
        if not request.user.groups.filter(name='Sisven Representantes').exists():
            # Se não pertencer, nega o acesso (resultará em um erro 403 Forbidden)
            return self.handle_no_permission()
            
        return super().dispatch(request, *args, **kwargs)

    def get_login_url(self):
        """Define para qual URL de login redirecionar."""
        return reverse_lazy('login_sisven_vendas')


class SisvenAdminRequiredMixin(AccessMixin):
    """
    Mixin de segurança para o portal Sisven Admin.

    Verifica se o usuário está logado e pertence ao grupo 'Sisven Admin'.
    Se não estiver logado, redireciona para a tela de login de admin.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if not request.user.groups.filter(name='Sisven Admin').exists():
            return self.handle_no_permission()
            
        return super().dispatch(request, *args, **kwargs)

    def get_login_url(self):
        return reverse_lazy('login_sisven_admin')


class ControleIBGRequiredMixin(AccessMixin):
    """
    Mixin de segurança para o portal Controle IBG.

    Verifica se o usuário está logado e pertence aos grupos 'Producao' ou 'PCP'.
    Se não estiver logado, redireciona para a tela de login do IBG.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        grupos_permitidos = {'Producao', 'PCP'}
        if not request.user.groups.filter(name__in=grupos_permitidos).exists():
            return self.handle_no_permission()
            
        return super().dispatch(request, *args, **kwargs)

    def get_login_url(self):
        return reverse_lazy('login_ibg')
    

