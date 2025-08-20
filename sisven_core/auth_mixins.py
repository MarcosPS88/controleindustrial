from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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