from django.urls import path
from . import views

app_name = 'sisven_users'

urlpatterns = [
    # URLs de Usuários
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/novo/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/editar/<int:pk>/', views.UsuarioUpdateView.as_view(), name='usuario_update'),

    # URLs de Representantes
    path('representantes/', views.RepresentanteListView.as_view(), name='representante_list'),
    path('representantes/novo/', views.RepresentanteCreateView.as_view(), name='representante_create'),
    path('representantes/editar/<int:pk>/', views.RepresentanteUpdateView.as_view(), name='representante_update'),
]