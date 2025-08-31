from django.urls import path
from .views import ComLogCreateView, BuscarPedidoView

app_name = 'sisven_pedidos'

urlpatterns = [
    # URL da página principal do formulário
    path('comissao/log/novo/', ComLogCreateView.as_view(), name='comlog_create'),

    # URL da API interna para busca de pedidos (agora usando CBV)
    path('api/buscar-pedido/', BuscarPedidoView.as_view(), name='buscar_pedido'),
]