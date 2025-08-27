# core/urls_controle_ibg.py

from django.urls import path, include
from .views import HomeIBGView

# Este arquivo centraliza todas as URLs relacionadas ao sistema "Controle IBG".


urlpatterns = [
    path('home/', HomeIBGView.as_view(), name='home_ibg'),
    # Inclui as URLs do app de produção sob o prefixo 'controle-fluxo/'
    # Ex: /controle-ibg/controle-fluxo/pcp/ordens/
    path('controle-fluxo/', include('producao.urls')),

    # Inclui as URLs do app de controle industrial sob o prefixo 'controle-industria/'
    # Ex: /controle-ibg/controle-industria/artigos/
    path('controle-industria/', include('ibgcontrole.urls')),
]
