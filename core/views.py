from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin # Adicionado
from django.views.generic import TemplateView
from django.urls import reverse_lazy

# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/base_templates/index.html'
    login_url = reverse_lazy('core:login') # Adicionado
    redirect_field_name = 'next' # Adicionado (opcional, mas bom ter),