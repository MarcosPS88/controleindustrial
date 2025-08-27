# sisven_core/urls_vendas.py

from django.urls import path, include
from .views import HomeVendasView
# Este arquivo centraliza todas as URLs relacionadas ao sistema "Sisven Vendas".
# Ele agrupa todos os apps que os representantes utilizarão.

urlpatterns = [
    path('home/', HomeVendasView.as_view(), name='home_vendas'),
    path('precos/', include('sisven_consulta_precos.urls', namespace='vendas-precos')),
    path('precos/', include('sisven_consulta_precos.urls', namespace='vendas-rendimento')),

   
]
