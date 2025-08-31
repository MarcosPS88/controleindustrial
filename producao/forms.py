# Se o arquivo não existir, crie-o.
from django import forms
from .models import( 
    OrdemProducao,
    ControlePastilha, 
    Setor,
    MotivoReprogramacao,
    ReprogramacaoOP,
    Maquina,
    ControleProducaoTornoLaser,
    SolicitacaoQuimicaKanban,
    Parada,
    Operador,
    ParadaLancamentoAgrupado,
    ContribuicaoOP,
    LancamentoCilindro,
    SolicitacaoReposicaoKanban,
    ItemEstoqueKanban,
    ControlePolimento,
    ParadaPolimento,
    ItemPolimento,
    SaldoOPSetor,
    ConferenciaEscolhaFinal,
    ControleQualidadeEsteira,
    ContagemFinal,
    LancamentoTingimento,
    ItemTingimento,
    ParadaTingimento,
    CargaLancamentoTingimento,
    ApontamentoEmbalagem,
    Caixa,
    ItemCaixa,
    Operador,
    ConferenciaCaixaExpedicao

    )
from cadastros.models import Setor as SetorModel 
from django.utils import timezone
from django.forms import modelformset_factory
import decimal
from collections import defaultdict

class ImportarOpsForm(forms.Form):
    data_inicio = forms.DateField(
        label="Importar OPs a partir de",
        widget=forms.DateInput(
            attrs={
                'type': 'date', 'class': 'form-control', 'style': 'width: 70%;'
            }
        ),
        required=True
    )
    tarja = forms.ChoiceField(
        label="Tarja da Programação (Opcional)",
        choices=[('', 'Nenhuma')] + list(OrdemProducao.TARJA_CHOICES),
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-select', 'style': 'width: 70%;'}
        )
    )

