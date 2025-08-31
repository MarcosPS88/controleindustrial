from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ProducaoPCPRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='PCP').exists()

class ProducaoTornosRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='Tornos').exists()

class ProducaoLaserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='Laser').exists()

class ProducaoKanbanRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='Kanban').exists()

class ProducaoQuimicaRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='Quimica').exists()

class ProducaoPastilhasRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='Pastilhas').exists()

class ProducaoPolimentoRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='Kanban').exists()

class ProducaoTingimentoRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='Kanban').exists()

class ProducaoEscolhaFinalRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='Escolha Final').exists()
    
class ProducaoEmbalagemRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Garante que o usuário pertence ao grupo correto para acessar estas views
        return self.request.user.groups.filter(name='Embalagem').exists()