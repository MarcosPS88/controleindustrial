from django import forms
from sisven_core.models import (ComRepSub,
                                ComCliEsp,
                                Cliente,
                                Representante
                                )
from acedata_core.models import (Ter01)
from django.core.exceptions import ValidationError

class ComRepSubForm(forms.ModelForm):
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
    # Campo para selecionar o cliente do banco de dados ACEDATA.
    cliente_selecionado = forms.ModelChoiceField(
        queryset=Ter01.objects.filter(tersta='ATIVO', tercli='S').order_by('ternom'),
        label="Cliente (Busca em Acedata)",
        widget=forms.Select(attrs={'class': 'form-select'}),
        to_field_name="terdoc",
        help_text="Selecione o cliente do banco de dados Acedata."
    )

    class Meta:
        model = ComCliEsp
        # Os campos 'clicod' e 'clinom' serão preenchidos no método save().
        fields = ['dias_max_sem_visita', 'percentual_comissao']
        labels = {
            'dias_max_sem_visita': 'Dias Máximos sem Visita',
            'percentual_comissao': 'Percentual de Comissão (%)',
        }
        widgets = {
            'dias_max_sem_visita': forms.NumberInput(attrs={'class': 'form-control'}),
            'percentual_comissao': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se for uma instância existente (edição), preenche o campo de seleção
        if self.instance and self.instance.pk:
            try:
                # CORREÇÃO: Usa 'self.instance.clicod' para buscar o cliente
                ter01_cliente = Ter01.objects.get(terdoc=self.instance.clicod)
                self.fields['cliente_selecionado'].initial = ter01_cliente
            except Ter01.DoesNotExist:
                pass

    def clean_cliente_selecionado(self):
        # Validação para evitar duplicatas de configuração.
        cliente_acedata = self.cleaned_data.get('cliente_selecionado')
        if cliente_acedata:
            # CORREÇÃO: Usa 'clicod' para verificar se a configuração já existe.
            config_exists = ComCliEsp.objects.filter(clicod=cliente_acedata.terdoc).exists()

            # self.instance.pk é None durante a criação
            if not self.instance.pk and config_exists:
                raise ValidationError(
                    "Já existe uma configuração de comissão para este cliente."
                )
        return cliente_acedata

    def save(self, commit=True):
        # Pega o cliente selecionado do banco Acedata
        cliente_acedata = self.cleaned_data.get('cliente_selecionado')

        # --- CORREÇÃO PRINCIPAL ---
        # Atribui o código e o nome do cliente diretamente aos campos da instância.
        self.instance.clicod = cliente_acedata.terdoc
        self.instance.clinom = cliente_acedata.ternom

        # Chama o método save() original do ModelForm para salvar no banco.
        return super().save(commit)
