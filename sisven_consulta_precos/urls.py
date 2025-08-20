from django.urls import path
from .views import ConsultaPrecoView

app_name = 'sisven_consulta_precos'

urlpatterns = [
    path('consulta-precos/', ConsultaPrecoView.as_view(), name='consulta'),
]