class ImportarOpIndividualForm(forms.Form):
    numero_op = forms.CharField(
        label="Número da Ordem de Produção",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    data_quimica = forms.DateField(
        label="Data Programada para Química",
        required=True,
        initial=timezone.now().date,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    # CAMPO 'cliente' FOI COMPLETAMENTE REMOVIDO DAQUI

    tarja = forms.ChoiceField(
        label="Tarja da Programação (Opcional)",
        choices=[('', 'Nenhuma')] + list(OrdemProducao.TARJA_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class ControlePastilhaForm(forms.ModelForm):
    peso_10_botoes = forms.DecimalField(
        label="Peso de 10 Botões (g)", 
        required=False, 
        max_digits=10, 
        decimal_places=3,
        help_text=""
    )

    proximo_setor = forms.ModelChoiceField(
        queryset=SetorModel.objects.filter(
            nome__in=['TORNOS', 'LASER', 'LASER 2', 'KANBAN']
        ),
        label="Transferir para o Setor",
        required=True,
        empty_label="Selecione o destino..."
    )

    class Meta:
        model = ControlePastilha
        fields = [
            'responsavel', 'tipo', 'peso_10_botoes', 'peso', 
            'quantidade_grosas', 'observacao'
        ]
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 3}),
            'peso': forms.NumberInput(attrs={'placeholder': 'Ex: 15.500'}),
        }
        labels = {
            'peso': 'Peso Medido (Kg)',
            'quantidade_grosas': 'Quantidade (Grôsas)',
        }

    def __init__(self, *args, **kwargs):
        self.saldo_maximo = kwargs.pop('saldo_maximo', None)
        self.ordem_producao = kwargs.pop('ordem_producao', None)
        super().__init__(*args, **kwargs)
        
        self.fields['responsavel'].queryset = Operador.objects.filter(
            setor__nome='ESCOLHA PASTILHA', 
            ativo=True
        )
        
        self.fields['quantidade_grosas'].widget.attrs['readonly'] = True
        self.fields['quantidade_grosas'].required = False

        if self.ordem_producao and self.ordem_producao.peso_bruto_grosa:
            try:
                initial_peso = (self.ordem_producao.peso_bruto_grosa / 144) * 10
                self.fields['peso_10_botoes'].initial = round(initial_peso, 3)
            except (TypeError, ValueError):
                pass

    def clean_peso(self):
        peso_medido = self.cleaned_data.get('peso')
        
        if peso_medido is None or peso_medido <= 0:
            raise forms.ValidationError("O peso medido deve ser maior que zero.")

        if self.saldo_maximo is not None:
            # --- CORREÇÃO APLICADA AQUI ---
            # Define o limite inferior (5% menor que o saldo)
            limite_inferior = self.saldo_maximo * decimal.Decimal('0.95')
            
            # Mantém a trava apenas se o peso for menor que o limite inferior
            if peso_medido < limite_inferior:
                raise forms.ValidationError(
                    f"O peso medido ({peso_medido} Kg) não pode ser mais de 5% menor que o saldo pendente ({limite_inferior:.4f} Kg)."
                )
            # A trava para o limite superior foi removida.
            
        return peso_medido

class PcpListFilterForm(forms.Form):
    """
    Formulário de filtro para a lista de Ordens de Produção do PCP.
    Refatorado para incluir a busca por nome do cliente.
    """
    numero_op = forms.CharField(
        label="Nº da OP",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nº da OP...'})
    )
    numero_pedido = forms.CharField(
        label="Nº do Pedido",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nº do Pedido...'})
    )
    # --- NOVO CAMPO ADICIONADO ---
    cliente = forms.CharField(
        label="Cliente",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do cliente...'})
    )
    numero_agrupamento = forms.CharField(
        label="Nº do Agrupamento",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nº do Agrupamento...'})
    )
    data_inicio = forms.DateField(
        label="Data de Emissão (Início)",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    data_fim = forms.DateField(
        label="Data de Emissão (Fim)",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

class PcpListFinanFilterForm(forms.Form):
    numero_pedido = forms.CharField(
        label="Pesquisar por Nº do Pedido",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o número do pedido...'})
    )
    # NOVO CAMPO
    cliente = forms.CharField(
        label="Pesquisar por Cliente",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do cliente...'})
    )
    status = forms.ChoiceField(
        label="Status do Pedido",
        choices=[('', 'Todos'), ('PENDENTE', 'Pendentes'), ('FECHADO', 'Fechados')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class OrdemProducaoPCPUpdateForm(forms.ModelForm):
    class Meta:
        model = OrdemProducao
        # Campos que o PCP poderá editar nesta tela
        fields = ['sequencia_pcp', 'data_qmc', 'tarja', 'observacao_op']
        
        widgets = {
            'data_qmc': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'observacao_op': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
            'sequencia_pcp': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'tarja': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }
        
        labels = {
            'sequencia_pcp': 'Sequência PCP (NOVA_SEQ)',
            'data_qmc': 'Data Produção Química (DATA_QMC)',
            'tarja': 'Tarja de Prioridade',
            'observacao_op': 'Observações da OP (PCP)',
        }

class ReprogramacaoForm(forms.ModelForm):
    peso_10_botoes = forms.DecimalField(
        label="Peso de 10 Botões (g)",
        required=False,
        max_digits=10,
        decimal_places=3,
        help_text="Necessário se o peso da grôsa ainda não foi definido para esta OP."
    )

    class Meta:
        model = ReprogramacaoOP
        fields = ['motivo', 'peso_reprogramado', 'peso_10_botoes', 'observacao']
        widgets = {
            'motivo': forms.Select(attrs={'class': 'form-select'}),
            'peso_reprogramado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2.500'}),
            'peso_10_botoes': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'peso_reprogramado': 'Peso a ser Reprogramado (Kg)',
        }

    def __init__(self, *args, **kwargs):
        self.ordem_producao = kwargs.pop('ordem_producao', None)
        super().__init__(*args, **kwargs)

        if self.ordem_producao and self.ordem_producao.peso_bruto_grosa:
            try:
                initial_peso = (self.ordem_producao.peso_bruto_grosa / 144) * 10
                self.fields['peso_10_botoes'].initial = round(initial_peso, 3)
                self.fields['peso_10_botoes'].widget.attrs['readonly'] = True
                self.fields['peso_10_botoes'].help_text = "Peso já definido no apontamento anterior."
            except (TypeError, ValueError):
                pass

    def clean(self):
        cleaned_data = super().clean()
        peso_reprogramado = cleaned_data.get('peso_reprogramado')
        peso_10_botoes = cleaned_data.get('peso_10_botoes')
        
        if peso_reprogramado and self.ordem_producao and not self.ordem_producao.peso_bruto_grosa and not peso_10_botoes:
            self.add_error('peso_10_botoes', 'Este campo é obrigatório para calcular as grôsas do retrabalho.')
            
        return cleaned_data

class ApontamentoInicioForm(forms.ModelForm):
    """
    Formulário simples para iniciar um novo apontamento de produção.
    """
    class Meta:
        model = ControleProducaoTornoLaser
        fields = ['maquina', 'responsavel']
        widgets = {
            'maquina': forms.Select(attrs={'class': 'form-select'}),
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        setor = kwargs.pop('setor', None)
        super().__init__(*args, **kwargs)

        # CORREÇÃO: Filtra as máquinas pelo nome do setor relacionado,
        # usando um lookup que "atravessa" a chave estrangeira.
        if setor:
            # O lookup 'setor__nome__istartswith' busca por máquinas cujo 'setor'
            # relacionado tenha um 'nome' que comece com o valor do enum (ex: 'TORNO'),
            # ignorando maiúsculas/minúsculas.
            self.fields['maquina'].queryset = Maquina.objects.filter(setor__nome__istartswith=setor.value)



class ApontamentoFimForm(forms.ModelForm):
    """
    Formulário para registrar o FIM de um apontamento de produção,
    agora com lógica para transferência de saldo.
    """
    peso_10_botoes = forms.DecimalField(
        label="Peso de 10 botões (em gramas)",
        required=False, max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Atualize para recalcular o peso da grôsa."
    )
    
    producao_grosas = forms.DecimalField(
        label="Produção (Grôsas)",
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        help_text="Calculado automaticamente."
    )

    peso_a_transferir = forms.DecimalField(
        label="Peso a Transferir (Kg)",
        required=False, max_digits=10, decimal_places=3,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Informe o peso a ser enviado para o próximo setor."
    )

    # --- REATORAÇÃO PRINCIPAL APLICADA AQUI ---
    # Trocamos o ChoiceField por um ModelChoiceField.
    # Agora, o campo trabalha diretamente com os objetos do banco de dados.
    proximo_setor = forms.ModelChoiceField(
        # Busca os setores diretamente do banco de dados.
        queryset=SetorModel.objects.filter(
            nome__in=['POLIMENTO', 'TINGIMENTO', 'ESCOLHA FINAL', 'LASER']
        ),
        required=False,
        label="Encaminhar Saldo para o Setor",
        widget=forms.Select(attrs={'class': 'form-select'}),
        # Garante que a opção em branco seja exibida
        empty_label="Selecione um setor..."
    )

    class Meta:
        model = ControleProducaoTornoLaser
        fields = [
            'estado', 'botoes_por_minuto', 'producao_peso', 'quebra_peso',
            'responsavel',
            'check_espessura_cabecote1', 'check_espessura_cabecote2', 'check_broca',
            'check_abertura', 'check_carregador', 'check_botao', 'check_troca',
            'observacao'
        ]
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
            'producao_peso': forms.NumberInput(attrs={'id': 'id_producao_peso'}),
            'observacao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.ordem_producao = kwargs.pop('ordem_producao', None)
        super().__init__(*args, **kwargs)
        
        if self.ordem_producao and self.ordem_producao.peso_liquido_grosa:
            try:
                initial_peso = (self.ordem_producao.peso_liquido_grosa / 144) * 10
                self.fields['peso_10_botoes'].initial = round(initial_peso, 2)
            except (TypeError, ValueError):
                self.fields['peso_10_botoes'].initial = 0

        for field_name in self.fields:
            if field_name.startswith('check_'):
                self.fields[field_name].required = True

    def clean(self):
        cleaned_data = super().clean()
        producao_peso = cleaned_data.get('producao_peso') or 0
        peso_a_transferir = cleaned_data.get('peso_a_transferir') or 0
        proximo_setor = cleaned_data.get('proximo_setor')

        if peso_a_transferir > producao_peso:
            self.add_error('peso_a_transferir', 
                f"O peso a transferir ({peso_a_transferir} Kg) não pode ser maior que o peso produzido ({producao_peso} Kg).")
        
        # Validação adicional: se um peso for informado, o setor de destino é obrigatório.
        if peso_a_transferir > 0 and not proximo_setor:
            self.add_error('proximo_setor', "Se um peso for transferido, o setor de destino é obrigatório.")

        return cleaned_data



# FormSet para criar dinamicamente múltiplos formulários de parada.
ParadaProducaoFormSet = modelformset_factory(
    Parada,
    fields=('motivo', 'data_hora_inicio', 'data_hora_fim'),
    extra=1,  # Começa com 1 formulário de parada em branco.
    can_delete=True, # Permite deletar paradas existentes.
    widgets={
        'motivo': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        'data_hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control form-control-sm'}),
        'data_hora_fim': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control form-control-sm'}),
    }
)

class SolicitacaoQuimicaKanbanForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoQuimicaKanban
        fields = ['quantidade_solicitada']
        widgets = {
            'quantidade_solicitada': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Qtd. em Grosas'}),
        }
        labels = {
            'quantidade_solicitada': 'Quantidade Necessária (GRS)',
        }
    class Meta:
        model = SolicitacaoQuimicaKanban
        fields = ['quantidade_solicitada']
        widgets = {
            'quantidade_solicitada': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Qtd. em Grosas'}),
        }
        labels = {
            'quantidade_solicitada': 'Quantidade Necessária (GRS)',
        }

# --- FORMS PARA APONTAMENTO CILINDRO (NOVOS E REATORADOS) ---

class ApontamentoCilindroInicioForm(forms.ModelForm):
    """
    Formulário para iniciar um novo lançamento de produção no cilindro.
    """
    class Meta:
        model = LancamentoCilindro
        fields = ['operador', 'maquina']
        widgets = {
            'operador': forms.Select(attrs={'class': 'form-select'}),
            'maquina': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['operador'].queryset = Operador.objects.filter(ativo=True)
        self.fields['maquina'].queryset = Maquina.objects.filter(setor_id=10)


class ApontamentoCilindroFimForm(forms.ModelForm):
    """
    Formulário para finalizar/editar um lançamento de produção no cilindro.
    Inclui campos dinâmicos para a contribuição de cada OP.
    """
    class Meta:
        model = LancamentoCilindro
        fields = ['observacoes'] 
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control form-control-sm'}),
        }

    def __init__(self, *args, **kwargs):
        ordens_producao = kwargs.pop('ordens_producao', [])
        super().__init__(*args, **kwargs)

        if ordens_producao:
            for op in ordens_producao:
                field_name = f'placas_op_{op.pk}'
                initial_value = 0
                if self.instance.pk:
                    try:
                        contrib = ContribuicaoOP.objects.get(lancamento=self.instance, ordem_producao=op)
                        initial_value = contrib.quantidade_placas_contribuida
                    except ContribuicaoOP.DoesNotExist:
                        initial_value = 0

                self.fields[field_name] = forms.DecimalField(
                    label=f'Qtd. Placas (OP {op.numero_op})',
                    required=False,
                    initial=initial_value,
                    widget=forms.NumberInput(attrs={
                        'class': 'form-control form-control-sm contribution-placas',
                        'data-rendimento': str(op.rendimento or '0'),
                        'step': '0.0001',
                        'placeholder': '0.0000'
                    })
                )

    def clean(self):
        """
        Validação personalizada para garantir que a quantidade total de placas seja maior que zero.
        """
        cleaned_data = super().clean()
        
        # Encontra todos os campos de contribuição de placas
        placas_fields = [key for key in self.cleaned_data if key.startswith('placas_op_')]
        
        total_placas = 0
        for field in placas_fields:
            # Soma os valores, tratando valores nulos como zero
            total_placas += self.cleaned_data.get(field) or 0
            
        # Se a soma for zero ou menos, levanta um erro de validação
        if total_placas <= 0:
            raise forms.ValidationError(
                "O apontamento não pode ser salvo com a quantidade total de placas igual a zero. Por favor, insira uma quantidade.",
                code='total_placas_zero'
            )
            
        return cleaned_data

# FormSet para as paradas do lançamento do cilindro
ParadaCilindroFormSet = modelformset_factory(
    ParadaLancamentoAgrupado,
    fields=('motivo', 'duracao_minutos'),
    extra=1,
    can_delete=True,
    widgets={
        'motivo': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        'duracao_minutos': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Minutos'}),
    }
)

# --- FIM DOS FORMS PARA APONTAMENTO CILINDRO ---

# Formulário de Solicitação de estoque Kanban
class SolicitacaoReposicaoKanbanForm(forms.ModelForm):
    """
    Formulário para criar uma nova solicitação de reposição de estoque Kanban.
    """
    class Meta:
        model = SolicitacaoReposicaoKanban
        fields = ['item_estoque', 'quantidade_placas_solicitada', 'observacao']
        widgets = {
            'item_estoque': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_placas_solicitada': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'item_estoque': 'Item de Estoque a ser Produzido',
            'quantidade_placas_solicitada': 'Quantidade de Placas (conforme cartão)',
            'observacao': 'Observações (Opcional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Garante que o campo de item de estoque seja obrigatório e tenha um texto inicial
        self.fields['item_estoque'].empty_label = "Selecione o material..."
        self.fields['item_estoque'].required = True

class ApontamentoCilindroKanbanInicioForm(forms.ModelForm):
    """
    Formulário para iniciar um novo lançamento de produção para reposição Kanban.
    É funcionalmente idêntico ao formulário de início para OPs de cliente.
    """
    class Meta:
        model = LancamentoCilindro
        fields = ['operador', 'maquina']
        widgets = {
            'operador': forms.Select(attrs={'class': 'form-select'}),
            'maquina': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra para operadores ativos e máquinas do tipo Cilindro (setor_id=10, conforme seu código)
        self.fields['operador'].queryset = Operador.objects.filter(ativo=True)
        self.fields['maquina'].queryset = Maquina.objects.filter(setor_id=10)


class ApontamentoCilindroKanbanFimForm(forms.ModelForm):
    """
    Formulário para finalizar/editar um lançamento de produção para reposição Kanban.
    Simplificado para ter apenas um campo de quantidade de placas.
    """
    class Meta:
        model = LancamentoCilindro
        # O campo 'quantidade_placas_total' é o principal aqui.
        fields = ['quantidade_placas_total', 'observacoes']
        widgets = {
            'quantidade_placas_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'observacoes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control form-control-sm'}),
        }
        labels = {
            'quantidade_placas_total': 'Quantidade de Placas Produzidas',
            'observacoes': 'Observações do Lançamento'
        }

    def clean_quantidade_placas_total(self):
        """ Garante que a quantidade de placas seja um valor positivo. """
        qtd = self.cleaned_data.get('quantidade_placas_total')
        if qtd is None or qtd <= 0:
            raise forms.ValidationError("A quantidade de placas produzidas deve ser maior que zero.")
        return qtd

# O FormSet de paradas pode ser o mesmo usado para o outro fluxo
ParadaCilindroKanbanFormSet = modelformset_factory(
    ParadaLancamentoAgrupado,
    fields=('motivo', 'duracao_minutos'),
    extra=1,
    can_delete=True,
    widgets={
        'motivo': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        'duracao_minutos': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Minutos'}),
    }
)

class ControlePastilhaKanbanForm(forms.Form):
    """
    Formulário específico para o apontamento de medição de pastilha 
    para solicitações de reposição de estoque Kanban.
    """
    responsavel = forms.ModelChoiceField(
        queryset=Operador.objects.filter(setor__nome='ESCOLHA PASTILHA', ativo=True),
        label="Responsável",
        empty_label="Selecione o responsável..."
    )
    tipo = forms.ChoiceField(
        choices=ControlePastilha.Tipo.choices,
        label="Tipo de Pastilha"
    )
    peso_10_botoes = forms.DecimalField(
        label="Peso de 10 Botões (g)",
        required=True,
        max_digits=10,
        decimal_places=3,
        help_text="Informe o peso em gramas de 10 peças para calcular o peso da grôsa.",
        widget=forms.NumberInput(attrs={'placeholder': 'Ex: 12.345'})
    )
    peso = forms.DecimalField(
        label="Peso Medido (Kg)",
        required=True,
        max_digits=10,
        decimal_places=4,
        help_text="Peso real medido que entrará no estoque.",
        widget=forms.NumberInput(attrs={'placeholder': 'Ex: 15.5000'})
    )
    quantidade_grosas = forms.DecimalField(
        label="Quantidade (Grôsas)",
        required=False,
        max_digits=10,
        decimal_places=2,
    )
    observacao = forms.CharField(
        label="Observação",
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna o campo de grôsas somente leitura e adiciona classes para estilização
        self.fields['quantidade_grosas'].widget.attrs['readonly'] = True
        self.fields['quantidade_grosas'].widget.attrs['class'] = 'fw-bold bg-light'

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if peso is None or peso <= 0:
            raise forms.ValidationError("O peso medido deve ser maior que zero.")
        return peso

    def clean_peso_10_botoes(self):
        peso = self.cleaned_data.get('peso_10_botoes')
        if peso is None or peso <= 0:
            raise forms.ValidationError("O peso de 10 botões deve ser maior que zero.")
        return peso

class ApontamentoPolimentoForm(forms.ModelForm):
    """
    Formulário principal para o apontamento de polimento.
    """
    class Meta:
        model = ControlePolimento
        fields = ['tambor', 'responsavel', 'observacao']
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'tambor': forms.Select(attrs={'class': 'form-select'}),
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tambor'].label = "Tambor de Polimento"
        self.fields['responsavel'].label = "Responsável"
        self.fields['responsavel'].queryset = Operador.objects.filter(ativo=True, setor__nome='POLIMENTO')
        self.fields['tambor'].queryset = Maquina.objects.filter(setor__nome='POLIMENTO')


class ApontamentoPolimentoForm(forms.ModelForm):
    class Meta:
        model = ControlePolimento
        fields = ['tambor', 'responsavel', 'observacao']
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'tambor': forms.Select(attrs={'class': 'form-select'}),
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tambor'].label = "Tambor de Polimento"
        self.fields['responsavel'].label = "Responsável"
        self.fields['responsavel'].queryset = Operador.objects.filter(ativo=True, setor__nome='POLIMENTO')
        self.fields['tambor'].queryset = Maquina.objects.filter(setor__nome='POLIMENTO')


class ItemPolimentoForm(forms.ModelForm):
    # Este campo existe apenas no formulário, não no modelo.
    proximo_setor = forms.ModelChoiceField(
        queryset=SetorModel.objects.filter(nome__in=['POLIMENTO', 'ESCOLHA FINAL', 'TINGIMENTO', 'TORNOS']),
        required=False, # A obrigatoriedade é verificada na view, ao finalizar.
        label="Próximo Setor",
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )

    class Meta:
        model = ItemPolimento
        # Apenas os campos do modelo são listados aqui.
        fields = ['item_demanda', 'peso_carregado']
        widgets = {
            'item_demanda': forms.HiddenInput(),
            'peso_carregado': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '0.000'}),
        }


class BaseItemPolimentoFormSet(forms.BaseModelFormSet):
    # ... (a lógica de validação 'clean' permanece a mesma) ...
    def clean(self):
        if any(self.errors):
            return
        super().clean()
        
        pesos_por_op = defaultdict(decimal.Decimal)
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                continue
            
            peso_carregado = form.cleaned_data.get('peso_carregado', 0)
            item_demanda = form.cleaned_data.get('item_demanda')

            if not item_demanda:
                continue

            op_id = item_demanda.ordem_producao_id
            pesos_por_op[op_id] += peso_carregado

        setor_polimento = SetorModel.objects.get(nome__iexact='POLIMENTO')
        for op_id, total_peso_carregado in pesos_por_op.items():
            try:
                saldo_op = SaldoOPSetor.objects.get(ordem_producao_id=op_id, setor=setor_polimento)
                saldo_disponivel = saldo_op.saldo_peso
            except SaldoOPSetor.DoesNotExist:
                saldo_disponivel = 0

            if total_peso_carregado > saldo_disponivel:
                op_numero = OrdemProducao.objects.get(pk=op_id).numero_op
                raise forms.ValidationError(
                    f"O peso total carregado para a OP {op_numero} "
                    f"({total_peso_carregado} Kg) excede o saldo disponível de {saldo_disponivel} Kg."
                )

# O ParadaPolimentoFormSet permanece o mesmo
ParadaPolimentoFormSet = modelformset_factory(
    ParadaPolimento,
    fields=('id', 'motivo', 'data_hora_inicio', 'data_hora_fim'),
    extra=1,
    can_delete=True,
    widgets={
        'id': forms.HiddenInput(),
        'motivo': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        'data_hora_inicio': forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', 'class': 'form-control form-control-sm'}
        ),
        'data_hora_fim': forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', 'class': 'form-control form-control-sm'}
        ),
    }
)

# -- Escolha Final
class ConferenciaEscolhaFinalForm(forms.ModelForm):
    """
    Formulário para a etapa de CONFERÊNCIA na Escolha Final.
    Refatorado para incluir o campo de espessura e sua validação.
    """
    peso_a_transferir = forms.DecimalField(
        label="Peso a Transferir (Kg)",
        required=False, max_digits=10, decimal_places=3,
        help_text="Peso que será enviado ao próximo setor. Deve ser igual ou menor que o peso aferido."
    )
    proximo_setor = forms.ModelChoiceField(
        label="Transferir para o Setor",
        queryset=SetorModel.objects.filter(nome__in=['TINGIMENTO', 'CONTROLE DE QUALIDADE', 'CONTAGEM ACIMA 80', 'CONTAGEM ATE 80']),
        required=False, empty_label="Selecione o destino..."
    )

    class Meta:
        model = ConferenciaEscolhaFinal
        # --- CAMPO 'espessura_conferida' ADICIONADO ---
        fields = ['responsavel', 'peso_10_botoes', 'peso_aferido', 'espessura_conferida', 'observacao', 'peso_a_transferir', 'proximo_setor']
        widgets = { 'observacao': forms.Textarea(attrs={'rows': 3}) }
        labels = {
            'peso_10_botoes': 'Peso de 10 Botões (g)',
            'peso_aferido': 'Peso Total Aferido (Kg)',
            'espessura_conferida': 'Espessura Conferida (mm)',
        }

    def __init__(self, *args, **kwargs):
        self.item_demanda = kwargs.pop('item_demanda', None)
        super().__init__(*args, **kwargs)
        self.fields['responsavel'].queryset = Operador.objects.filter(ativo=True, setor__nome='ESCOLHA FINAL')
        self.fields['responsavel'].empty_label = "Selecione o responsável..."
        if self.item_demanda and self.item_demanda.ordem_producao.peso_liquido_grosa:
            try:
                initial_peso_10 = (self.item_demanda.ordem_producao.peso_liquido_grosa / 144) * 10
                self.fields['peso_10_botoes'].initial = round(initial_peso_10, 3)
            except (TypeError, ValueError): pass

    def clean(self):
        cleaned_data = super().clean()
        peso_aferido = cleaned_data.get('peso_aferido', 0) or 0
        peso_a_transferir = cleaned_data.get('peso_a_transferir', 0) or 0
        proximo_setor = cleaned_data.get('proximo_setor')

        if peso_a_transferir > peso_aferido:
            self.add_error('peso_a_transferir', 'O peso a transferir não pode ser maior que o peso aferido.')
        if peso_a_transferir > 0 and not proximo_setor:
            self.add_error('proximo_setor', 'Se um peso for transferido, o setor de destino é obrigatório.')
        return cleaned_data

class ApontamentoCQInicioForm(forms.ModelForm):
    """ Formulário para iniciar uma inspeção, registrando os responsáveis e a máquina. """
    class Meta:
        model = ControleQualidadeEsteira
        fields = ['responsavel', 'responsavel_2', 'maquina']
        labels = {
            'responsavel': 'Operador 1',
            'responsavel_2': 'Operador 2 (Opcional)',
            'maquina': 'Esteira de Inspeção'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra operadores do setor de Controle de Qualidade
        operadores_qs = Operador.objects.filter(
            ativo=True, setor__nome='CONTROLE DE QUALIDADE'
        )
        self.fields['responsavel'].queryset = operadores_qs
        self.fields['responsavel_2'].queryset = operadores_qs
        self.fields['responsavel'].empty_label = "Selecione..."
        self.fields['responsavel_2'].empty_label = "Nenhum"
        
        # Filtra máquinas do setor 'ESCOLHA PASTILHA', conforme solicitado.
        # Isso implica que as esteiras de CQ estão cadastradas sob este setor no sistema.
        self.fields['maquina'].queryset = Maquina.objects.filter(
            setor__nome='ESCOLHA PASTILHA'
        )
        self.fields['maquina'].empty_label = "Selecione..."
        
        # Garante que a seleção da máquina seja obrigatória
        self.fields['maquina'].required = True


# FORMULÁRIO DE FIM CORRIGIDO
class ApontamentoCQFimForm(forms.ModelForm):
    """
    Formulário para finalizar a inspeção de Controle de Qualidade.
    """
    peso_a_devolver = forms.DecimalField(
        label="Peso a Devolver para Conferência (Kg)",
        required=False, 
        max_digits=10, 
        decimal_places=3,
        help_text="Preencha este campo apenas se parte do lote for devolvido."
    )

    class Meta:
        model = ControleQualidadeEsteira
        # CORREÇÃO: 'peso_total_apontado' foi alterado para 'peso_total_aprovado'
        # para corresponder ao nome do campo no modelo.
        fields = [
            'peso_total_aprovado', 'peso_defeito_tipo_a', 
            'peso_defeito_tipo_b', 'peso_a_devolver', 'observacao'
        ]
        widgets = { 'observacao': forms.Textarea(attrs={'rows': 3}) }
        labels = {
            'peso_total_aprovado': 'Peso Total Aprovado (Kg)',
            'peso_defeito_tipo_a': 'Peso Defeito Tipo A (Kg)',
            'peso_defeito_tipo_b': 'Peso Defeito Tipo B (Kg)',
        }

    def __init__(self, *args, **kwargs):
        self.item_demanda = kwargs.pop('item_demanda', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        peso_aprovado = cleaned_data.get('peso_total_aprovado') or 0
        peso_defeito_a = cleaned_data.get('peso_defeito_tipo_a') or 0
        peso_defeito_b = cleaned_data.get('peso_defeito_tipo_b') or 0
        peso_a_devolver = cleaned_data.get('peso_a_devolver') or 0

        if self.item_demanda:
            setor_cq = SetorModel.objects.get(nome='CONTROLE DE QUALIDADE')
            saldo_obj = SaldoOPSetor.objects.filter(
                ordem_producao=self.item_demanda.ordem_producao,
                setor=setor_cq
            ).first()
            saldo_disponivel = saldo_obj.saldo_peso if saldo_obj else 0
            
            soma_pesos_declarados = peso_aprovado + peso_defeito_a + peso_defeito_b + peso_a_devolver
            
            if soma_pesos_declarados > (saldo_disponivel + decimal.Decimal('0.001')):
                raise forms.ValidationError(
                    f"A soma dos pesos informados ({soma_pesos_declarados} Kg) não pode exceder o saldo disponível no setor ({saldo_disponivel} Kg)."
                )
        return cleaned_data

class ContagemFinalForm(forms.ModelForm):
    """
    Formulário para o apontamento de Contagem Final.
    """
    class Meta:
        model = ContagemFinal
        # --- CORREÇÃO APLICADA AQUI ---
        # O campo 'maquina_contagem' foi removido da lista de campos do formulário.
        fields = [
            'responsavel', 'tipo_embalagem', 
            'pesagem', 'total_embalagem', 'observacao'
        ]
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 3}),
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
            'tipo_embalagem': forms.Select(attrs={'class': 'form-select'}),
            'pesagem': forms.Select(attrs={'class': 'form-select'}),
            'total_embalagem': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'responsavel': 'Responsável pela Contagem',
            'tipo_embalagem': 'Tipo de Embalagem',
            'pesagem': 'Tipo de Pesagem',
            'total_embalagem': 'Total de Embalagens Fechadas',
            'observacao': 'Observações'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra os operadores para o setor 'ESCOLHA FINAL'
        self.fields['responsavel'].queryset = Operador.objects.filter(
            ativo=True, setor__nome='ESCOLHA FINAL'
        )
        self.fields['responsavel'].empty_label = "Selecione..."

class LancamentoTingimentoInicioForm(forms.ModelForm):
    class Meta:
        model = LancamentoTingimento
        fields = ['responsavel']
        widgets = { 'responsavel': forms.Select(attrs={'class': 'form-select'}) }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsavel'].queryset = Operador.objects.filter(ativo=True, setor__nome='TINGIMENTO')
        self.fields['responsavel'].empty_label = "Selecione o responsável..."


class LancamentoTingimentoFimForm(forms.ModelForm):
    class Meta:
        model = LancamentoTingimento
        fields = ['observacao']
        widgets = { 'observacao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control form-control-sm'}) }


