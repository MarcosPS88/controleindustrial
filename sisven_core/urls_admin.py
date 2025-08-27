# sisven_core/urls_admin.py

from django.urls import path, include
from .views import HomeAdminView



# Este arquivo centraliza todas as URLs relacionadas ao sistema "Sisven Admin".
# Ele funciona como um roteador secundário, recebendo o tráfego do urls.py principal
# e direcionando para o app correto dentro deste sistema.


urlpatterns = [

    path('home/', HomeAdminView.as_view(), name='home_admin'),
    path('usuarios/', include('sisven_users.urls')),
    path('comissoes/', include('sisven_conf_comissoes.urls')),
    path('precos/', include('sisven_consulta_precos.urls', namespace='admin-precos')),


]
