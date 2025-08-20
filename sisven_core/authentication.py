from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User, Group
from .models import Usuario, Representante

class SisvenAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        db_legado = 'sisven'

        # Tenta encontrar um Representante primeiro
        try:
            # CORREÇÃO: Adicionado .using(db_legado) para forçar a consulta no banco correto.
            rep = Representante.objects.using(db_legado).get(login=username)
            
            # ATENÇÃO: Verificação de senha em texto puro.
            if rep.senha == password:
                # Usamos um prefixo para evitar conflito de usernames no banco do Django
                user, created = User.objects.get_or_create(username=f"rep_{username}")
                if created:
                    # Garante que o grupo existe antes de tentar adicioná-lo
                    group, _ = Group.objects.get_or_create(name='Sisven Representantes')
                    user.groups.add(group)
                return user
        except Representante.DoesNotExist:
            pass # Se não for representante, continua para tentar como usuário

        # Tenta encontrar um Usuário do sistema
        try:
            # CORREÇÃO: Adicionado .using(db_legado) para forçar a consulta no banco correto.
            usr = Usuario.objects.using(db_legado).get(login=username)

            if usr.senha == password:
                user, created = User.objects.get_or_create(username=f"usr_{username}")
                if created:
                    group, _ = Group.objects.get_or_create(name='Sisven Usuarios')
                    user.groups.add(group)
                return user
        except Usuario.DoesNotExist:
            return None # Usuário não encontrado em nenhuma das tabelas
        
        return None # Senha incorreta

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None