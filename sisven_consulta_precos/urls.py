from django.urls import path
from .views import ConsultaPrecoView, ConsultaRendimentoView

app_name = 'sisven_consulta_precos'

urlpatterns = [
    path('consulta-preco/', ConsultaPrecoView.as_view(), name='consulta'),
    path('consulta-rendimento/', ConsultaRendimentoView.as_view(), name='consulta_rendimento_vendas'),
]