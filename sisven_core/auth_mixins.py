from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import AccessMixin

from django.urls import reverse_lazy

class SisvenAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='Sisven Admin').exists()

class SisvenUsuariosRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='Sisven Usuarios').exists()

class SisvenRepresentantesRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='Sisven Representantes').exists()
    

class ContextualSisvenAccessMixin(AccessMixin):
    """
    Mixin que concede acesso com base no contexto da URL.
    - Se a URL for de admin, exige o grupo de admin.
    - Se a URL for de vendas, exige o grupo de representante.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Lógica para redirecionar para o login correto
            if request.path.startswith('/sisven-admin/'):
                self.login_url = reverse_lazy('login_sisven_admin')
            else:
                self.login_url = reverse_lazy('login_sisven_vendas')
            return self.handle_no_permission()

        # Verifica a permissão com base na URL
        if request.path.startswith('/sisven-admin/'):
            if not request.user.groups.filter(name='Sisven Admin').exists():
                return self.handle_no_permission() # Nega acesso
        
        elif request.path.startswith('/sisven-vendas/'):
            if not request.user.groups.filter(name='Sisven Representantes').exists():
                return self.handle_no_permission() # Nega acesso
        
        else:
            # Se a URL não corresponder a nenhum padrão, nega por segurança
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
