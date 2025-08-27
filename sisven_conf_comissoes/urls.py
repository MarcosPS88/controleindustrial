from django.urls import path
from . import views

app_name = 'sisven_conf_comissoes'

urlpatterns = [
    # URLs para Configuração por Representante
    path('configuracao/representantes/', views.ComRepSubListView.as_view(), name='com_rep_sub_list'),
    path('configuracao/representantes/novo/', views.ComRepSubCreateView.as_view(), name='com_rep_sub_create'),
    path('configuracao/representantes/editar/<int:pk>/', views.ComRepSubUpdateView.as_view(), name='com_rep_sub_update'),
    path('configuracao/representantes/apagar/<int:pk>/', views.ComRepSubDeleteView.as_view(), name='com_rep_sub_delete'),

    # URLs para Configuração por Cliente
    path('configuracao/clientes/', views.ComCliEspListView.as_view(), name='com_cli_esp_list'),
    path('configuracao/clientes/novo/', views.ComCliEspCreateView.as_view(), name='com_cli_esp_create'),
    path('configuracao/clientes/editar/<int:pk>/', views.ComCliEspUpdateView.as_view(), name='com_cli_esp_update'),
    path('configuracao/clientes/apagar/<int:pk>/', views.ComCliEspDeleteView.as_view(), name='com_cli_esp_delete'),
]