# ALTERAÇÃO 1: Este formset agora será usado no topo da página para definir o destino final de cada item.
class ItemTingimentoForm(forms.ModelForm):
    """ Este form controla o destino final do item no lote. """
    class Meta:
        model = ItemTingimento
        fields = ['proximo_setor']
        widgets = {
            'proximo_setor': forms.Select(attrs={'class': 'form-select form-select-sm'})
        }

ItemTingimentoFormSet = modelformset_factory(
    ItemTingimento,
    form=ItemTingimentoForm,
    extra=0,
    can_delete=False
)


# ALTERAÇÃO 2: O form de Carga agora só se preocupa com o peso. O destino foi removido.
class CargaLancamentoTingimentoForm(forms.ModelForm):
    """ Form para o peso de cada item DENTRO de um lançamento. """
    class Meta:
        model = CargaLancamentoTingimento
        fields = ['peso_carregado'] # REMOVIDO: 'proximo_setor'
        widgets = {
            'peso_carregado': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '0.000'}),
        }

CargaLancamentoFormSet = modelformset_factory(
    CargaLancamentoTingimento,
    form=CargaLancamentoTingimentoForm,
    extra=0,
    can_delete=False
)


# ... (ParadaTingimentoForm e ParadaTingimentoFormSet permanecem iguais) ...
class ParadaTingimentoForm(forms.ModelForm):
    class Meta:
        model = ParadaTingimento
        fields = ['motivo', 'data_hora_inicio', 'data_hora_fim']
        widgets = {
            'motivo': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'data_hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control form-control-sm'}),
            'data_hora_fim': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control form-control-sm'}),
        }

