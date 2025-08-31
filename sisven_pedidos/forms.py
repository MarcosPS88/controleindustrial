from django import forms
from sisven_core.models import Representante


class ComLogForm(forms.Form):
    """
    Formulário para registrar o vínculo de um representante subordinado a um pedido.
    (Atualizado sem atributos HTMX)
    """
    pedido = forms.IntegerField(
        label="Número do Pedido",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Digite o nº do pedido e aguarde...',
            'id': 'id_pedido',  # Garante um ID consistente para o JavaScript
        })
    )

    representante_subordinado = forms.ModelChoiceField(
        label="Representante Subordinado (que receberá a comissão)",
        queryset=Representante.objects.filter(status='ATIVO').exclude(rep_tipo='TELEVENDAS').order_by('nome'),
        empty_label="Selecione um representante",
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define o campo como não obrigatório inicialmente,
        # pois a validação real depende do pedido existir.
        self.fields['representante_subordinado'].required = False
