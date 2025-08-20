from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name  = 'core'

urlpatterns = [
    path('', view=IndexView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='core/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]