ParadaTingimentoFormSet = modelformset_factory(
    ParadaTingimento,
    form=ParadaTingimentoForm,
    extra=1,
    can_delete=True
)

class ApontamentoEmbalagemForm(forms.ModelForm):
    class Meta:
        model = ApontamentoEmbalagem
        fields = [
            'responsavel', 'quantidade_embalada', 'numero_caixa', 
            'tam_cx', 'tipo_caixa', 'peso_caixa'
        ]
        widgets = {
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_embalada': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_caixa': forms.NumberInput(attrs={'class': 'form-control'}),
            'tam_cx': forms.Select(attrs={'class': 'form-select'}),
            'tipo_caixa': forms.Select(attrs={'class': 'form-select'}),
            'peso_caixa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
        }

    def __init__(self, *args, **kwargs):
        self.item_demanda = kwargs.pop('item_demanda', None)
        super().__init__(*args, **kwargs)
        
        # Filtra para mostrar apenas operadores do setor de Embalagem
        self.fields['responsavel'].queryset = Operador.objects.filter(setor__nome='CONFERENCIA/EXPEDIÇÃO', ativo=True)
        self.fields['responsavel'].empty_label = "Selecione..."

    def clean_quantidade_embalada(self):
        quantidade = self.cleaned_data.get('quantidade_embalada')
        if self.item_demanda and hasattr(self.item_demanda, 'saldo_embalagem'):
            saldo_disponivel = self.item_demanda.saldo_embalagem.saldo_grosas
            if quantidade > saldo_disponivel:
                raise forms.ValidationError(
                    f"A quantidade a embalar ({quantidade}) não pode ser maior que o saldo disponível ({saldo_disponivel})."
                )
        elif self.item_demanda:
             raise forms.ValidationError("Este item não possui saldo no setor de embalagem.")
        return quantidade

