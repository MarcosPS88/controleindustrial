from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views as core_views
from core.forms import SisvenVendasAuthenticationForm, SisvenAdminAuthenticationForm, IbgAuthenticationForm


urlpatterns = [
    # A rota do admin continua a mesma
    path('admin/', admin.site.urls),

    # --- ROTAS DE AUTENTICAÇÃO E LOGOUT (NOVA SEÇÃO) ---
    # Em vez de uma URL de login, agora temos três, uma para cada sistema.
    # Cada uma aponta para um template e redireciona para um dashboard específico.
    
    path('sisven-vendas/login', auth_views.LoginView.as_view(
        template_name='core/registration/login_sisven_vendas.html',
        authentication_form=SisvenVendasAuthenticationForm,
        next_page='home_vendas' 
    ), name='login_sisven_vendas'),
    
    path('sisven-admin/login/', auth_views.LoginView.as_view(
        template_name='core/registration/login_sisven_admin.html',
        authentication_form=SisvenAdminAuthenticationForm,
        next_page='home_admin'
    ), name='login_sisven_admin'),

    path('controle-ibg/login/', auth_views.LoginView.as_view(
        template_name='core/registration/login_ibg.html',
        authentication_form=IbgAuthenticationForm,
        next_page='home_ibg'
    ), name='login_ibg'),

    #  URL de logout agora aponta para nossa view customizada e inteligente
    path('logout/', core_views.CustomLogoutView.as_view(), name='logout'),

    # --- ROTEAMENTO PARA OS SISTEMAS PRINCIPAIS (NOVA SEÇÃO) ---
    # Esta é a mudança principal: removemos os 'includes' da raiz e os
    # agrupamos sob prefixos de URL claros.
    
    path('sisven-admin/', include('sisven_core.urls_admin')),
    path('sisven-vendas/', include('sisven_core.urls_vendas')),
   # path('controle-ibg/', include('core.urls_controle_ibg')),
    

    # --- ROTAS DAS PÁGINAS INICIAIS (DASHBOARDS) (NOVA SEÇÃO) ---
    # Rotas para as novas páginas iniciais de cada sistema
        
]

# A configuração de arquivos estáticos e de mídia continua a mesma,
# mas é uma boa prática colocá-la dentro de uma verificação de DEBUG.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)