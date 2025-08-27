# core/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class SisvenAdminAuthenticationForm(AuthenticationForm):
    """
    Formulário de autenticação personalizado para o portal Sisven Admin.
    Verifica se o usuário pertence aos grupos 'Sisven Admin' ou 'Sisven Usuarios'.
    """
    def confirm_login_allowed(self, user):
        # Chama a implementação original primeiro (verifica se a conta está ativa, etc.)
        super().confirm_login_allowed(user)

        # Nossa verificação personalizada de grupo
        user_groups = set(user.groups.values_list('name', flat=True))
        allowed_groups = {'Sisven Admin', 'Sisven Usuarios'}
        
        # Se não houver interseção entre os grupos do usuário e os grupos permitidos, falha.
        if not user_groups.intersection(allowed_groups):
            raise ValidationError(
                "Usuário ou senha inválida.", # Mensagem genérica por segurança
                code='invalid_login',
            )

class SisvenVendasAuthenticationForm(AuthenticationForm):
    """
    Formulário de autenticação personalizado para o portal Sisven Vendas.
    Verifica se o usuário pertence ao grupo 'Sisven Representantes'.
    """
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        
        if not user.groups.filter(name='Sisven Representantes').exists():
            raise ValidationError(
                "Usuário ou senha inválida.",
                code='invalid_login',
            )

class IbgAuthenticationForm(AuthenticationForm):
    """
    Formulário de autenticação personalizado para o portal Controle IBG.
    Verifica se o usuário pertence aos grupos 'Producao' ou 'PCP'.
    """
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        
        user_groups = set(user.groups.values_list('name', flat=True))
        allowed_groups = {'Producao', 'PCP'}

        if not user_groups.intersection(allowed_groups):
            raise ValidationError(
                "Usuário ou senha inválida.",
                code='invalid_login',
            )
