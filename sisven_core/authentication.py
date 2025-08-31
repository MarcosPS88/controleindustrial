from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User, Group
from .models import Usuario, Representante


class SisvenAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        db_legado = 'sisven'

        # Tenta encontrar um Representante primeiro
        try:
            rep = Representante.objects.using(db_legado).get(login=username)

            # Verificação de senha em texto puro.
            if rep.senha == password:
                # Usa update_or_create para criar o usuário ou atualizar seus dados a cada login
                user, created = User.objects.update_or_create(
                    username=rep.login,  # O username no Django será o mesmo do login do representante
                    defaults={
                        'first_name': rep.nome,
                        'last_name': str(rep.codigo)  # Converte o código para string
                    }
                )

                # Se o usuário foi criado agora, adiciona ao grupo correto
                if created:
                    group, _ = Group.objects.get_or_create(name='Sisven Representantes')
                    user.groups.add(group)
                return user
        except Representante.DoesNotExist:
            pass

            # Tenta encontrar um Usuário do sistema
        try:
            usr = Usuario.objects.using(db_legado).get(login=username)

            if usr.senha == password:
                # Mesma lógica de update_or_create para usuários
                user, created = User.objects.update_or_create(
                    username=usr.login,
                    defaults={
                        'first_name': usr.nome,
                    }
                )
                if created:
                    group, _ = Group.objects.get_or_create(name='Sisven Usuarios')
                    user.groups.add(group)
                return user
        except Usuario.DoesNotExist:
            return None

        return None  # Senha incorreta

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None