# - Painel de Conferência PCP
class PCPConferenciaItemUpdateForm(forms.ModelForm):
    """
    Formulário usado no modal da tela de conferência do PCP para
    ajustar dados específicos de uma Ordem de Produção.
    """
    class Meta:
        model = OrdemProducao
        # --- CAMPO ADICIONADO ---
        fields = ['observacao_op', 'tarja', 'data_qmc', 'requer_tingimento']
        widgets = {
            'observacao_op': forms.Textarea(attrs={'rows': 3}),
            'tarja': forms.Select(attrs={'class': 'form-select'}),
            'data_qmc': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # --- WIDGET PARA O NOVO CAMPO ---
            'requer_tingimento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'observacao_op': 'Observações do PCP',
            'tarja': 'Tarja de Prioridade',
            'data_qmc': 'Data da Química',
            # --- LABEL PARA O NOVO CAMPO ---
            'requer_tingimento': 'Requer Tingimento?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tarja'].choices = [('', '---------')] + list(OrdemProducao.TARJA_CHOICES)

# --- NOVOS FORMULÁRIOS PARA EMBALAGEM E EXPEDIÇÃO ---

class AbrirCaixaForm(forms.ModelForm):
    """
    Formulário para abrir uma nova caixa no setor de Embalagem.
    """
    class Meta:
        model = Caixa
        fields = ['responsavel_embalagem', 'tam_cx', 'tipo_caixa']
        widgets = {
            'responsavel_embalagem': forms.Select(attrs={'class': 'form-select'}),
            'tam_cx': forms.Select(attrs={'class': 'form-select'}),
            'tipo_caixa': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'responsavel_embalagem': 'Responsável pela Embalagem',
            'tam_cx': 'Tamanho da Caixa',
            'tipo_caixa': 'Tipo da Caixa',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsavel_embalagem'].queryset = Operador.objects.filter(
            setor__nome='CONFERENCIA/EXPEDIÇÃO', ativo=True
        )
        self.fields['responsavel_embalagem'].empty_label = "Selecione..."


class AdicionarItemCaixaForm(forms.ModelForm):
    """
    Formulário para adicionar um item de demanda a uma caixa aberta.
    """
    class Meta:
        model = ItemCaixa
        fields = ['quantidade_embalada']
        labels = {
            'quantidade_embalada': 'Quantidade a Embalar (GRS)',
        }

    def __init__(self, *args, **kwargs):
        # Recebe o item_demanda da view para poder validar o saldo
        self.item_demanda = kwargs.pop('item_demanda', None)
        super().__init__(*args, **kwargs)

    def clean_quantidade_embalada(self):
        quantidade = self.cleaned_data.get('quantidade_embalada')
        
        if quantidade is None or quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")

        if self.item_demanda and hasattr(self.item_demanda, 'saldo_embalagem'):
            saldo_disponivel = self.item_demanda.saldo_embalagem.saldo_grosas
            if quantidade > saldo_disponivel:
                raise forms.ValidationError(
                    f"A quantidade a embalar ({quantidade}) não pode ser maior que o saldo disponível ({saldo_disponivel})."
                )
        elif self.item_demanda:
            # Este caso ocorre se o item não tiver um saldo criado, o que não deveria acontecer no fluxo normal
            raise forms.ValidationError("Este item não possui saldo no setor de embalagem.")
            
        return quantidade


class ConferenciaCaixaForm(forms.ModelForm):
    """
    Formulário para a Expedição conferir e pesar uma caixa.
    """
    class Meta:
        model = Caixa
        fields = ['responsavel_expedicao', 'peso_final_caixa']
        widgets = {
            'responsavel_expedicao': forms.Select(attrs={'class': 'form-select'}),
            'peso_final_caixa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
        }
        labels = {
            'responsavel_expedicao': 'Responsável pela Conferência',
            'peso_final_caixa': 'Peso Final da Caixa (Kg)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsavel_expedicao'].queryset = Operador.objects.filter(
            setor__nome='CONFERENCIA/EXPEDIÇÃO', ativo=True
        )
        self.fields['responsavel_expedicao'].empty_label = "Selecione..."

# Formset para os checkboxes dos itens na conferência da caixa
ConferenciaItemCaixaFormSet = modelformset_factory(
    ItemCaixa,
    fields=('conferido_expedicao',),
    extra=0, # Não mostra formulários em branco
    widgets={
        'conferido_expedicao': forms.CheckboxInput(attrs={'class': 'form-check-input'})
    }
)

class ConferenciaCaixaForm(forms.ModelForm):
    class Meta:
        model = ConferenciaCaixaExpedicao
        fields = ['responsavel', 'peso_conferido']
        widgets = {
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
            'peso_conferido': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso Final da Caixa (Kg)'}),
        }
        labels = {
            'responsavel': 'Responsável pela Conferência',
            'peso_conferido': 'Peso Final da Caixa (Kg)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsavel'].queryset = Operador.objects.filter(setor__nome='EMBALAGEM', ativo=True) # Ajuste o nome do setor se necessário
        self.fields['responsavel'].empty_label = "Selecione o responsável..."

ACABAMENTO_CHOICES = (
    ('', 'Todos Acabamentos'),
    ('B', 'Brilhante'),
    ('F', 'Fosco'),
)

class OpFilterForm(forms.Form):
    """
    Formulário reutilizável para filtrar Ordens de Produção em diversas listagens.
    """
    # Dicionário de atributos para os widgets, garantindo a classe 'form-control-sm'
    widget_attrs = {'class': 'form-control form-control-sm'}

    numero_pedido = forms.IntegerField(
        label='Pedido',
        required=False,
        widget=forms.NumberInput(attrs={**widget_attrs, 'placeholder': 'Nº do Pedido...'})
    )
    numero_op = forms.IntegerField(
        label='OP',
        required=False,
        widget=forms.NumberInput(attrs={**widget_attrs, 'placeholder': 'Nº da OP...'})
    )
    tamanho = forms.IntegerField(
        label='Tamanho',
        required=False,
        widget=forms.NumberInput(attrs={**widget_attrs, 'placeholder': 'Tamanho...'})
    )
    material = forms.CharField(
        label='Material',
        required=False,
        widget=forms.TextInput(attrs={**widget_attrs, 'placeholder': 'Material...'})
    )
    cliente = forms.CharField(
        label='Cliente',
        required=False,
        widget=forms.TextInput(attrs={**widget_attrs, 'placeholder': 'Nome do Cliente...'})
    )

    acabamento = forms.ChoiceField(
    choices=ACABAMENTO_CHOICES,
    required=False,
    label="Acabamento",
    widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )


