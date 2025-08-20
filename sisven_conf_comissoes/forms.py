from django import forms
from sisven_core.models import (ComRepSub, 
                                ComCliEsp, 
                                Cliente,
                                Representante
                                )

class ComRepSubForm(forms.ModelForm):
    # Campo para selecionar o representante de uma lista.
    representante = forms.ModelChoiceField(
        queryset=Representante.objects.order_by('nome'),
        label="Representante",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = ComRepSub
        # O campo 'repcod' será preenchido automaticamente na view.
        fields = ['representante', 'dias_max_sem_visita', 'percentual_comissao']
        labels = {
            'dias_max_sem_visita': 'Dias Máximos sem Visita',
            'percentual_comissao': 'Percentual de Comissão (%)',
        }
        widgets = {
            'dias_max_sem_visita': forms.NumberInput(attrs={'class': 'form-control'}),
            'percentual_comissao': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class ComCliEspForm(forms.ModelForm):
    # NOTA: Para uma lista grande de clientes, o ideal é usar um widget de autocomplete.
    # Para começar, um ModelChoiceField funciona.
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.order_by('clinom'),
        label="Cliente",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = ComCliEsp
        # O campo 'clinom' será preenchido automaticamente na view.
        fields = ['cliente', 'dias_max_sem_visita', 'percentual_comissao']
        labels = {
            'dias_max_sem_visita': 'Dias Máximos sem Visita',
            'percentual_comissao': 'Percentual de Comissão (%)',
        }
        widgets = {
            'dias_max_sem_visita': forms.NumberInput(attrs={'class': 'form-control'}),
            'percentual_comissao': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
