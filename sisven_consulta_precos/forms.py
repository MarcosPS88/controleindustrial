from django import forms

MOEDA_CHOICES = (
    ('real', 'Real (R$)'),
    ('dolar', 'Dólar (US$)'),
)

class PrecoSearchForm(forms.Form):
    artigo = forms.CharField(
        label='Código do Artigo',
        max_length=20,
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 12345'})
    )
    tamanho = forms.CharField(
        label='Tamanho',
        max_length=10,
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 24'})
    )
    moeda = forms.ChoiceField(
        label='Moeda',
        choices=MOEDA_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )