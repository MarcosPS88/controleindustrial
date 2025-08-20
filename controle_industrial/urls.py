"""
URL configuration for controle_industrial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    #path('', include('ibgcontrole.urls')),
    #path('', include('producao.urls')),
    path('', include('sisven_users.urls')),
    path('', include('sisven_consulta_precos.urls')),
    path('', include('sisven_conf_comissoes.urls')),
    # --- URLs DE AUTENTICAÇÃO ---
    # Usamos as views prontas do Django, apontando para nosso template customizado.
    
    # 1. URL da Página de Login
    path('login/', auth_views.LoginView.as_view(template_name='core/registration/login.html'), name='login'),

    # 2. URL de Logout (também pronta)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
