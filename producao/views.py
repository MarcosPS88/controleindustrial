from collections import defaultdict
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
import decimal
from django.db.models import  Max, F, Q, Sum, Count, Case, When, Value, CharField, DecimalField, OuterRef, Subquery, Min, Exists
from django.db import transaction

from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import (
    Q, Sum, F, ExpressionWrapper, DecimalField, Count, Case, When, Value, CharField,
)
from django.utils import timezone
# Adiciona as CBVs genéricas que serão usadas
from django.views.generic import TemplateView, View, FormView, ListView, DetailView, UpdateView
from django.db.models.functions import Concat, Coalesce
import math
import re
from .auth_mixins import (
    ProducaoTornosRequiredMixin,
)


from .forms import (
    ImportarOpsForm,
    ImportarOpIndividualForm,
    ControlePastilhaForm,
    PcpListFilterForm,
    PcpListFinanFilterForm,
    OrdemProducaoPCPUpdateForm,
    ReprogramacaoForm,
    ApontamentoInicioForm, 
    ApontamentoFimForm,   
    SolicitacaoQuimicaKanbanForm,
    ParadaProducaoFormSet,
    ApontamentoCilindroInicioForm,
    ApontamentoCilindroFimForm,
    ParadaCilindroFormSet,
    SolicitacaoReposicaoKanbanForm,
    ApontamentoCilindroKanbanInicioForm,
    ApontamentoCilindroKanbanFimForm,
    ParadaCilindroKanbanFormSet,
    ControlePastilhaKanbanForm,
    ApontamentoPolimentoForm,
    ParadaPolimentoFormSet,
    ParadaPolimento,
    ConferenciaEscolhaFinalForm,
    ApontamentoCQInicioForm,
    ApontamentoCQFimForm,
    ContagemFinalForm,
    LancamentoTingimentoInicioForm,
    LancamentoTingimentoFimForm,
    ParadaTingimentoFormSet,
    ParadaTingimento,   
    CargaLancamentoFormSet,
    ItemTingimentoFormSet,
    ApontamentoEmbalagemForm,
    PCPConferenciaItemUpdateForm,
    AbrirCaixaForm, 
    AdicionarItemCaixaForm,
    ConferenciaCaixaForm, 
    ConferenciaItemCaixaFormSet,
    ConferenciaCaixaForm,
    OpFilterForm,
    ItemPolimentoForm,
    BaseItemPolimentoFormSet,

)
from django.forms import modelformset_factory
from .services import importar_ops_do_erp
from cadastros.models import Setor as SetorModel
from .models import (
    OrdemProducao,
    Setor,
    OrdemProducaoStatus,
    RegraKanban,
    FormulaQuimica,
    LoteQuimico,
    Pedido,
    ItemDemandaProducao,
    SolicitacaoQuimicaKanban,
    ContribuicaoOP, 
    ParadaLancamentoAgrupado,
    Operador,
    Maquina,
    MotivoParada,
    AgrupamentoLancamento,
    LancamentoCilindro,
    ControleProducaoTornoLaser,
    Parada,
    SaldoOPSetor,
    TransferenciaEntreSetores,
    ControlePastilha,
    ReprogramacaoOP,
    EstoqueKanban,
    ItemEstoqueKanban,
    SolicitacaoReposicaoKanban,
    MovimentoEstoqueKanban,
    ControlePolimento,
    ItemPolimento,
    ItemDemandaStatus,
    ControleQualidadeEsteira,
    LancamentoTingimento, 
    ItemTingimento,
    LoteTingimento,
    CargaLancamentoTingimento,
    ConferenciaEscolhaFinal,
    ApontamentoEmbalagem,
    SaldoItemEmbalagem,
    Cliente, 
    Pedido, 
    ItemDemandaProducao, 
    SaldoItemEmbalagem,
    Caixa, 
    ItemCaixa,
    ConferenciaCaixaExpedicao, 
    ItemConferenciaCaixa
    
)
from .models_erp import Pro01


class ImportarOpsView(FormView):
    """ Substitui a função importar_ops_view """
    template_name = 'producao/importar_ops.html'
    form_class = ImportarOpsForm
    success_url = reverse_lazy('producao:importar_ops_view') # Substitua pelo nome correto da sua URL

    def form_valid(self, form):
        data_selecionada = form.cleaned_data['data_inicio']
        tarja_selecionada = form.cleaned_data.get('tarja') or None
        
        importadas, com_erro = importar_ops_do_erp(
            data_inicio=data_selecionada,
            tarja=tarja_selecionada
        )
        
        if importadas > 0:
            messages.success(self.request, f'{importadas} nova(s) Ordem(ns) de Produção foram importadas com sucesso!')
        else:
            messages.info(self.request, 'Nenhuma nova Ordem de Produção encontrada para importação a partir da data selecionada.')

        if com_erro > 0:
            messages.warning(self.request, f'Houve erro ao tentar importar {com_erro} OP(s). Verifique os logs do sistema.')

        return super().form_valid(form)


class ImportarOpIndividualView(FormView):
    template_name = 'producao/importar_op_individual.html'
    form_class = ImportarOpIndividualForm
    success_url = reverse_lazy('producao:importar_op_individual')

    def form_valid(self, form):
        numero_op_str = form.cleaned_data['numero_op']
        tarja = form.cleaned_data.get('tarja') or None
        data_quimica = form.cleaned_data['data_quimica']
        
        # A variável 'cliente' foi removida.

        # Chama o serviço modificado, SEM passar o cliente_override.
        # A função import_ops_do_erp usará sua lógica interna para buscar o cliente.
        op_obj, erros = importar_ops_do_erp(
            op_especifica=numero_op_str,
            tarja=tarja,
            data_quimica=data_quimica
            # O parâmetro 'cliente_override' foi removido da chamada.
        )

        if not op_obj:
            messages.error(self.request, f'Não foi possível importar a OP {numero_op_str}. Verifique se o número está correto ou se ela já foi importada.')
            return super().form_valid(form)

        # --- LÓGICA DE VERIFICAÇÃO DO LOTE (permanece igual) ---
        try:
            formula_associada = op_obj.get_formulas().first()

            if not formula_associada:
                messages.warning(self.request, f"OP {op_obj.numero_op} importada, mas não foi possível encontrar uma fórmula química associada. Verifique a Ficha Técnica.")
                return super().form_valid(form)

            lote_ja_gerado = LoteQuimico.objects.filter(
                formula=formula_associada,
                data_programacao=data_quimica
            ).exists()

            if lote_ja_gerado:
                messages.warning(self.request, 
                    f"Atenção: OP {op_obj.numero_op} importada com sucesso para {data_quimica.strftime('%d/%m/%Y')}, "
                    f"mas o lote para a fórmula '{formula_associada.nome_formula}' neste dia JÁ FOI GERADO. "
                    f"A OP aparecerá como um item separado no painel da Química."
                )
            else:
                messages.success(self.request, 
                    f"OP {op_obj.numero_op} importada com sucesso e agendada para {data_quimica.strftime('%d/%m/%Y')}. "
                    f"Ela será agrupada com outras OPs da mesma fórmula quando o lote for gerado."
                )

        except Exception as e:
            messages.error(self.request, f"OP importada, mas ocorreu um erro ao verificar o lote: {e}")

        return super().form_valid(form)


# --- Views de Listagem e Detalhes (PCP) ---

class PcpPedidoDetalhesView(ListView):
    """ Exibe os detalhes das Ordens de Produção para um pedido específico no modal. """
    template_name = 'producao/partials/_pedido_detalhes_modal_content.html'
    context_object_name = 'ordens_producao'

    def get_queryset(self):
        numero_pedido = self.kwargs.get('numero_pedido')

        # <<< CORREÇÃO AQUI >>>
        # 1. O filtro foi ajustado para usar o relacionamento correto: demandas__pedido__numero_pedido.
        # 2. A anotação foi melhorada para SOMAR os valores dos itens, garantindo o total correto por OP.
        return OrdemProducao.objects.filter(
            demandas__pedido__numero_pedido=numero_pedido
        ).annotate(
            valor_total_op_no_pedido=Sum(
                # Multiplica a quantidade pelo preço de cada item de demanda
                F('demandas__quantidade_producao') * F('demandas__preco_venda'),
                # Garante que a soma inclua apenas os itens do pedido que estamos filtrando
                filter=Q(demandas__pedido__numero_pedido=numero_pedido)
            )
        ).order_by('numero_op').distinct()


class PcpListOrdemProducaoFinanView(ListView):
    """
    View refatorada para a Análise Financeira de Pedidos.
    - Utiliza os novos modelos Cliente e Representante.
    - Otimiza a consulta ao banco de dados.
    - Corrige a lógica de filtro e ordenação para o campo de cliente.
    """
    template_name = 'producao/pcp_list_ordem_producao_finan.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        # Otimiza a consulta inicial, já buscando os dados do cliente associado
        pedidos_qs = Pedido.objects.select_related('cliente').annotate(
            valor_total=Sum(
                F('itens__quantidade_producao') * F('itens__preco_venda'),
                output_field=DecimalField()
            ),
            total_ops=Count('itens__ordem_producao', distinct=True),
            ops_finalizadas=Count(
                'itens__ordem_producao',
                filter=Q(itens__ordem_producao__status=OrdemProducaoStatus.FINALIZADO),
                distinct=True
            )
        ).annotate(
            status_pedido=Case(
                When(ops_finalizadas=F('total_ops'), then=Value('FECHADO')),
                default=Value('PENDENTE'),
                output_field=CharField()
            )
        ).exclude(valor_total__isnull=True)

        # Lógica de filtro do formulário
        self.form = PcpListFinanFilterForm(self.request.GET or None)
        if self.form.is_valid():
            numero_pedido = self.form.cleaned_data.get('numero_pedido')
            cliente = self.form.cleaned_data.get('cliente')
            status = self.form.cleaned_data.get('status')
            
            if numero_pedido:
                pedidos_qs = pedidos_qs.filter(numero_pedido__icontains=numero_pedido)
            if cliente:
                # --- CORREÇÃO APLICADA AQUI ---
                # Filtra pelo nome do cliente através da relação ForeignKey
                pedidos_qs = pedidos_qs.filter(cliente__nome__icontains=cliente)
            if status:
                pedidos_qs = pedidos_qs.filter(status_pedido=status)
        
        # Lógica de Ordenação
        self.sort_param = self.request.GET.get('sort', '-numero_pedido')
        # --- CORREÇÃO APLICADA AQUI ---
        # Atualiza os campos válidos para ordenação
        valid_sort_fields = ['numero_pedido', '-numero_pedido', 'valor_total', '-valor_total', 'cliente__nome', '-cliente__nome']
        
        if self.sort_param in valid_sort_fields:
            return pedidos_qs.order_by(self.sort_param)
        
        return pedidos_qs.order_by('-numero_pedido')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['current_sort'] = self.sort_param
        
        query_params = self.request.GET.copy()
        if 'sort' in query_params:
            del query_params['sort']
        context['base_query_string'] = query_params.urlencode()
        return context

class DetalhesPedidoView(ListView):
    model = ItemDemandaProducao
    template_name = 'producao/partials/_detalhes_pedido_modal.html'
    context_object_name = 'itens_pedido'

    def get_queryset(self):
        numero_pedido_da_url = self.kwargs.get('numero_pedido')
        
        # <<< CORREÇÃO AQUI >>>
        # Acessa o numero_pedido através do relacionamento com o modelo Pedido.
        queryset = super().get_queryset().filter(
            pedido__numero_pedido=numero_pedido_da_url
        ).select_related('ordem_producao')
        
        return queryset

    # Opcional, mas recomendado: Adicionar o total ao contexto para o template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = sum(item.valor_total_item for item in self.object_list if item.valor_total_item is not None)
        context['valor_total_pedido'] = total
        return context


class PcpListOrdemProducaoView(ListView):
    """
    View refatorada para a lista de Ordens de Produção do PCP.
    - Otimiza a consulta para incluir dados do cliente.
    - Adiciona a lógica de filtro por nome do cliente.
    """
    template_name = 'producao/pcp_list_ordem_producao.html'
    context_object_name = 'ordens_producao'
    
    def get_queryset(self):
        # Otimiza a consulta pré-carregando os dados de cliente através dos relacionamentos
        ordens_qs = OrdemProducao.objects.all().prefetch_related(
            'demandas__pedido__cliente'
        ).order_by('-data_emissao', 'numero_op')
        
        self.form = PcpListFilterForm(self.request.GET or None)

        if self.form.is_valid():
            if self.form.cleaned_data.get('numero_op'):
                ordens_qs = ordens_qs.filter(numero_op__icontains=self.form.cleaned_data['numero_op'])
            
            if self.form.cleaned_data.get('numero_pedido'):
                ordens_qs = ordens_qs.filter(
                    demandas__pedido__numero_pedido__icontains=self.form.cleaned_data['numero_pedido']
                )

            # --- NOVA LÓGICA DE FILTRO ADICIONADA ---
            if self.form.cleaned_data.get('cliente'):
                ordens_qs = ordens_qs.filter(
                    demandas__pedido__cliente__nome__icontains=self.form.cleaned_data['cliente']
                )
            
            if self.form.cleaned_data.get('numero_agrupamento'):
                ordens_qs = ordens_qs.filter(numero_agrupamento__icontains=self.form.cleaned_data['numero_agrupamento'])
            if self.form.cleaned_data.get('data_inicio'):
                ordens_qs = ordens_qs.filter(data_emissao__gte=self.form.cleaned_data['data_inicio'])
            if self.form.cleaned_data.get('data_fim'):
                ordens_qs = ordens_qs.filter(data_emissao__lte=self.form.cleaned_data['data_fim'])

        # distinct() é crucial para evitar duplicatas ao filtrar por modelos relacionados
        return ordens_qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        
        # --- CORREÇÃO APLICADA AQUI ---
        # Prepara a string de clientes para cada OP, evitando a chamada ao método antigo no template.
        # Isso utiliza os dados já pré-carregados pelo prefetch_related, sendo muito eficiente.
        for op in context['ordens_producao']:
            clientes = {
                demanda.pedido.cliente.nome 
                for demanda in op.demandas.all() 
                if demanda.pedido and demanda.pedido.cliente
            }
            op.clientes_display = ', '.join(sorted(list(clientes))) or "-"

        return context
    
# Em producao/views.py
# --- Views de Filas de Produção por Setor ---

class ListaOpsQuimicaView(ListView):
    """ View para listar as OPs na fila da Química, com filtros corrigidos e otimizados. """
    template_name = 'producao/lista_ops_quimica.html'
    context_object_name = 'ordens_producao'
    paginate_by = 50

    def get_queryset(self):
        # 1. OTIMIZAÇÃO: Usamos prefetch_related para buscar os dados relacionados
        # (demandas, pedidos, clientes) de forma eficiente, evitando múltiplas
        # consultas ao banco de dados (problema N+1).
        queryset = OrdemProducao.objects.prefetch_related(
            'demandas__pedido__cliente'
        ).filter(
            status=OrdemProducaoStatus.PENDENTE,
            is_kanban=False
        ).order_by('data_qmc', 'tarja', 'numero_op')

        form = OpFilterForm(self.request.GET)

        if form.is_valid():
            # Filtros diretos no modelo OrdemProducao
            numero_op = form.cleaned_data.get('numero_op')
            if numero_op:
                queryset = queryset.filter(numero_op__icontains=numero_op)

            tamanho = form.cleaned_data.get('tamanho')
            if tamanho:
                queryset = queryset.filter(tamanho__icontains=tamanho)
            
            material = form.cleaned_data.get('material')
            if material:
                queryset = queryset.filter(material__icontains=material)

            # 2. CORREÇÃO: Filtros que atravessam as relações
            # OrdemProducao -> ItemDemandaProducao -> Pedido -> Cliente
            numero_pedido = form.cleaned_data.get('numero_pedido')
            if numero_pedido:
                # O caminho correto é via 'demandas' e depois 'pedido'
                queryset = queryset.filter(demandas__pedido__numero_pedido__icontains=numero_pedido)

            cliente = form.cleaned_data.get('cliente')
            if cliente:
                # O caminho correto para o nome do cliente
                queryset = queryset.filter(demandas__pedido__cliente__nome__icontains=cliente)
        
        # 3. IMPORTANTE: Adicionamos .distinct() para evitar que uma OP apareça
        # mais de uma vez na lista caso ela esteja em múltiplos pedidos que
        # correspondam ao filtro.
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setor_nome'] = 'Fila de Produção - Química'
        context['filter_form'] = OpFilterForm(self.request.GET or None)
        return context


class ListaOpsPastilhaView(ListView):
    """
    Exibe a fila de produção para o Controle de Pastilha, com abas para OPs de Cliente e Kanban.
    A aba de OPs de Cliente agora possui filtros.
    """
    template_name = 'producao/lista_ops_pastilha.html'
    context_object_name = 'ordens_producao'
    paginate_by = 30

    def get_queryset(self):
        """
        Este queryset agora foca APENAS na aba de OPs de Cliente.
        A query de Kanban será feita no get_context_data.
        """
        setor_pastilha = get_object_or_404(SetorModel, nome='Controle de Pastilha')

        base_qs = OrdemProducao.objects.filter(
            Q(status=OrdemProducaoStatus.AGUARDANDO_PASTILHA) |
            Q(status=OrdemProducaoStatus.EM_PRODUCAO, transferencias__setor_origem=setor_pastilha)
        ).prefetch_related(
            'demandas__pedido__cliente', 'reprogramacoes', 'transferencias'
        ).distinct()

        form = OpFilterForm(self.request.GET)
        if form.is_valid():
            numero_op = form.cleaned_data.get('numero_op')
            if numero_op:
                base_qs = base_qs.filter(numero_op__icontains=numero_op)

            tamanho = form.cleaned_data.get('tamanho')
            if tamanho:
                base_qs = base_qs.filter(tamanho__icontains=tamanho)
            
            material = form.cleaned_data.get('material')
            if material:
                base_qs = base_qs.filter(material__icontains=material)

            numero_pedido = form.cleaned_data.get('numero_pedido')
            if numero_pedido:
                base_qs = base_qs.filter(demandas__pedido__numero_pedido__icontains=numero_pedido)

            cliente = form.cleaned_data.get('cliente')
            if cliente:
                base_qs = base_qs.filter(demandas__pedido__cliente__nome__icontains=cliente)
        
        return base_qs.order_by('tarja', 'data_emissao', 'numero_op')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setor_pastilha = get_object_or_404(SetorModel, nome='Controle de Pastilha')
        
        active_tab = self.request.GET.get('tab', 'ops_cliente')
        
        ordens_para_exibir = []
        for op in context['ordens_producao']:
            # --- LÓGICA CORRIGIDA ADICIONADA AQUI ---
            # Prepara as strings de cliente e pedido para exibição, evitando o método quebrado do model.
            clientes = {d.pedido.cliente.nome for d in op.demandas.all() if d.pedido and d.pedido.cliente}
            op.clientes_display = ', '.join(sorted(list(clientes))) or "-"

            pedidos = {d.pedido.numero_pedido for d in op.demandas.all() if d.pedido}
            op.pedidos_display = ', '.join(sorted(list(pedidos))) or "-"
            # --- FIM DA LÓGICA ADICIONADA ---

            op.is_reprogramacao = op.reprogramacoes.exists()
            op.total_transferido = sum(
                t.peso_transferido for t in op.transferencias.all() if t.setor_origem_id == setor_pastilha.id
            )
            
            peso_previsto_original = op.peso_previsto or decimal.Decimal('0.0')
            saldo_real_da_tarefa = decimal.Decimal('0.0')

            if op.is_reprogramacao:
                latest_reprogramacao = max(op.reprogramacoes.all(), key=lambda r: r.data_reprogramacao, default=None)
                if latest_reprogramacao:
                    transferencias_relevantes = [
                        t.peso_transferido for t in op.transferencias.all()
                        if t.setor_origem_id == setor_pastilha.id and t.data_transferencia >= latest_reprogramacao.data_reprogramacao
                    ]
                    transferido_para_reprogramacao = sum(transferencias_relevantes)
                    saldo_real_da_tarefa = latest_reprogramacao.peso_reprogramado - transferido_para_reprogramacao
                    
                    if op.peso_bruto_grosa and op.peso_bruto_grosa > 0:
                        op.total_grosas_reprogramadas = latest_reprogramacao.peso_reprogramado / (op.peso_bruto_grosa / 1000)
                    else:
                        op.total_grosas_reprogramadas = 0
            else:
                saldo_real_da_tarefa = peso_previsto_original - op.total_transferido
            
            op.saldo_pendente = saldo_real_da_tarefa
            
            if saldo_real_da_tarefa > decimal.Decimal('0.0001'):
                ordens_para_exibir.append(op)

        solicitacoes_kanban = SolicitacaoReposicaoKanban.objects.filter(
            status=SolicitacaoReposicaoKanban.Status.AGUARDANDO_PASTILHA
        ).select_related('item_estoque').order_by('data_solicitacao')

        context['setor_nome'] = 'Controle de Pastilha'
        context['filter_form'] = OpFilterForm(self.request.GET or None)
        context['active_tab'] = active_tab
        context['ordens_producao_processadas'] = ordens_para_exibir
        context['solicitacoes_kanban'] = solicitacoes_kanban
        
        return context


# --- Views de Apontamento ---

class ApontamentoPastilhaView(View):
    """
    View para o apontamento no setor de Controle de Pastilha.
    Refatorada para buscar e exibir os dados do cliente corretamente.
    """
    template_name = 'producao/apontamento_pastilha.html'
    
    def get_setor_pastilha(self):
        setor, _ = SetorModel.objects.get_or_create(nome='ESCOLHA PASTILHA')
        return setor

    def get(self, request, op_id):
        # --- CONSULTA CORRIGIDA ---
        # Otimiza a busca da OP, já carregando os dados do cliente.
        op = get_object_or_404(
            OrdemProducao.objects.prefetch_related('demandas__pedido__cliente'), 
            pk=op_id
        )
        context = self._get_common_context(op)
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, op_id):
        # A lógica do POST permanece a mesma.
        op = get_object_or_404(OrdemProducao, pk=op_id)
        saldo_pendente = self._get_saldo_pendente(op)
        
        form = ControlePastilhaForm(request.POST, saldo_maximo=saldo_pendente, ordem_producao=op)

        if form.is_valid():
            apontamento = form.save(commit=False)
            apontamento.ordem_producao = op
            
            peso_medido = form.cleaned_data.get('peso')
            proximo_setor_obj = form.cleaned_data.get('proximo_setor')
            
            peso_10_botoes = form.cleaned_data.get('peso_10_botoes')
            if peso_10_botoes and peso_10_botoes > 0:
                peso_bruto_grosa = (peso_10_botoes / 10) * 144
                op.peso_bruto_grosa = peso_bruto_grosa
                op.save(update_fields=['peso_bruto_grosa'])
                if peso_medido and peso_bruto_grosa > 0:
                    apontamento.quantidade_grosas = (peso_medido * 1000) / peso_bruto_grosa

            now = timezone.now()
            apontamento.data_hora_inicio = now
            apontamento.data_hora_fim = now
            apontamento.save()

            setor_origem = self.get_setor_pastilha()
            
            TransferenciaEntreSetores.objects.create(
                ordem_producao=op,
                setor_origem=setor_origem,
                setor_destino=proximo_setor_obj,
                peso_transferido=peso_medido,
                responsavel=apontamento.responsavel
            )

            saldo_destino, _ = SaldoOPSetor.objects.get_or_create(
                ordem_producao=op,
                setor=proximo_setor_obj
            )
            saldo_destino.saldo_peso = F('saldo_peso') + peso_medido
            saldo_destino.save()
            
            if op.status != OrdemProducaoStatus.EM_PRODUCAO:
                op.status = OrdemProducaoStatus.EM_PRODUCAO
                op.save(update_fields=['status'])
            
            messages.success(request, f'Apontamento de {peso_medido} Kg para a OP {op.numero_op} salvo e transferido para {proximo_setor_obj.nome}.')
            
            if self._get_saldo_pendente(op) <= 0:
                messages.info(request, f"Todo o peso previsto para a OP {op.numero_op} foi medido e transferido.")
                return redirect('producao:lista_ops_pastilha')

            return redirect('producao:apontamento_pastilha', op_id=op.pk)
        
        context = self._get_common_context(op)
        context['form'] = form
        return render(request, self.template_name, context)

    def _get_saldo_pendente(self, op):
        setor_pastilha = self.get_setor_pastilha()
        
        total_transferido = TransferenciaEntreSetores.objects.filter(
            ordem_producao=op,
            setor_origem=setor_pastilha
        ).aggregate(
            total=Coalesce(Sum('peso_transferido'), decimal.Decimal('0.0'), output_field=DecimalField())
        )['total']
        
        peso_previsto = op.peso_previsto or decimal.Decimal('0.0')
        saldo_pendente = peso_previsto - total_transferido
        return saldo_pendente

    def get_setor_recomendado(self, op):
        if op.is_kanban:
            setor, _ = SetorModel.objects.get_or_create(nome='Kanban')
        else:
            setor, _ = SetorModel.objects.get_or_create(nome='Tornos')
        return setor

    def _get_common_context(self, op):
        saldo_pendente = self._get_saldo_pendente(op)
        total_transferido = (op.peso_previsto or 0) - saldo_pendente
        apontamentos_anteriores = ControlePastilha.objects.filter(ordem_producao=op).order_by('-data_hora_fim')

        # --- LÓGICA ADICIONADA PARA CLIENTE E PEDIDO ---
        clientes = {d.pedido.cliente.nome for d in op.demandas.all() if d.pedido and d.pedido.cliente}
        pedidos = {d.pedido.numero_pedido for d in op.demandas.all() if d.pedido}

        return {
            'ordem_producao': op,
            'form': ControlePastilhaForm(
                initial={'proximo_setor': self.get_setor_recomendado(op)},
                saldo_maximo=saldo_pendente,
                ordem_producao=op
            ),
            'reprogramacao_form': ReprogramacaoForm(
                ordem_producao=op
            ),
            'setor_nome': 'Controle de Pastilha',
            'saldo_pendente': saldo_pendente,
            'total_transferido': total_transferido,
            'apontamentos_anteriores': apontamentos_anteriores,
            'clientes_display': ', '.join(sorted(list(clientes))) or "-",
            'pedidos_display': ', '.join(sorted(list(pedidos))) or "-",
        }
        

class ApontamentoQuimicaView(DetailView):
    """
    Exibe a "papeleta digital" para o setor de Química no padrão Class-Based View.
    """
    model = OrdemProducao
    template_name = 'producao/apontamento_quimica.html'
    context_object_name = 'ordem_producao'  # Nome do objeto no template
    pk_url_kwarg = 'op_id'  # Informa que o ID na URL vem como 'op_id'

    def get_context_data(self, **kwargs):
        # 1. Inicia o contexto chamando o método da classe pai
        context = super().get_context_data(**kwargs)
        
        # O objeto 'ordem_producao' já está no contexto, mas o pegamos para trabalhar com ele
        op = self.get_object()

        # 2. Toda a lógica de cálculo da receita é movida para cá
        receitas_calculadas = op.get_receita_calculada()
        receitas_para_template = {}
        total_receita_geral = decimal.Decimal('0.0')

        if receitas_calculadas:
            codigos_componentes = set()
            for dados_camada in receitas_calculadas.values():
                for componente in dados_camada.get('receita', []):
                    codigos_componentes.add(componente['codigo_componente'])
            
            nomes_map = {}
            if codigos_componentes:
                produtos_erp = Pro01.objects.using('acedata').filter(procod__in=list(codigos_componentes)).values('procod', 'pronom')
                nomes_map = {p['procod'].strip(): p['pronom'].strip() for p in produtos_erp}
            
            for nome_camada, dados_camada in receitas_calculadas.items():
                total_camada = sum(c.get('quantidade_necessaria', 0) for c in dados_camada.get('receita', []))
                
                for componente in dados_camada.get('receita', []):
                    codigo = componente['codigo_componente']
                    componente['nome_componente'] = nomes_map.get(codigo, f'NOME NÃO ENCONTRADO ({codigo})')
                
                dados_camada['total_camada'] = round(total_camada, 4)
                total_receita_geral += dados_camada['total_camada']
                
                nome_formatado = nome_camada.replace('_', ' ').title()
                receitas_para_template[nome_formatado] = dados_camada
        else:
            messages.warning(self.request, f"A OP {op.numero_op} não possui uma fórmula química associada ou os dados para cálculo estão incompletos.")

        # 3. ===== NOVO: CÁLCULO DA QUANTIDADE TOTAL DO PEDIDO =====
        # Soma a quantidade de todas as demandas de cliente vinculadas a esta OP
        quantidade_total_pedido = op.demandas.aggregate(
            total=Sum('quantidade')
        )['total'] or decimal.Decimal('0.0')

        # 4. Adiciona os dados processados ao contexto final
        context['receitas_por_camada'] = receitas_para_template
        context['total_receita_geral'] = round(total_receita_geral, 4)
        context['quantidade_total_pedido'] = quantidade_total_pedido # <--- Adiciona ao contexto
        context['setor_nome'] = 'Apontamento de Química'
        
        return context


class PainelQuimicaView(TemplateView):
    template_name = 'producao/painel_quimica.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # --- 1. BUSCA POR RETRABALHOS PENDENTES (Lógica completa preservada) ---
        reprogramacoes_pendentes_qs = ReprogramacaoOP.objects.filter(
            ordem_producao__status=OrdemProducaoStatus.PENDENTE
        ).select_related('ordem_producao', 'motivo').order_by('-data_reprogramacao')

        reprogramacoes_para_template = []
        op_ids_em_retrabalho = set()

        for repro in reprogramacoes_pendentes_qs:
            op = repro.ordem_producao
            op_ids_em_retrabalho.add(op.id)
            
            grosas_reprogramadas = decimal.Decimal('0.0')
            if repro.peso_reprogramado and op.peso_bruto_grosa and op.peso_bruto_grosa > 0:
                peso_bruto_grosa_kg = op.peso_bruto_grosa / 1000
                grosas_reprogramadas = repro.peso_reprogramado / peso_bruto_grosa_kg
            
            reprogramacoes_para_template.append({
                'reprogramacao': repro,
                'ordem_producao': op,
                'grosas_reprogramadas': grosas_reprogramadas
            })
        
        context['reprogramacoes_pendentes'] = reprogramacoes_para_template

        # --- 2. BUSCA POR LOTES NORMAIS DE CLIENTES (Lógica completa preservada) ---
        ops_agendadas = OrdemProducao.objects.filter(
            status=OrdemProducaoStatus.PENDENTE,
            data_qmc__isnull=False,
            is_kanban=False
        ).exclude(
            id__in=op_ids_em_retrabalho
        ).prefetch_related('formulas_por_camada__formula').order_by('data_qmc', 'sequencia_pcp')

        grouped_by_date = defaultdict(lambda: defaultdict(lambda: {
            'ops': set(), 'formula_obj': None, 'total_necessario': decimal.Decimal('0.0')
        }))

        for op in ops_agendadas:
            receita_op = op.get_receita_calculada()
            if not receita_op:
                continue

            for camada_data in receita_op.values():
                formula = camada_data['formula']
                peso_alvo = camada_data['peso_alvo']
                group = grouped_by_date[op.data_qmc][formula.id]
                group['ops'].add(op)
                if not group['formula_obj']:
                    group['formula_obj'] = formula
                group['total_necessario'] += peso_alvo

        datas_programadas = grouped_by_date.keys()
        lotes_existentes = set()
        if datas_programadas:
            lotes_qs = LoteQuimico.objects.filter(data_programacao__in=datas_programadas)
            lotes_existentes = {(lote.data_programacao, lote.formula_id) for lote in lotes_qs}

        programacao_pendente_dict = {}
        for data, formulas_do_dia in grouped_by_date.items():
            lotes_pendentes_neste_dia = {}
            for formula_id, group_data in formulas_do_dia.items():
                if (data, formula_id) not in lotes_existentes:
                    group_data['lote_status'] = 'Pendente para Gerar'
                    lotes_pendentes_neste_dia[formula_id] = group_data
            
            if lotes_pendentes_neste_dia:
                programacao_pendente_dict[data] = lotes_pendentes_neste_dia
        
        programacao_diaria_lista = sorted(programacao_pendente_dict.items())
        
        paginator = Paginator(programacao_diaria_lista, 1)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['lotes_gerados'] = LoteQuimico.objects.select_related('formula').order_by('-data_programacao', 'formula__nome_formula')
        context['today'] = timezone.now().date()
        
        # --- 3. NOVA LÓGICA PARA SOLICITAÇÕES DE REPOSIÇÃO KANBAN (ESTOQUE) ---
        solicitacoes_reposicao = SolicitacaoReposicaoKanban.objects.filter(
            status=SolicitacaoReposicaoKanban.Status.PENDENTE
        ).select_related(
            'item_estoque', 
            'solicitado_por'
        ).order_by('data_solicitacao')

        context['solicitacoes_reposicao_kanban'] = solicitacoes_reposicao
        
        # --- 4. LÓGICA ANTIGA PARA DEMANDAS KANBAN (VINCULADAS A OP) ---
        # Mantida para compatibilidade com o template atual. Pode ser removida no futuro.
        context['solicitacoes_kanban'] = SolicitacaoQuimicaKanban.objects.filter(
            status=SolicitacaoQuimicaKanban.Status.PENDENTE
        ).select_related('ordem_producao', 'solicitado_por').order_by('data_solicitacao')

        return context

class GerarLoteQuimicoView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        formula_id = kwargs.get('formula_id')
        formula = get_object_or_404(FormulaQuimica, id=formula_id)
        
        data_qmc_str = request.POST.get('data_qmc')
        if not data_qmc_str:
            messages.error(request, "Data de programação não informada.")
            return redirect('producao:painel_quimica')

        data_qmc = timezone.datetime.strptime(data_qmc_str, '%Y-%m-%d').date()

        ops_do_grupo = OrdemProducao.objects.filter(
            status=OrdemProducaoStatus.PENDENTE,
            data_qmc=data_qmc,
            formulas_por_camada__formula=formula
        ).distinct()

        if not ops_do_grupo.exists():
            messages.error(request, "Nenhuma OP pendente encontrada para este grupo.")
            return redirect('producao:painel_quimica')

        total_necessario = sum(
            camada_data['peso_alvo']
            for op in ops_do_grupo
            for camada_data in op.get_receita_calculada().values()
            if camada_data['formula'].id == formula.id
        )

        lote, created = LoteQuimico.objects.get_or_create(
            formula=formula,
            data_programacao=data_qmc,
            defaults={'quantidade_total_necessaria': total_necessario}
        )

        if created:
            lote.ordens_producao.set(ops_do_grupo)
            messages.success(request, f"Lote para a fórmula {formula.nome_formula} (prog. {data_qmc.strftime('%d/%m')}) gerado com sucesso.")
        else:
            messages.warning(request, f"O lote para a fórmula {formula.nome_formula} (prog. {data_qmc.strftime('%d/%m')}) já existia.")

        # --- LÓGICA DE VERIFICAÇÃO MOVIDA PARA CÁ ---
        # Após gerar o lote, verifica se alguma OP associada a ele está completa.
        ops_liberadas_pks = []
        for op in ops_do_grupo:
            # 1. Pega todas as fórmulas que a OP precisa.
            formulas_necessarias_ids = set(op.formulas_por_camada.values_list('formula_id', flat=True))
            
            # 2. Pega todas as fórmulas dos lotes JÁ GERADOS para esta OP.
            lotes_gerados_op = LoteQuimico.objects.filter(ordens_producao=op)
            formulas_geradas_ids = set(lotes_gerados_op.values_list('formula_id', flat=True))

            # 3. Se todas as fórmulas necessárias já têm um lote gerado, a OP está pronta.
            if formulas_necessarias_ids.issubset(formulas_geradas_ids):
                ops_liberadas_pks.append(op.pk)

        # 4. Atualiza o status de todas as OPs prontas de uma só vez.
        if ops_liberadas_pks:
            OrdemProducao.objects.filter(pk__in=ops_liberadas_pks).update(status=OrdemProducaoStatus.EM_PRODUCAO)
            messages.info(request, f"{len(ops_liberadas_pks)} OP(s) foram liberadas para o Lançamento no Cilindro.")

        return redirect('producao:painel_quimica')

class CancelarLoteQuimicoView(View):
    """
    Processa o cancelamento de um Lote Químico, com uma trava de segurança
    para impedir o cancelamento se a produção já foi iniciada.
    """
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        lote_id = kwargs.get('lote_id')
        lote = get_object_or_404(LoteQuimico, id=lote_id)

        # --- TRAVA DE SEGURANÇA CORRIGIDA ---
        # Pega todas as Ordens de Produção associadas a este Lote Químico.
        ops_do_lote = lote.ordens_producao.all()

        # Verifica se existe algum LancamentoCilindro cujo agrupamento contenha
        # QUALQUER UMA das OPs deste lote.
        if LancamentoCilindro.objects.filter(agrupamento__ordens_producao__in=ops_do_lote).exists():
            messages.error(request, f"Não é possível cancelar o lote para a fórmula {lote.formula.nome_formula}, pois já existem lançamentos de produção associados a uma ou mais de suas OPs.")
            return redirect('producao:painel_quimica')

        # Se não houver lançamentos, prossegue com o cancelamento.
        try:
            # Reverte o status das OPs associadas de volta para PENDENTE
            # A variável ops_do_lote já foi definida acima, então podemos reutilizá-la.
            ops_do_lote.update(status=OrdemProducaoStatus.PENDENTE)

            formula_nome = lote.formula.nome_formula
            data_prog = lote.data_programacao.strftime('%d/%m/%Y')

            # Deleta o lote químico
            lote.delete()

            messages.success(request, f"Lote para a fórmula {formula_nome} (prog. {data_prog}) foi cancelado. As OPs vinculadas estão pendentes novamente.")

        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao tentar cancelar o lote: {e}")

        return redirect('producao:painel_quimica')

class MarcarLoteProduzidoView(View):
    """
    Processa a AÇÃO de marcar um Lote Químico como PRODUZIDO.
    Esta ação agora apenas atualiza o status do lote, sem alterar o status da OP.
    """
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        formula_id = kwargs.get('formula_id')
        data_qmc_str = request.POST.get('data_qmc')
        if not data_qmc_str:
            messages.error(request, "Data de programação não informada.")
            return redirect('producao:painel_quimica')

        data_qmc = timezone.datetime.strptime(data_qmc_str, '%Y-%m-%d').date()
        
        lote = get_object_or_404(LoteQuimico, formula_id=formula_id, data_programacao=data_qmc)
        
        if lote.status == LoteQuimico.Status.PENDENTE:
            lote.status = LoteQuimico.Status.PRODUZIDO
            lote.data_producao = timezone.now()
            lote.save()
            messages.success(request, f"Lote da fórmula {lote.formula.nome_formula} marcado como PRODUZIDO.")
            
            # --- LÓGICA DE LIBERAÇÃO DE OP REMOVIDA DAQUI ---
            # A verificação agora acontece no momento da GERAÇÃO do último lote.

        else:
            messages.info(request, "Este lote já estava marcado como produzido.")
            
        return redirect('producao:painel_quimica')
    
class ReceitaAgrupadaView(LoginRequiredMixin, TemplateView):
    """
    Calcula e exibe a receita agregada para uma fórmula específica em uma data programada,
    no mesmo formato da papeleta de produção.
    """
    template_name = 'producao/receita_agrupada.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formula_id = self.kwargs.get('formula_id')
        data_str = self.kwargs.get('data_programacao')

        try:
            data_programacao = datetime.strptime(data_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(self.request, "Formato de data inválido ou ausente.")
            return context

        formula = get_object_or_404(FormulaQuimica, id=formula_id)

        # 1. Encontra todas as OPs do grupo
        ops_do_grupo = OrdemProducao.objects.filter(
            status=OrdemProducaoStatus.PENDENTE,
            data_qmc=data_programacao,
            formulas_por_camada__formula=formula
        ).distinct()

        if not ops_do_grupo:
            messages.warning(self.request, "Nenhuma OP encontrada para este grupo com os filtros aplicados.")
            context['formula'] = formula
            context['data_programacao'] = data_programacao
            return context

        # 2. Calcula a receita agregada
        componentes_agregados = defaultdict(decimal.Decimal)
        peso_total_alvo = decimal.Decimal('0.0')

        for op in ops_do_grupo:
            # O método get_receita_calculada() da OP é o responsável por calcular os pesos
            receita_op = op.get_receita_calculada() 
            for camada_data in receita_op.values():
                if camada_data.get('formula') and camada_data['formula'].id == formula_id:
                    peso_total_alvo += camada_data.get('peso_alvo', 0)
                    for componente in camada_data.get('receita', []):
                        codigo = componente['codigo_componente']
                        componentes_agregados[codigo] += componente.get('quantidade_necessaria', 0)

        # 3. Busca os nomes dos componentes do ERP
        codigos = list(componentes_agregados.keys())
        produtos_erp = Pro01.objects.using('acedata').filter(procod__in=codigos).values('procod', 'pronom')
        nomes_map = {p['procod'].strip(): p['pronom'].strip() for p in produtos_erp}

        # 4. Busca a receita base (para 1kg) da fórmula
        # --- CORREÇÃO ---
        # Acessa os componentes diretamente da fórmula e cria um mapa com os dados corretos.
        base_componentes = formula.componentes.all()
        base_receita_map = {
            comp.componente_codigo.strip(): comp.componente_qtd_base
            for comp in base_componentes
        }

        # 5. Monta a lista final para o template, incluindo a receita base
        receita_final = []
        total_geral_g = decimal.Decimal('0.0')
        for codigo, quantidade_total in componentes_agregados.items():
            total_geral_g += quantidade_total
            receita_final.append({
                'codigo': codigo,
                'nome': nomes_map.get(codigo, f'NOME NÃO ENCONTRADO ({codigo})'),
                'quantidade_por_kg': base_receita_map.get(codigo, decimal.Decimal('0.0')), # Busca a quantidade base no mapa
                'quantidade_total_g': quantidade_total
            })
            
        context['formula'] = formula
        context['data_programacao'] = data_programacao
        context['peso_total_alvo'] = round(peso_total_alvo, 3)
        context['receita_agrupada'] = sorted(receita_final, key=lambda x: x['codigo'])
        context['total_geral_g'] = round(total_geral_g, 3)
        context['ops_do_grupo'] = ops_do_grupo
        
        return context
    
# View de Conferencia do PCP
class PainelConferenciaPCPView(View):
    """
    View refatorada para o Painel de Conferência do PCP.
    - Adiciona filtros para a lista de pedidos pendentes.
    - Corrige a lógica de atualização do modal.
    """
    template_name = 'producao/painel_conferencia_pcp.html'

    def get(self, request, *args, **kwargs):
        # --- LÓGICA DE FILTRAGEM ADICIONADA ---
        filter_form = OpFilterForm(request.GET or None)
        
        pedido_ids_pendentes = ItemDemandaProducao.objects.filter(
            ordem_producao__status=OrdemProducaoStatus.PENDENTE_CONFERENCIA
        ).values_list('pedido_id', flat=True).distinct()

        pedidos_pendentes = Pedido.objects.select_related('cliente').filter(
            id__in=pedido_ids_pendentes
        )

        if filter_form.is_valid():
            numero_pedido = filter_form.cleaned_data.get('numero_pedido')
            if numero_pedido:
                pedidos_pendentes = pedidos_pendentes.filter(numero_pedido__icontains=numero_pedido)
            
            cliente = filter_form.cleaned_data.get('cliente')
            if cliente:
                pedidos_pendentes = pedidos_pendentes.filter(cliente__nome__icontains=cliente)

        pedidos_pendentes = pedidos_pendentes.order_by('numero_pedido')
        # --- FIM DA LÓGICA DE FILTRAGEM ---

        context = {
            'pedidos_pendentes': pedidos_pendentes,
            'pedido_selecionado_obj': None,
            'itens_do_pedido': None,
            'numero_pedido_selecionado': None,
            'form_modal': PCPConferenciaItemUpdateForm(),
            'tarja_choices': OrdemProducao.TARJA_CHOICES,
            'filter_form': filter_form, # Passa o formulário para o template
        }

        numero_pedido_selecionado = kwargs.get('numero_pedido')
        if numero_pedido_selecionado:
            pedido_obj = get_object_or_404(
                Pedido.objects.select_related('cliente__representante'), 
                numero_pedido=numero_pedido_selecionado
            )

            itens_do_pedido = ItemDemandaProducao.objects.filter(
                pedido=pedido_obj,
                ordem_producao__status=OrdemProducaoStatus.PENDENTE_CONFERENCIA
            ).select_related(
                'ordem_producao', 
                'pedido__cliente'
            ).order_by('item_pedido_erp')
            
            total_pedido = itens_do_pedido.aggregate(
                total_qtd=Sum('quantidade')
            )['total_qtd'] or 0
            
            observacoes_ft = {
                item.ordem_producao.observacao_ficha_tecnica 
                for item in itens_do_pedido if item.ordem_producao.observacao_ficha_tecnica
            }
            observacoes_material = {
                item.ordem_producao.observacao_material 
                for item in itens_do_pedido if item.ordem_producao.observacao_material
            }
            observacoes_item = {
                item.observacao_item_pedido 
                for item in itens_do_pedido if item.observacao_item_pedido
            }

            context.update({
                'pedido_selecionado_obj': pedido_obj,
                'itens_do_pedido': itens_do_pedido,
                'numero_pedido_selecionado': numero_pedido_selecionado,
                'total_quantidade_pedido': total_pedido,
                'observacao_geral_pedido': pedido_obj.observacao_detalhada,
                'observacoes_ficha_tecnica': list(observacoes_ft),
                'observacoes_material': list(observacoes_material),
                'observacoes_item_pedido': list(observacoes_item),
            })

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # A lógica do POST permanece a mesma, pois a correção do modal é feita no frontend (JS)
        numero_pedido_confirmado = kwargs.get('numero_pedido')
        if not numero_pedido_confirmado:
            messages.error(request, "Nenhum pedido selecionado para confirmação.")
            return redirect('producao:pcp_conferencia')

        op_ids_enviados = set(request.POST.getlist('op_id'))

        for op_id in op_ids_enviados:
            try:
                op = OrdemProducao.objects.get(pk=op_id)
                op.observacao_op = request.POST.get(f'observacao_op_{op_id}', op.observacao_op)
                op.tarja = request.POST.get(f'tarja_{op_id}', op.tarja)
                data_qmc_str = request.POST.get(f'data_qmc_{op_id}')
                if data_qmc_str:
                    op.data_qmc = data_qmc_str
                
                requer_tingimento_val = request.POST.get(f'requer_tingimento_{op_id}')
                op.requer_tingimento = requer_tingimento_val == 'on'
                
                op.save()
            except OrdemProducao.DoesNotExist:
                messages.warning(request, f"OP com ID {op_id} não encontrada durante a confirmação.")
                continue

        itens_para_confirmar = ItemDemandaProducao.objects.filter(
            pedido__numero_pedido=numero_pedido_confirmado,
            ordem_producao__status=OrdemProducaoStatus.PENDENTE_CONFERENCIA
        )

        if not itens_para_confirmar.exists():
            messages.warning(request, f"O pedido {numero_pedido_confirmado} não tem mais itens pendentes de conferência.")
            return redirect('producao:pcp_conferencia')

        op_ids_para_liberar = {item.ordem_producao_id for item in itens_para_confirmar}
        
        ops_a_liberar = OrdemProducao.objects.filter(id__in=op_ids_para_liberar)
        ops_a_liberar.filter(is_kanban=True).update(status=OrdemProducaoStatus.EM_PRODUCAO)
        ops_a_liberar.filter(is_kanban=False).update(status=OrdemProducaoStatus.PENDENTE)

        itens_para_confirmar.update(
            conferido_por=request.user,
            conferido_em=timezone.now()
        )

        messages.success(request, f"Pedido {numero_pedido_confirmado} conferido! OPs liberadas para os setores de produção.")
        return redirect('producao:pcp_conferencia')

    
class OrdemProducaoPCPUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para a edição de uma Ordem de Produção pelo PCP.
    - Utiliza o formulário unificado 'PCPConferenciaItemUpdateForm'.
    - Otimiza a consulta para buscar todos os dados relacionados de uma vez.
    """
    model = OrdemProducao
    form_class = PCPConferenciaItemUpdateForm
    template_name = 'producao/ordem_producao_pcp_editar.html'
    context_object_name = 'ordem_producao'
    
    def get_form(self, form_class=None):
        """
        Sobrescreve o método para customizar o formulário.
        Adiciona o formato correto ao widget de data para garantir que o HTML o renderize.
        """
        form = super().get_form(form_class)
        form.fields['data_qmc'].widget.format = '%Y-%m-%d'
        return form

    def get_context_data(self, **kwargs):
        """
        Adiciona dados extras ao contexto, como o título da página e a lista
        de itens de demanda otimizada.
        """
        context = super().get_context_data(**kwargs)
        op = self.get_object()
        context['page_title'] = f"Ajustes PCP | OP {op.numero_op}"
        
        # Otimiza a consulta, incluindo todos os dados relacionados necessários para o template
        context['itens_demanda'] = op.demandas.select_related(
            'pedido__cliente'
        ).all()
        
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Ordem de Produção {self.object.numero_op} atualizada com sucesso!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('producao:pcp_list_ordem_producao')

    
class PainelSelecaoOPLancamentoView(ListView):
    """
    Painel refatorado para a Química, mostrando em abas separadas as OPs de Cliente
    e as Solicitações Kanban que estão prontas para iniciar o lançamento.
    """
    template_name = 'producao/painel_quimica_lancamento_selecao_op.html'
    context_object_name = 'ordens_para_iniciar' # Foco na lista de OPs
    paginate_by = 20

    def get_queryset(self):
        # --- CORREÇÃO 1: LÓGICA DE FILTRAGEM E ANOTAÇÃO ---
        # Subquery para verificar se existe algum lançamento em andamento (não finalizado)
        # associado a uma OP através de seu agrupamento.
        lancamento_em_andamento = LancamentoCilindro.objects.filter(
            agrupamento__ordens_producao=OuterRef('pk'),
            data_hora_fim__isnull=True
        )

        # A query base agora filtra apenas pelo status 'EM_PRODUCAO'.
        # A OP só sairá desta lista quando seu status for alterado (ex: para AGUARDANDO_CORTE).
        base_qs = OrdemProducao.objects.filter(
            status=OrdemProducaoStatus.EM_PRODUCAO,
            is_kanban=False
        ).annotate(
            # Anotação para exibir o total já produzido (incluindo lançamentos não finalizados)
            quantidade_grosas_produzida_agg=Coalesce(Sum('contribuicoes_op__quantidade_grosas_produzida'), decimal.Decimal('0.0'), output_field=DecimalField()),
            # Anotação para calcular o total de retrabalho
            total_grosas_reprogramadas=Coalesce(Sum((F('reprogramacoes__peso_reprogramado') / (F('peso_bruto_grosa') / 1000)), filter=Q(reprogramacoes__ordem_producao__status=OrdemProducaoStatus.EM_PRODUCAO)), decimal.Decimal('0.0'), output_field=DecimalField()),
            # Anotação para o marcador visual 'Processando'
            tem_lancamento_em_andamento=Exists(lancamento_em_andamento)
        ).annotate(
            # Anotação para o cálculo do alvo total
            quantidade_total_alvo=F('quantidade_programada_total') + F('total_grosas_reprogramadas')
        )
        
        ops_para_produzir_qs = base_qs.prefetch_related(
            'demandas__pedido__cliente', 'agrupamentos'
        ).distinct().order_by('data_qmc', 'sequencia_pcp')

        # Aplica filtros do formulário
        if self.request.GET.get('tab', 'ops_cliente') == 'ops_cliente':
            form = OpFilterForm(self.request.GET)
            if form.is_valid():
                numero_op = form.cleaned_data.get('numero_op')
                if numero_op: ops_para_produzir_qs = ops_para_produzir_qs.filter(numero_op__icontains=numero_op)
                tamanho = form.cleaned_data.get('tamanho')
                if tamanho: ops_para_produzir_qs = ops_para_produzir_qs.filter(tamanho__icontains=tamanho)
                material = form.cleaned_data.get('material')
                if material: ops_para_produzir_qs = ops_para_produzir_qs.filter(material__icontains=material)
                numero_pedido = form.cleaned_data.get('numero_pedido')
                if numero_pedido: ops_para_produzir_qs = ops_para_produzir_qs.filter(demandas__pedido__numero_pedido__icontains=numero_pedido)
                cliente = form.cleaned_data.get('cliente')
                if cliente: ops_para_produzir_qs = ops_para_produzir_qs.filter(demandas__pedido__cliente__nome__icontains=cliente)

        return ops_para_produzir_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Processa as OPs para calcular saldos e dados de exibição
        for op in context['ordens_para_iniciar']:
            op.saldo = op.quantidade_total_alvo - op.quantidade_grosas_produzida_agg
            op.is_retrabalho = op.total_grosas_reprogramadas > 0
            
            clientes = {d.pedido.cliente.nome for d in op.demandas.all() if d.pedido and d.pedido.cliente}
            op.clientes_display = ', '.join(sorted(list(clientes))) or "-"
            
            pedidos = {d.pedido.numero_pedido for d in op.demandas.all() if d.pedido}
            op.pedidos_display = ', '.join(sorted(list(pedidos))) or "-"

        # Query para a aba de Kanban
        context['solicitacoes_kanban'] = SolicitacaoReposicaoKanban.objects.filter(
            status=SolicitacaoReposicaoKanban.Status.EM_PRODUCAO
        ).select_related('item_estoque').order_by('data_solicitacao')
        
        context['active_tab'] = self.request.GET.get('tab', 'ops_cliente')
        context['filter_form'] = OpFilterForm(self.request.GET or None)
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        op_ids = request.POST.getlist('op_selecionada')
        if not op_ids:
            messages.warning(request, "Nenhuma Ordem de Produção foi selecionada.")
            return redirect('producao:lancamento-painel-selecao')

        primeira_op = get_object_or_404(OrdemProducao, pk=op_ids[0])
        agrupamento_existente = primeira_op.agrupamentos.first()

        if agrupamento_existente:
            if agrupamento_existente.lancamentos.exists():
                agrupamento = agrupamento_existente
                agrupamento.ordens_producao.add(*op_ids)
                messages.info(request, f"OPs adicionadas ao Agrupamento em andamento {agrupamento.id}.")
            else:
                agrupamento = agrupamento_existente
                agrupamento.ordens_producao.set(op_ids)
                messages.info(request, f"Agrupamento {agrupamento.id} atualizado com a nova seleção de OPs.")
        else:
            agrupamento = AgrupamentoLancamento.objects.create()
            agrupamento.ordens_producao.set(op_ids)
            messages.success(request, f"Novo Agrupamento {agrupamento.id} criado. Inicie o primeiro lançamento.")

        return redirect('producao:lancamento-apontamento-agrupado', agrupamento_pk=agrupamento.pk)

class ListaOpsAguardandoCorteView(ListView):
    """
    Lista OPs e Solicitações Kanban que estão no status 'Aguardando Corte',
    organizadas em abas com filtros para OPs de cliente.
    """
    model = OrdemProducao
    template_name = 'producao/lista_ops_aguardando_corte.html'
    context_object_name = 'ordens_producao'
    paginate_by = 30

    def get_queryset(self):
        # A query base filtra apenas OPs de CLIENTE aguardando corte
        queryset = OrdemProducao.objects.filter(
            status=OrdemProducaoStatus.AGUARDANDO_CORTE,
            is_kanban=False
        ).annotate(
            quantidade_grosas_produzida_agg=Coalesce(
                Sum('contribuicoes_op__quantidade_grosas_produzida'),
                decimal.Decimal('0.0'),
                output_field=DecimalField()
            )
        ).prefetch_related('demandas__pedido__cliente').distinct().order_by('data_qmc', 'sequencia_pcp')

        # Aplica os filtros do formulário
        form = OpFilterForm(self.request.GET)
        if form.is_valid():
            numero_op = form.cleaned_data.get('numero_op')
            if numero_op:
                queryset = queryset.filter(numero_op__icontains=numero_op)
            tamanho = form.cleaned_data.get('tamanho')
            if tamanho:
                queryset = queryset.filter(tamanho__icontains=tamanho)
            material = form.cleaned_data.get('material')
            if material:
                queryset = queryset.filter(material__icontains=material)
            numero_pedido = form.cleaned_data.get('numero_pedido')
            if numero_pedido:
                queryset = queryset.filter(demandas__pedido__numero_pedido__icontains=numero_pedido)
            cliente = form.cleaned_data.get('cliente')
            if cliente:
                queryset = queryset.filter(demandas__pedido__cliente__nome__icontains=cliente)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Define a aba ativa e busca os dados para a aba de Kanban
        active_tab = self.request.GET.get('tab', 'ops_cliente')
        context['active_tab'] = active_tab
        
        context['solicitacoes_kanban'] = SolicitacaoReposicaoKanban.objects.filter(
            status=SolicitacaoReposicaoKanban.Status.AGUARDANDO_CORTE
        ).select_related('item_estoque').order_by('data_solicitacao')

        context['setor_nome'] = 'Fila de OPs - Aguardando Corte'
        context['filter_form'] = OpFilterForm(self.request.GET or None)
        
        # Prepara os dados de display para as OPs de cliente
        for op in context['ordens_producao']:
            clientes = {d.pedido.cliente.nome for d in op.demandas.all() if d.pedido and d.pedido.cliente}
            op.clientes_display = ', '.join(sorted(list(clientes))) or "-"
            
            pedidos = {d.pedido.numero_pedido for d in op.demandas.all() if d.pedido}
            op.pedidos_display = ', '.join(sorted(list(pedidos))) or "-"
            
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        Processa o envio do formulário para marcar OPs ou Solicitações Kanban
        como cortadas e as envia para o próximo setor (Controle de Pastilha).
        """
        op_ids = request.POST.getlist('op_selecionada')
        kanban_ids = request.POST.getlist('kanban_selecionado')
        
        ops_atualizadas_count = 0
        kanbans_atualizados_count = 0

        # Processa as Ordens de Produção de cliente selecionadas
        if op_ids:
            ops_para_atualizar = OrdemProducao.objects.filter(
                pk__in=op_ids,
                status=OrdemProducaoStatus.AGUARDANDO_CORTE
            )
            ops_atualizadas_count = ops_para_atualizar.update(status=OrdemProducaoStatus.AGUARDANDO_PASTILHA)
            
            if ops_atualizadas_count > 0:
                messages.success(request, f"{ops_atualizadas_count} OP(s) de cliente enviada(s) para o Controle de Pastilha.")

        # Processa as Solicitações de Reposição Kanban selecionadas
        if kanban_ids:
            kanbans_para_atualizar = SolicitacaoReposicaoKanban.objects.filter(
                pk__in=kanban_ids,
                status=SolicitacaoReposicaoKanban.Status.AGUARDANDO_CORTE
            )
            kanbans_atualizados_count = kanbans_para_atualizar.update(status=SolicitacaoReposicaoKanban.Status.AGUARDANDO_PASTILHA)
            
            if kanbans_atualizados_count > 0:
                messages.success(request, f"{kanbans_atualizados_count} solicitação(ões) Kanban enviada(s) para o Controle de Pastilha.")

        # Exibe uma mensagem de aviso se nenhuma ação foi executada
        if not ops_atualizadas_count and not kanbans_atualizados_count:
            messages.warning(request, "Nenhum item foi selecionado ou os itens já foram processados.")
            
        return redirect('producao:lista_ops_aguardando_corte')

def op_finalizar_quimica(request, op_pk):
    if request.method == 'POST':
        op = get_object_or_404(OrdemProducao, pk=op_pk)
        op.status = OrdemProducaoStatus.AGUARDANDO_PASTILHA
        op.save()
        messages.success(request, f"OP {op.numero_op} enviada com sucesso para o Controle de Pastilha.")
    return redirect('producao:lista_ops_aguardando_corte')

class ApontamentoLancamentoAgrupadoView(View):
    """
    Controla a tela de apontamento para um AgrupamentoLancamento,
    com um fluxo de Início e Fim para cada lançamento em abas.
    """
    template_name = 'producao/apontamento_quimica_lancamento_agrupado.html'

    def get(self, request, *args, **kwargs):
        """ Prepara e renderiza a página de apontamento com os forms necessários. """
        context = self._get_common_context(request, **kwargs)
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """ Processa as ações de Iniciar, Salvar, Finalizar ou Cancelar um lançamento. """
        agrupamento = get_object_or_404(AgrupamentoLancamento, pk=kwargs.get('agrupamento_pk'))
        
        action = next((key for key in request.POST if key.startswith('action_')), None)

        if action == 'action_iniciar':
            return self._handle_iniciar_lancamento(request, agrupamento)
        
        if not action:
            messages.error(request, "Ação inválida ou não reconhecida.")
            return redirect('producao:lancamento-apontamento-agrupado', agrupamento_pk=agrupamento.pk)

        try:
            lancamento_id = action.split('_')[-1]
        except (IndexError, ValueError):
            messages.error(request, "ID de lançamento inválido na ação.")
            return redirect('producao:lancamento-apontamento-agrupado', agrupamento_pk=agrupamento.pk)

        if action.startswith('action_finalizar_'):
            return self._handle_salvar_ou_finalizar(request, agrupamento, lancamento_id, finalizar=True)
        
        if action.startswith('action_salvar_'):
            return self._handle_salvar_ou_finalizar(request, agrupamento, lancamento_id, finalizar=False)

        if action.startswith('action_cancelar_'):
            return self._handle_cancelar_lancamento(request, agrupamento, lancamento_id)

        messages.error(request, "Ação desconhecida.")
        return redirect('producao:lancamento-apontamento-agrupado', agrupamento_pk=agrupamento.pk)

    def _get_common_context(self, request, **kwargs):
        """ Monta o dicionário de contexto, separando lançamentos em andamento e finalizados. """
        agrupamento_pk = kwargs.get('agrupamento_pk')
        agrupamento = get_object_or_404(
            AgrupamentoLancamento.objects.prefetch_related(
                'ordens_producao__reprogramacoes__motivo', 
                'ordens_producao__contribuicoes_op', 
                'lancamentos__paradas__motivo',
                'lancamentos__contribuicoes_op__ordem_producao',
                'lancamentos__operador', 'lancamentos__maquina'
            ), pk=agrupamento_pk
        )
        
        ordens_do_agrupamento = list(agrupamento.ordens_producao.all())
        
        total_grosas_programado = decimal.Decimal('0.0')
        for op in ordens_do_agrupamento:
            total_grosas_programado += op.quantidade_total_alvo_com_retrabalho
            op.info_retrabalho = op.get_info_retrabalho()

        total_grosas_produzido_geral = ContribuicaoOP.objects.filter(
            ordem_producao__in=ordens_do_agrupamento
        ).aggregate(total=Coalesce(Sum('quantidade_grosas_produzida'), decimal.Decimal(0)))['total']
        
        saldo_restante = total_grosas_programado - total_grosas_produzido_geral

        lancamentos_em_andamento = agrupamento.lancamentos.filter(data_hora_fim__isnull=True).order_by('data_hora_inicio')
        forms_em_andamento = []
        for lancamento in lancamentos_em_andamento:
            forms_em_andamento.append({
                'lancamento': lancamento,
                'form_fim': ApontamentoCilindroFimForm(prefix=f'fim_{lancamento.id}', instance=lancamento, ordens_producao=ordens_do_agrupamento),
                'formset_paradas': ParadaCilindroFormSet(prefix=f'paradas_{lancamento.id}', queryset=ParadaLancamentoAgrupado.objects.filter(lancamento=lancamento))
            })

        return {
            'agrupamento': agrupamento,
            'ordens_do_agrupamento': ordens_do_agrupamento,
            'total_grosas_programado': total_grosas_programado,
            'total_grosas_produzido': total_grosas_produzido_geral,
            'saldo_restante': saldo_restante,
            'forms_em_andamento': forms_em_andamento,
            'form_inicio': ApontamentoCilindroInicioForm(prefix='inicio'),
            'lancamentos_anteriores': agrupamento.lancamentos.filter(data_hora_fim__isnull=False).order_by('-data_hora_fim'),
            'active_tab': request.GET.get('tab'),
        }

    def _handle_iniciar_lancamento(self, request, agrupamento):
        """ Valida o form de início e cria um novo lançamento em andamento. """
        form_inicio = ApontamentoCilindroInicioForm(request.POST, prefix='inicio')
        if form_inicio.is_valid():
            maquina = form_inicio.cleaned_data['maquina']
            if LancamentoCilindro.objects.filter(agrupamento=agrupamento, maquina=maquina, data_hora_fim__isnull=True).exists():
                messages.error(request, f"Já existe um apontamento em andamento para a máquina {maquina.nome_maq_erp} neste agrupamento.")
                return redirect('producao:lancamento-apontamento-agrupado', agrupamento_pk=agrupamento.pk)

            lancamento = form_inicio.save(commit=False)
            lancamento.agrupamento = agrupamento
            lancamento.data_hora_inicio = timezone.now()
            lancamento.quantidade_placas_total = 0
            lancamento.quantidade_grosas_total = 0
            lancamento.save()
            messages.success(request, f"Lançamento para a máquina {lancamento.maquina.nome_maq_erp} iniciado.")
            
            redirect_url = reverse('producao:lancamento-apontamento-agrupado', kwargs={'agrupamento_pk': agrupamento.pk})
            return redirect(f'{redirect_url}?tab=lanc-{lancamento.pk}')
        else:
            messages.error(request, f"Erro ao iniciar lançamento: {form_inicio.errors.as_text()}")
            return redirect('producao:lancamento-apontamento-agrupado', agrupamento_pk=agrupamento.pk)

    def _handle_salvar_ou_finalizar(self, request, agrupamento, lancamento_id, finalizar=False):
        """ Salva os dados de um lançamento em andamento e, opcionalmente, o finaliza. """
        lancamento = get_object_or_404(LancamentoCilindro, pk=lancamento_id, agrupamento=agrupamento)
        ordens_do_agrupamento = list(agrupamento.ordens_producao.all())

        form_fim = ApontamentoCilindroFimForm(request.POST, prefix=f'fim_{lancamento.id}', instance=lancamento, ordens_producao=ordens_do_agrupamento)
        formset_paradas = ParadaCilindroFormSet(request.POST, prefix=f'paradas_{lancamento.id}', queryset=ParadaLancamentoAgrupado.objects.filter(lancamento=lancamento))

        if form_fim.is_valid() and formset_paradas.is_valid():
            lancamento_salvo = form_fim.save()
            
            total_placas_lancamento = decimal.Decimal('0.0')
            lancamento_salvo.contribuicoes_op.all().delete() 
            for op in ordens_do_agrupamento:
                field_name = f'placas_op_{op.pk}'
                qtd_placas = form_fim.cleaned_data.get(field_name, decimal.Decimal('0.0')) or decimal.Decimal('0.0')
                if qtd_placas > 0:
                    ContribuicaoOP.objects.create(
                        lancamento=lancamento_salvo,
                        ordem_producao=op,
                        quantidade_placas_contribuida=qtd_placas
                    )
                    total_placas_lancamento += qtd_placas
            
            lancamento_salvo.quantidade_placas_total = total_placas_lancamento
            lancamento_salvo.save(update_fields=['quantidade_placas_total'])
            lancamento_salvo.atualizar_total_grosas()

            paradas = formset_paradas.save(commit=False)
            for parada in paradas:
                parada.lancamento = lancamento_salvo
                parada.save()
            formset_paradas.save_m2m()
            for parada_deletada in formset_paradas.deleted_objects:
                parada_deletada.delete()

            if finalizar:
                lancamento_salvo.data_hora_fim = timezone.now()
                lancamento_salvo.save(update_fields=['data_hora_fim'])
                messages.success(request, f'Lançamento #{lancamento.id} finalizado com sucesso.')

                # --- LÓGICA DE FINALIZAÇÃO DO GRUPO (CORRIGIDA) ---
                # 1. Recalcula o total produzido COM OS DADOS ATUALIZADOS
                total_grosas_produzido_final = ContribuicaoOP.objects.filter(
                    ordem_producao__in=ordens_do_agrupamento
                ).aggregate(total=Coalesce(Sum('quantidade_grosas_produzida'), decimal.Decimal(0)))['total']

                # 2. Recalcula o total programado (usando a propriedade do modelo para garantir consistência)
                total_grosas_programado_final = sum(op.quantidade_total_alvo_com_retrabalho for op in ordens_do_agrupamento)

                # 3. Verifica se a meta foi atingida
                if total_grosas_produzido_final >= total_grosas_programado_final:
                    ops_atualizadas = agrupamento.ordens_producao.update(status=OrdemProducaoStatus.AGUARDANDO_CORTE)
                    if ops_atualizadas > 0:
                        messages.info(request, f"{ops_atualizadas} OP(s) do agrupamento atingiram a meta e foram enviadas para 'Aguardando Corte'.")
                    # Redireciona para o painel principal, pois o trabalho neste agrupamento terminou.
                    return redirect('producao:lancamento-painel-selecao')
            else:
                messages.success(request, f'Dados do lançamento #{lancamento.id} salvos com sucesso.')
        else:
            formset_errors = str(formset_paradas.errors) if formset_paradas.errors else ""
            messages.error(request, f"Erro ao salvar dados. Verifique os campos. Erros: {form_fim.errors.as_text()} {formset_errors}")

        # Redireciona de volta para a mesma página, mantendo o usuário no contexto do apontamento.
        redirect_url = reverse('producao:lancamento-apontamento-agrupado', kwargs={'agrupamento_pk': agrupamento.pk})
        tab_param = 'lanc-new' if finalizar else f'lanc-{lancamento_id}'
        return redirect(f'{redirect_url}?tab={tab_param}')

    def _handle_cancelar_lancamento(self, request, agrupamento, lancamento_id):
        """ Exclui um lançamento que foi iniciado por engano. """
        lancamento = get_object_or_404(LancamentoCilindro, pk=lancamento_id, agrupamento=agrupamento)
        if lancamento.data_hora_fim is not None:
            messages.error(request, "Não é possível cancelar um lançamento que já foi finalizado.")
        else:
            nome_maquina = lancamento.maquina.nome_maq_erp
            lancamento.delete()
            messages.warning(request, f'O lançamento em andamento para a máquina {nome_maquina} foi cancelado.')
        
        redirect_url = reverse('producao:lancamento-apontamento-agrupado', kwargs={'agrupamento_pk': agrupamento.pk})
        return redirect(f'{redirect_url}?tab=lanc-new')
    
# --- NOVA VIEW ---
class FinalizarOPQuimicaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        op_pk = kwargs.get('op_pk')
        op = get_object_or_404(OrdemProducao, pk=op_pk)

        try:          
            op.status = OrdemProducaoStatus.AGUARDANDO_PASTILHA
            op.save(update_fields=['status'])
            
            messages.success(request, f"A OP {op.numero_op} foi finalizada na Química e enviada para o Controle de Pastilha.")
        
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao finalizar a OP {op.numero_op}: {e}")

        return redirect('producao:lancamento-painel-selecao')
    
#Reprogramação
class CriarRetrabalhoPastilhaView(LoginRequiredMixin, View):
    """
    Processa a criação de um registro de reprogramação (retrabalho)
    a partir do setor de Pastilha, enviando a OP de volta para a Química.
    """
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        op_pk = kwargs.get('op_pk')
        op = get_object_or_404(OrdemProducao, pk=op_pk)
        
        form = ReprogramacaoForm(request.POST, ordem_producao=op)

        if form.is_valid():
            reprogramacao = form.save(commit=False)
            reprogramacao.ordem_producao = op
            
            setor_pastilha = get_object_or_404(SetorModel, nome='Controle de Pastilha')
            reprogramacao.setor_origem = setor_pastilha
            
            try:
                operador_logado = Operador.objects.get(nome__iexact=request.user.username)
                reprogramacao.responsavel = operador_logado
            except Operador.DoesNotExist:
                messages.error(request, f"Não foi possível criar o retrabalho: Nenhum operador encontrado com o nome '{request.user.username}'.")
                return redirect('producao:apontamento_pastilha', op_id=op.pk)

            reprogramacao.save()

            peso_10_botoes = form.cleaned_data.get('peso_10_botoes')
            if not op.peso_bruto_grosa and peso_10_botoes:
                op.peso_bruto_grosa = (peso_10_botoes / 10) * 144
                messages.info(request, f"Peso da grôsa ({op.peso_bruto_grosa:.2f}g) definido para a OP {op.numero_op}.")

            # --- CORREÇÃO PRINCIPAL: A OP não tem mais sua quantidade total alterada ---
            # A quantidade do retrabalho fica registrada apenas no modelo ReprogramacaoOP.
            op.status = OrdemProducaoStatus.PENDENTE
            op.save()
            
            messages.success(request, f"Retrabalho para a OP {op.numero_op} solicitado com sucesso. A OP retornou para a Química.")
            return redirect('producao:lista_ops_pastilha')
        
        else:
            erros = '. '.join([f'{k}: {v[0]}' for k, v in form.errors.items()])
            messages.error(request, f"Não foi possível criar o retrabalho. Erros: {erros}")
            return redirect('producao:apontamento_pastilha', op_id=op.pk)


class ApontamentoTornoLaserKanbanView(ProducaoTornosRequiredMixin, View):
    """
    View unificada para o apontamento de produção nos setores de Torno, Laser e Kanban.
    Refatorada para usar os novos modelos de Cliente.
    """
    template_name = 'producao/apontamento_torno_laser_kanban.html'

    def get(self, request, *args, **kwargs):
        # Otimiza a busca da OP, já carregando os dados do cliente
        op = get_object_or_404(
            OrdemProducao.objects.prefetch_related('demandas__pedido__cliente'), 
            pk=kwargs['op_id']
        )
        setor_url = self.kwargs['setor']
        setor_enum = getattr(Setor, setor_url.upper())

        apontamentos_em_andamento = ControleProducaoTornoLaser.objects.filter(
            ordem_producao=op,
            data_hora_fim__isnull=True
        ).order_by('data_hora_inicio')

        forms_em_andamento = []
        for apontamento in apontamentos_em_andamento:
            forms_em_andamento.append({
                'apontamento': apontamento,
                'form_fim': ApontamentoFimForm(prefix=f'fim_{apontamento.id}', instance=apontamento, ordem_producao=op),
                'formset_paradas': ParadaProducaoFormSet(prefix=f'paradas_{apontamento.id}', queryset=Parada.objects.filter(apontamento_producao=apontamento))
            })

        context = self._get_common_context(request, op, setor_url)
        context['forms_em_andamento'] = forms_em_andamento
        context['form_inicio'] = ApontamentoInicioForm(prefix='inicio', setor=setor_enum)
        
        return render(request, self.template_name, context)

    def _get_common_context(self, request, op, setor_url):
        """
        Prepara o contexto comum para a view, agora incluindo dados formatados
        de cliente, pedidos e observações.
        """
        self.request = request
        saldo_disponivel_kg = decimal.Decimal('0.0')
        
        if setor_url == 'kanban':
            try:
                item_estoque = ItemEstoqueKanban.objects.select_related('estoque').get(
                    material=op.material, cor=op.cor, tamanho=op.tamanho
                )
                if hasattr(item_estoque, 'estoque') and item_estoque.estoque:
                    saldo_disponivel_kg = item_estoque.estoque.saldo_peso_kg
            except ItemEstoqueKanban.DoesNotExist:
                pass
        else:
            try:
                setor_obj = SetorModel.objects.get(nome__iexact=setor_url)
                saldo_setor = SaldoOPSetor.objects.filter(ordem_producao=op, setor=setor_obj).first()
                if saldo_setor:
                    saldo_disponivel_kg = saldo_setor.saldo_peso
            except SetorModel.DoesNotExist:
                pass
        
        # --- LÓGICA DE PREPARAÇÃO DE DADOS ADICIONADA ---
        # Prepara a string de clientes e pedidos
        clientes = {d.pedido.cliente.nome for d in op.demandas.all() if d.pedido and d.pedido.cliente}
        pedidos = {d.pedido.numero_pedido for d in op.demandas.all() if d.pedido}
        
        # Coleta observações únicas
        observacoes_pedidos = {d.pedido.observacao_detalhada for d in op.demandas.all() if d.pedido and d.pedido.observacao_detalhada}
        observacoes_itens = {d.observacao_item_pedido for d in op.demandas.all() if d.observacao_item_pedido}

        return { 
            'ordem_producao': op, 
            'setor_nome': f"Apontamento - {setor_url.title()}", 
            'setor_url': setor_url,
            'saldo_disponivel_kg': saldo_disponivel_kg,
            # Novas variáveis de contexto para o template
            'clientes_display': ', '.join(sorted(list(clientes))) or "-",
            'pedidos_display': ', '.join(sorted(list(pedidos))) or "-",
            'observacoes_pedidos_unicas': list(observacoes_pedidos),
            'observacoes_item_pedido': list(observacoes_itens),
        }

    # --- NENHUMA ALTERAÇÃO NECESSÁRIA NOS MÉTODOS DE POST ---
    # A lógica de apontamento (criar, salvar, finalizar) não depende dos campos de cliente/pedido.
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.request = request
        op = get_object_or_404(OrdemProducao, pk=kwargs['op_id'])
        setor_url = self.kwargs['setor']
        
        action = next((key for key in request.POST if key.startswith('action_')), None)

        if action == 'action_iniciar':
            return self._handle_iniciar_apontamento(request, op, setor_url)
        
        try:
            apontamento_id = int(action.split('_')[-1])
        except (ValueError, IndexError, TypeError):
            messages.error(request, "Ação inválida ou ID de apontamento não encontrado.")
            return redirect('producao:apontamento_torno_laser_kanban', setor=setor_url, op_id=op.id)

        if action.startswith('action_finalizar_'):
            return self._handle_salvar_ou_finalizar(request, op, setor_url, apontamento_id, finalizar=True)
        
        if action.startswith('action_salvar_'):
            return self._handle_salvar_ou_finalizar(request, op, setor_url, apontamento_id, finalizar=False)

        if action.startswith('action_cancelar_'):
            return self._handle_cancelar_apontamento(request, op, setor_url, apontamento_id)

        messages.error(request, "Ação desconhecida.")
        return redirect('producao:apontamento_torno_laser_kanban', setor=setor_url, op_id=op.id)

    def _handle_iniciar_apontamento(self, request, op, setor_url):
        setor_enum = getattr(Setor, setor_url.upper())
        form_inicio = ApontamentoInicioForm(request.POST, prefix='inicio', setor=setor_enum)
        if form_inicio.is_valid():
            apontamento = form_inicio.save(commit=False)
            apontamento.ordem_producao = op
            apontamento.data_hora_inicio = timezone.now()
            apontamento.save()
            messages.success(request, f"Novo apontamento para a OP {op.numero_op} iniciado com sucesso.")
        else:
            messages.error(request, f"Erro ao iniciar novo apontamento: {form_inicio.errors.as_text()}")
        return redirect('producao:apontamento_torno_laser_kanban', setor=setor_url, op_id=op.id)

    def _handle_salvar_ou_finalizar(self, request, op, setor_url, apontamento_id, finalizar=False):
        apontamento = get_object_or_404(ControleProducaoTornoLaser, pk=apontamento_id, ordem_producao=op)
        
        form_fim = ApontamentoFimForm(request.POST, prefix=f'fim_{apontamento.id}', instance=apontamento, ordem_producao=op)
        formset_paradas = ParadaProducaoFormSet(request.POST, prefix=f'paradas_{apontamento.id}', queryset=Parada.objects.filter(apontamento_producao=apontamento))

        if not (form_fim.is_valid() and formset_paradas.is_valid()):
            return self._render_page_with_errors(request, op, setor_url, apontamento_id, form_fim, formset_paradas)

        apontamento_salvo = self._salvar_dados_apontamento(form_fim, op, finalizar)
        self._salvar_paradas(formset_paradas, apontamento_salvo)

        peso_produzido = form_fim.cleaned_data.get('producao_peso')
        if peso_produzido and peso_produzido > 0:
            self._consumir_saldo_producao(op, setor_url, peso_produzido, apontamento_salvo)

        if finalizar:
            self._processar_transferencia(form_fim, op, setor_url, apontamento_salvo)
            op_foi_finalizada = self._verificar_e_finalizar_op(op)
            
            if op_foi_finalizada and setor_url != 'kanban':
                setor_origem_obj = get_object_or_404(SetorModel, nome__iexact=setor_url)
                saldo_op_a_zerar = SaldoOPSetor.objects.filter(ordem_producao=op, setor=setor_origem_obj).first()
                if saldo_op_a_zerar and saldo_op_a_zerar.saldo_peso > 0:
                    peso_residual = saldo_op_a_zerar.saldo_peso
                    saldo_op_a_zerar.saldo_peso = 0
                    saldo_op_a_zerar.save()
                    messages.info(request, f"Saldo residual de {peso_residual:.4f} Kg no setor {setor_origem_obj.nome} foi zerado pois a meta de produção foi atingida.")

            redirect_url_name = 'producao:lista_ops_kanban' if setor_url == 'kanban' else 'producao:lista_ops_torno_laser'
            redirect_kwargs = {'setor': setor_url} if setor_url != 'kanban' else {}

            if op_foi_finalizada:
                messages.success(request, f'OP {op.numero_op} finalizada!')
                return redirect(redirect_url_name, **redirect_kwargs)
            
            messages.success(request, f'Apontamento finalizado. OP continua em produção.')
        else:
            messages.success(request, f'Dados do apontamento salvos com sucesso.')

        return redirect('producao:apontamento_torno_laser_kanban', setor=setor_url, op_id=op.id)

    def _handle_cancelar_apontamento(self, request, op, setor_url, apontamento_id):
        apontamento = get_object_or_404(ControleProducaoTornoLaser, pk=apontamento_id, ordem_producao=op)
        apontamento.delete()
        messages.warning(request, f'O apontamento na máquina {apontamento.maquina.nome_maq_erp} foi cancelado.')
        return redirect('producao:apontamento_torno_laser_kanban', setor=setor_url, op_id=op.id)

    def _consumir_saldo_producao(self, op, setor_url, peso_consumido_kg, apontamento):
        if setor_url == 'kanban':
            try:
                item_estoque = ItemEstoqueKanban.objects.get(material=op.material, cor=op.cor, tamanho=op.tamanho)
                estoque, _ = EstoqueKanban.objects.get_or_create(item_estoque=item_estoque)
                
                grosas_produzidas = apontamento.producao_grosas or decimal.Decimal('0.0')
                peso_bruto_a_debitar_kg = decimal.Decimal('0.0')

                if grosas_produzidas > 0 and item_estoque.peso_bruto_grosa_medio and item_estoque.peso_bruto_grosa_medio > 0:
                    peso_bruto_grosa_kg = item_estoque.peso_bruto_grosa_medio / 1000
                    peso_bruto_a_debitar_kg = grosas_produzidas * peso_bruto_grosa_kg
                else:
                    peso_bruto_a_debitar_kg = peso_consumido_kg
                    #logger.warning(f"AVISO: Não foi possível calcular o consumo de peso bruto para o item {item_estoque}. Usando o peso do produto acabado ({peso_consumido_kg} Kg) como fallback.")

                estoque.saldo_peso_kg = F('saldo_peso_kg') - peso_bruto_a_debitar_kg
                estoque.save()
                
                estoque.refresh_from_db()
                
                if item_estoque.peso_bruto_grosa_medio and item_estoque.peso_bruto_grosa_medio > 0:
                    peso_bruto_grosa_kg = item_estoque.peso_bruto_grosa_medio / 1000
                    novo_saldo_grosas = estoque.saldo_peso_kg / peso_bruto_grosa_kg
                    estoque.saldo_grosas_aproximado = novo_saldo_grosas
                else:
                    estoque.saldo_grosas_aproximado = 0
                
                estoque.save()

                MovimentoEstoqueKanban.objects.create(
                    item_estoque=item_estoque,
                    tipo_movimento=MovimentoEstoqueKanban.Tipo.SAIDA_CONSUMO,
                    peso_movimentado_kg=peso_bruto_a_debitar_kg,
                    grosas_movimentadas=grosas_produzidas,
                    peso_bruto_grosa_no_momento=op.peso_liquido_grosa,
                    responsavel=apontamento.responsavel,
                    ordem_producao_consumo=op
                )
                messages.info(self.request, f"{peso_bruto_a_debitar_kg:.4f} Kg de matéria-prima (bruto) foram consumidos do estoque Kanban.")

            except ItemEstoqueKanban.DoesNotExist:
                messages.error(self.request, "Erro: Não foi possível encontrar o item no estoque Kanban para dar baixa.")
        else:
            pass

    def _salvar_dados_apontamento(self, form, op, finalizar):
        peso_10_botoes = form.cleaned_data.get('peso_10_botoes')
        if peso_10_botoes is not None and peso_10_botoes > 0:
            op.peso_liquido_grosa = (peso_10_botoes / 10) * 144
            op.save(update_fields=['peso_liquido_grosa'])
            op.refresh_from_db()

        apontamento = form.save(commit=False)
        
        producao_peso_kg = form.cleaned_data.get('producao_peso')
        if producao_peso_kg and op.peso_liquido_grosa and op.peso_liquido_grosa > 0:
            peso_liquido_grosa_kg = op.peso_liquido_grosa / 1000
            apontamento.producao_grosas = producao_peso_kg / peso_liquido_grosa_kg
        else:
            apontamento.producao_grosas = 0
        
        if finalizar:
            apontamento.data_hora_fim = timezone.now()
        
        apontamento.save()
        form.save_m2m()
        return apontamento

    def _salvar_paradas(self, formset, apontamento):
        paradas = formset.save(commit=False)
        for parada in paradas:
            parada.apontamento_producao = apontamento
            parada.save()
        for parada_deletada in formset.deleted_objects:
            parada_deletada.delete()

    def _processar_transferencia(self, form, op, setor_url, apontamento):
        peso_a_transferir = form.cleaned_data.get('peso_a_transferir')
        setor_destino_obj = form.cleaned_data.get('proximo_setor')

        if not (peso_a_transferir and peso_a_transferir > 0 and setor_destino_obj):
            return

        setor_origem_obj = get_object_or_404(SetorModel, nome__iexact=setor_url)

        TransferenciaEntreSetores.objects.create(
            ordem_producao=op,
            setor_origem=setor_origem_obj,
            setor_destino=setor_destino_obj,
            peso_transferido=peso_a_transferir,
            responsavel=apontamento.responsavel
        )

        saldo_destino, _ = SaldoOPSetor.objects.get_or_create(ordem_producao=op, setor=setor_destino_obj)
        saldo_destino.saldo_peso = F('saldo_peso') + peso_a_transferir
        saldo_destino.save()

        if setor_url != 'kanban':
            saldo_origem, _ = SaldoOPSetor.objects.get_or_create(ordem_producao=op, setor=setor_origem_obj)
            saldo_origem.saldo_peso = F('saldo_peso') - peso_a_transferir
            saldo_origem.save()

        messages.info(self.request, f"Saldo de {peso_a_transferir:.4f} Kg da OP {op.numero_op} transferido para {setor_destino_obj.nome}.")

    def _verificar_e_finalizar_op(self, op):
        total_produzido_grosas = ControleProducaoTornoLaser.objects.filter(
            ordem_producao=op
        ).aggregate(
            total=Sum('producao_grosas')
        )['total'] or decimal.Decimal('0.0')

        quantidade_alvo_final = op.quantidade_total_alvo_com_retrabalho

        if total_produzido_grosas >= quantidade_alvo_final:
            op.status = OrdemProducaoStatus.FINALIZADO
            op.save(update_fields=['status'])
            return True
            
        return False

    def _render_page_with_errors(self, request, op, setor_url, apontamento_id, form_fim, formset_paradas):
        messages.error(request, f"Erro ao salvar dados. Verifique os campos abaixo.")
        
        context = self._get_common_context(request, op, setor_url)
        
        apontamentos_em_andamento = ControleProducaoTornoLaser.objects.filter(
            ordem_producao=op, data_hora_fim__isnull=True
        ).order_by('data_hora_inicio')
        
        forms_em_andamento = []
        for ap in apontamentos_em_andamento:
            if ap.id == int(apontamento_id):
                forms_em_andamento.append({'apontamento': ap, 'form_fim': form_fim, 'formset_paradas': formset_paradas})
            else:
                forms_em_andamento.append({
                    'apontamento': ap,
                    'form_fim': ApontamentoFimForm(prefix=f'fim_{ap.id}', instance=ap, ordem_producao=op),
                    'formset_paradas': ParadaProducaoFormSet(prefix=f'paradas_{ap.id}', queryset=Parada.objects.filter(apontamento_producao=ap))
                })
        
        context['forms_em_andamento'] = forms_em_andamento
        setor_enum = getattr(Setor, setor_url.upper())
        context['form_inicio'] = ApontamentoInicioForm(prefix='inicio', setor=setor_enum)
        return render(request, self.template_name, context)


    
class SolicitarQuimicaKanbanView(LoginRequiredMixin, View):
    """
    Processa a criação de uma solicitação de matéria-prima para a Química
    a partir de uma OP Kanban.
    """
    def post(self, request, *args, **kwargs):
        op_pk = kwargs.get('op_pk')
        op = get_object_or_404(OrdemProducao, pk=op_pk, is_kanban=True)
        form = SolicitacaoQuimicaKanbanForm(request.POST)

        if form.is_valid():
            # Verifica se já existe uma solicitação pendente para evitar duplicidade
            if SolicitacaoQuimicaKanban.objects.filter(ordem_producao=op, status='PENDENTE').exists():
                messages.warning(request, f"A OP {op.numero_op} já possui uma solicitação pendente para a Química.")
            else:
                solicitacao = form.save(commit=False)
                solicitacao.ordem_producao = op
                solicitacao.solicitado_por = request.user
                solicitacao.save()
                messages.success(request, f"Solicitação de {solicitacao.quantidade_solicitada} GRS para a OP {op.numero_op} enviada à Química.")
        else:
            messages.error(request, "Erro ao criar solicitação. Verifique a quantidade informada.")
        
        return redirect('producao:lista_ops_torno_laser_kanban', setor='kanban')

class AtenderDemandaKanbanView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        solicitacao_pk = kwargs.get('solicitacao_pk')
        solicitacao = get_object_or_404(SolicitacaoQuimicaKanban, pk=solicitacao_pk, status='PENDENTE')
        op = solicitacao.ordem_producao

        try:
            solicitacao.status = 'ATENDIDA'
            solicitacao.data_atendimento = timezone.now()
            solicitacao.save()

            # CORREÇÃO: Remove a mudança de 'setor_atual'. O status EM_PRODUCAO
            # já indica que a OP está ativa no seu respectivo setor (Kanban).
            # A solicitação atendida gera uma tarefa para a Química, mas não move a OP Kanban.
            op.status = OrdemProducaoStatus.EM_PRODUCAO
            op.save(update_fields=['status'])
            
            messages.success(request, f"A solicitação da OP Kanban {op.numero_op} foi atendida e enviada para produção na Química.")
        
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao processar a demanda da OP {op.numero_op}: {e}")

        return redirect('producao:painel_quimica')


class ReceitaOPView(LoginRequiredMixin, DetailView):
    """
    Exibe a receita calculada para uma única Ordem de Produção.
    Calcula a receita para a quantidade total, para uma demanda Kanban específica,
    ou para uma quantidade parcial de retrabalho.
    """
    model = OrdemProducao
    template_name = 'producao/receita_op.html'
    context_object_name = 'ordem_producao'
    pk_url_kwarg = 'op_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        op = self.get_object()
        
        quantidade_alvo_grosas = None
        solicitacao = None
        context['is_retrabalho'] = False

        # 1. Verifica se é um cálculo para um retrabalho específico
        reprogramacao_pk = self.request.GET.get('reprogramacao_pk')
        if reprogramacao_pk:
            repro = get_object_or_404(ReprogramacaoOP, pk=reprogramacao_pk, ordem_producao=op)
            context['is_retrabalho'] = True
            context['motivo_retrabalho'] = repro.motivo.descricao
            
            if repro.peso_reprogramado and op.peso_bruto_grosa and op.peso_bruto_grosa > 0:
                peso_bruto_grosa_kg = op.peso_bruto_grosa / 1000
                quantidade_alvo_grosas = repro.peso_reprogramado / peso_bruto_grosa_kg
                context['quantidade_alvo_grosas'] = quantidade_alvo_grosas

                # --- LÓGICA PARA CALCULAR DADOS PARCIAIS DO RETRABALHO ---
                if op.rendimento and op.rendimento > 0:
                    placas_reprogramadas = quantidade_alvo_grosas / op.rendimento
                    
                    if op.peso_placa and op.peso_placa > 0:
                        context['retrabalho_peso_bruto'] = placas_reprogramadas * op.peso_placa

                    fracao_placa, _ = math.modf(placas_reprogramadas)
                    if fracao_placa > 0:
                        TAMANHO_PLACA_CM = decimal.Decimal('57.0')
                        cm_borracha = decimal.Decimal(fracao_placa) * TAMANHO_PLACA_CM
                        context['retrabalho_borracha_cm'] = int(cm_borracha.to_integral_value(rounding=decimal.ROUND_HALF_UP))
                # --- FIM DA LÓGICA PARCIAL ---

            elif repro.peso_reprogramado:
                messages.error(self.request, "Não é possível calcular a receita do retrabalho. O 'Peso de 10 botões' não foi informado em nenhum apontamento anterior para esta OP.")
        
        # 2. Se não for retrabalho, verifica se é Kanban
        elif op.is_kanban:
            solicitacao = SolicitacaoQuimicaKanban.objects.filter(
                ordem_producao=op, status='PENDENTE'
            ).last()
            if solicitacao:
                quantidade_alvo_grosas = solicitacao.quantidade_solicitada

        # 3. Calcula a receita passando a quantidade alvo
        receita_calculada = op.get_receita_calculada(
            quantidade_alvo_grosas=quantidade_alvo_grosas
        )
        
        # 4. Processa a receita para buscar nomes e calcular totais
        total_camada_geral = decimal.Decimal('0.0')
        if receita_calculada:
            codigos_componentes = set()
            for dados_camada in receita_calculada.values():
                for componente in dados_camada.get('receita', []):
                    codigos_componentes.add(componente['codigo_componente'])
            
            nomes_map = {}
            if codigos_componentes:
                produtos_erp = Pro01.objects.using('acedata').filter(procod__in=list(codigos_componentes)).values('procod', 'pronom')
                nomes_map = {p['procod'].strip(): p['pronom'].strip() for p in produtos_erp}

            for camada_data in receita_calculada.values():
                total_camada = sum(c.get('quantidade_necessaria', 0) for c in camada_data.get('receita', []))
                
                for componente in camada_data.get('receita', []):
                    codigo = componente['codigo_componente']
                    componente['nome_componente'] = nomes_map.get(codigo, f'NOME NÃO ENCONTRADO ({codigo})')
                
                camada_data['total_camada'] = total_camada
                total_camada_geral += total_camada

        context['receita_calculada'] = receita_calculada
        context['solicitacao'] = solicitacao
        context['total_receita_geral'] = total_camada_geral
        
        return context
    



class SolicitarQuimicaKanbanView(LoginRequiredMixin, View):
    """
    Processa a criação de uma solicitação de matéria-prima para a Química
    a partir de uma OP Kanban.
    """
    def post(self, request, *args, **kwargs):
        op_pk = kwargs.get('op_pk')
        op = get_object_or_404(OrdemProducao, pk=op_pk, is_kanban=True)
        form = SolicitacaoQuimicaKanbanForm(request.POST)

        if form.is_valid():
            if SolicitacaoQuimicaKanban.objects.filter(ordem_producao=op, status='PENDENTE').exists():
                messages.warning(request, f"A OP {op.numero_op} já possui uma solicitação pendente para a Química.")
            else:
                solicitacao = form.save(commit=False)
                solicitacao.ordem_producao = op
                solicitacao.solicitado_por = request.user
                solicitacao.save()
                messages.success(request, f"Solicitação de {solicitacao.quantidade_solicitada} GRS para a OP {op.numero_op} enviada à Química.")
        else:
            messages.error(request, "Erro ao criar solicitação. Verifique a quantidade informada.")
        
        return redirect('producao:lista_ops_torno_laser_kanban', setor='kanban')

class IniciarRetrabalhoView(LoginRequiredMixin, View):
    """
    Processa a ação de iniciar a produção de um retrabalho,
    movendo a OP para a fila de Lançamento no Cilindro.
    """
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        reprogramacao_pk = kwargs.get('reprogramacao_pk')
        reprogramacao = get_object_or_404(ReprogramacaoOP, pk=reprogramacao_pk)
        op = reprogramacao.ordem_producao

        # Verifica se a OP está realmente pendente para retrabalho
        if op.status != OrdemProducaoStatus.PENDENTE:
            messages.warning(request, f"A OP {op.numero_op} não está mais pendente para retrabalho.")
            return redirect('producao:painel_quimica')

        # Muda o status da OP para EM_PRODUCAO
        op.status = OrdemProducaoStatus.EM_PRODUCAO
        op.save(update_fields=['status'])

        messages.success(request, f"Retrabalho da OP {op.numero_op} enviado para a fila de Lançamento no Cilindro.")
        return redirect('producao:painel_quimica')

#Painel Estoque Kanban
class PainelEstoqueKanbanView(LoginRequiredMixin, ListView):
    """
    Exibe o painel principal com a lista de todos os itens de estoque do Kanban
    e seus saldos atuais.
    """
    model = ItemEstoqueKanban
    template_name = 'producao/painel_estoque_kanban.html'
    context_object_name = 'itens_estoque'

    def get_queryset(self):
        """
        Busca todos os itens de estoque e anota os saldos correspondentes do
        modelo EstoqueKanban para uma exibição eficiente.
        """
        # Usamos select_related por ser uma relação OneToOne, é mais eficiente que prefetch_related aqui.
        # Coalesce garante que, se não houver um registro de estoque correspondente, os valores serão 0.
        queryset = ItemEstoqueKanban.objects.select_related('estoque').annotate(
            saldo_kg=Coalesce(F('estoque__saldo_peso_kg'), 0.0, output_field=DecimalField()),
            saldo_grosas=Coalesce(F('estoque__saldo_grosas_aproximado'), 0.0, output_field=DecimalField()),
            ultima_atualizacao=Coalesce(F('estoque__data_atualizacao'), None)
        ).order_by('material', 'cor')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setor_nome'] = 'Painel de Controle de Estoque Kanban'
        # Adicionaremos formulários e outras informações aqui no futuro
        return context

class PainelEstoqueKanbanView(LoginRequiredMixin, ListView):
    """
    Exibe o painel principal com a lista de todos os itens de estoque do Kanban
    e seus saldos atuais.
    """
    model = ItemEstoqueKanban
    template_name = 'producao/painel_estoque_kanban.html'
    context_object_name = 'itens_estoque'

    def get_queryset(self):
        """
        Busca todos os itens de estoque e anota os saldos correspondentes do
        modelo EstoqueKanban para uma exibição eficiente.
        """
        # Usamos select_related por ser uma relação OneToOne, é mais eficiente que prefetch_related aqui.
        # Coalesce garante que, se não houver um registro de estoque correspondente, os valores serão 0.
        queryset = ItemEstoqueKanban.objects.select_related('estoque').annotate(
            # --- CORREÇÃO APLICADA AQUI ---
            # Usamos DecimalField diretamente, sem o prefixo 'models.'
            saldo_kg=Coalesce(F('estoque__saldo_peso_kg'), 0.0, output_field=DecimalField()),
            saldo_grosas=Coalesce(F('estoque__saldo_grosas_aproximado'), 0.0, output_field=DecimalField()),
            ultima_atualizacao=Coalesce(F('estoque__data_atualizacao'), None)
        ).order_by('material', 'cor')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setor_nome'] = 'Painel de Controle de Estoque Kanban'
        # --- ATUALIZAÇÃO: Adiciona o formulário ao contexto para o modal ---
        context['solicitacao_form'] = SolicitacaoReposicaoKanbanForm()
        return context


class CriarSolicitacaoReposicaoView(LoginRequiredMixin, FormView):
    """
    Processa a submissão do formulário para criar uma nova solicitação de reposição.
    """
    form_class = SolicitacaoReposicaoKanbanForm
    success_url = reverse_lazy('producao:kanban_estoque_painel')

    def form_valid(self, form):
        item_estoque = form.cleaned_data['item_estoque']
        
        # Verifica se já existe uma solicitação pendente para o mesmo item
        if SolicitacaoReposicaoKanban.objects.filter(
            item_estoque=item_estoque, 
            status=SolicitacaoReposicaoKanban.Status.PENDENTE
        ).exists():
            messages.warning(self.request, f"Já existe uma solicitação pendente para {item_estoque}. Aguarde a finalização da produção atual.")
            return super().form_invalid(form)

        solicitacao = form.save(commit=False)
        solicitacao.solicitado_por = self.request.user
        solicitacao.save()
        
        messages.success(self.request, f"Solicitação de reposição para {item_estoque} criada com sucesso e enviada para a Química.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Transforma os erros do formulário em uma mensagem para o usuário
        error_list = '. '.join([' '.join(errors) for field, errors in form.errors.items()])
        messages.error(self.request, f"Não foi possível criar a solicitação. Erros: {error_list}")
        return super().form_invalid(form)
    
class LiberarReposicaoParaCilindroView(LoginRequiredMixin, View):
    """
    Processa a ação de 'liberar' uma solicitação de reposição Kanban,
    mudando seu status para indicar que ela está pronta para a próxima fase (Cilindro).
    """
    def post(self, request, *args, **kwargs):
        solicitacao_pk = kwargs.get('solicitacao_pk')
        solicitacao = get_object_or_404(
            SolicitacaoReposicaoKanban, 
            pk=solicitacao_pk,
            status=SolicitacaoReposicaoKanban.Status.PENDENTE
        )

        # Altera o status para 'EM_PRODUCAO', que agora representa a fila do Cilindro.
        solicitacao.status = SolicitacaoReposicaoKanban.Status.EM_PRODUCAO
        solicitacao.save(update_fields=['status'])

        messages.success(
            request, 
            f"Solicitação para '{solicitacao.item_estoque}' liberada com sucesso para o Lançamento no Cilindro."
        )
        
        return redirect('producao:painel_quimica')

# -- Lançamento no Cilindro Kanban
class ApontamentoReposicaoKanbanView(LoginRequiredMixin, View):
    """
    Controla a tela de apontamento para uma Solicitação de Reposição Kanban.
    Esta view gerencia o ciclo de vida do lançamento no cilindro para produção de estoque.
    """
    template_name = 'producao/apontamento_quimica_lancamento_reposicao_kanban.html'

    def get(self, request, *args, **kwargs):
        context = self._get_common_context(**kwargs)
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        solicitacao = get_object_or_404(SolicitacaoReposicaoKanban, pk=kwargs.get('solicitacao_pk'))
        action = next((key for key in request.POST if key.startswith('action_')), None)

        if action == 'action_iniciar':
            return self._handle_iniciar_lancamento(request, solicitacao)
        
        try:
            lancamento_id = int(action.split('_')[-1])
        except (IndexError, ValueError, TypeError):
            messages.error(request, "Ação inválida.")
            return redirect('producao:kanban_apontamento_reposicao', solicitacao_pk=solicitacao.pk)

        # --- ATUALIZAÇÃO: Adiciona a lógica para salvar sem finalizar ---
        if action.startswith('action_salvar_'):
            return self._handle_salvar_ou_finalizar(request, solicitacao, lancamento_id, finalizar=False)
            
        if action.startswith('action_finalizar_'):
            return self._handle_salvar_ou_finalizar(request, solicitacao, lancamento_id, finalizar=True)
        
        if action.startswith('action_cancelar_'):
            return self._handle_cancelar_lancamento(request, solicitacao, lancamento_id)

        messages.error(request, "Ação desconhecida.")
        return redirect('producao:kanban_apontamento_reposicao', solicitacao_pk=solicitacao.pk)

    def _get_common_context(self, **kwargs):
        solicitacao_pk = kwargs.get('solicitacao_pk')
        solicitacao = get_object_or_404(
            SolicitacaoReposicaoKanban.objects.select_related('item_estoque'), 
            pk=solicitacao_pk
        )

        lancamentos_em_andamento = solicitacao.lancamentos_cilindro.filter(data_hora_fim__isnull=True).order_by('data_hora_inicio')
        lancamentos_finalizados = solicitacao.lancamentos_cilindro.filter(data_hora_fim__isnull=False).order_by('-data_hora_fim')

        forms_em_andamento = []
        for lancamento in lancamentos_em_andamento:
            forms_em_andamento.append({
                'lancamento': lancamento,
                'form_fim': ApontamentoCilindroKanbanFimForm(prefix=f'fim_{lancamento.id}', instance=lancamento),
                'formset_paradas': ParadaCilindroKanbanFormSet(prefix=f'paradas_{lancamento.id}', queryset=lancamento.paradas.all())
            })

        total_placas_produzidas = lancamentos_finalizados.aggregate(
            total=Coalesce(Sum('quantidade_placas_total'), decimal.Decimal('0.0'))
        )['total']
        
        saldo_placas = solicitacao.quantidade_placas_solicitada - total_placas_produzidas

        return {
            'solicitacao': solicitacao,
            'setor_nome': f"Apontamento de Reposição: {solicitacao.item_estoque}",
            'form_inicio': ApontamentoCilindroKanbanInicioForm(prefix='inicio'),
            'forms_em_andamento': forms_em_andamento,
            'lancamentos_finalizados': lancamentos_finalizados,
            'total_placas_produzidas': total_placas_produzidas,
            'saldo_placas': saldo_placas,
        }

    def _handle_iniciar_lancamento(self, request, solicitacao):
        form_inicio = ApontamentoCilindroKanbanInicioForm(request.POST, prefix='inicio')
        if form_inicio.is_valid():
            lancamento = form_inicio.save(commit=False)
            lancamento.solicitacao_reposicao = solicitacao
            lancamento.data_hora_inicio = timezone.now()
            lancamento.quantidade_placas_total = 0
            lancamento.save()
            messages.success(request, f"Lançamento para a máquina {lancamento.maquina.nome_maq_erp} iniciado.")
        else:
            messages.error(request, f"Erro ao iniciar lançamento: {form_inicio.errors.as_text()}")
        
        return redirect('producao:kanban_apontamento_reposicao', solicitacao_pk=solicitacao.pk)

    def _handle_salvar_ou_finalizar(self, request, solicitacao, lancamento_id, finalizar=False):
        lancamento = get_object_or_404(LancamentoCilindro, pk=lancamento_id, solicitacao_reposicao=solicitacao)
        form_fim = ApontamentoCilindroKanbanFimForm(request.POST, prefix=f'fim_{lancamento.id}', instance=lancamento)
        formset_paradas = ParadaCilindroKanbanFormSet(request.POST, prefix=f'paradas_{lancamento.id}', queryset=lancamento.paradas.all())

        if form_fim.is_valid() and formset_paradas.is_valid():
            lancamento_salvo = form_fim.save()
            
            paradas = formset_paradas.save(commit=False)
            for parada in paradas:
                parada.lancamento = lancamento_salvo
                parada.save()
            for parada_deletada in formset_paradas.deleted_objects:
                parada_deletada.delete()

            if finalizar:
                lancamento_salvo.data_hora_fim = timezone.now()
                lancamento_salvo.save()
                messages.success(request, f'Lançamento #{lancamento.id} finalizado com sucesso.')

                total_produzido = solicitacao.lancamentos_cilindro.filter(data_hora_fim__isnull=False).aggregate(
                    total=Sum('quantidade_placas_total')
                )['total'] or 0

                if total_produzido >= solicitacao.quantidade_placas_solicitada:
                    # <-- ALTERADO: Muda o status para AGUARDANDO_CORTE ao invés de AGUARDANDO_PASTILHA
                    solicitacao.status = SolicitacaoReposicaoKanban.Status.AGUARDANDO_CORTE
                    solicitacao.save(update_fields=['status'])
                    messages.info(request, f"Produção de placas para '{solicitacao.item_estoque}' concluída. Aguardando Corte.")
                    return redirect('producao:lancamento-painel-selecao')
            else:
                messages.success(request, f'Dados do lançamento #{lancamento.id} salvos com sucesso.')
        else:
            messages.error(request, f"Erro ao salvar dados: {form_fim.errors.as_text()} {formset_paradas.errors.as_text()}")

        return redirect('producao:kanban_apontamento_reposicao', solicitacao_pk=solicitacao.pk)

    def _handle_cancelar_lancamento(self, request, solicitacao, lancamento_id):
        lancamento = get_object_or_404(LancamentoCilindro, pk=lancamento_id, solicitacao_reposicao=solicitacao)
        if lancamento.data_hora_fim is not None:
            messages.error(request, "Não é possível cancelar um lançamento já finalizado.")
        else:
            nome_maquina = lancamento.maquina.nome_maq_erp
            lancamento.delete()
            messages.warning(request, f'O lançamento em andamento para a máquina {nome_maquina} foi cancelado.')
        
        return redirect('producao:kanban_apontamento_reposicao', solicitacao_pk=solicitacao.pk)

class ConfirmarCorteReposicaoKanbanView(LoginRequiredMixin, View):
    """
    Processa a confirmação de que o corte para uma solicitação de reposição
    foi realizado, movendo-a para a próxima etapa (Controle de Pastilha).
    """
    def post(self, request, *args, **kwargs):
        solicitacao_pk = kwargs.get('solicitacao_pk')
        solicitacao = get_object_or_404(
            SolicitacaoReposicaoKanban,
            pk=solicitacao_pk,
            status=SolicitacaoReposicaoKanban.Status.AGUARDANDO_CORTE
        )

        solicitacao.status = SolicitacaoReposicaoKanban.Status.AGUARDANDO_PASTILHA
        solicitacao.save(update_fields=['status'])

        messages.success(
            request,
            f"Corte para '{solicitacao.item_estoque}' confirmado. "
            f"A solicitação foi enviada para o Controle de Pastilha."
        )

        return redirect('producao:lancamento-painel-selecao')

class ApontamentoPastilhaKanbanView(LoginRequiredMixin, View):
    """
    Controla o apontamento de medição de pastilha para uma Solicitação de Reposição Kanban.
    """
    template_name = 'producao/apontamento_pastilha_kanban.html'

    def get(self, request, *args, **kwargs):
        solicitacao = get_object_or_404(SolicitacaoReposicaoKanban, pk=kwargs.get('solicitacao_pk'))
        context = self._get_common_context(solicitacao)
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        solicitacao = get_object_or_404(SolicitacaoReposicaoKanban, pk=kwargs.get('solicitacao_pk'))
        item_estoque = solicitacao.item_estoque
        
        # O form de OP é reutilizado, mas adaptamos a lógica
        form = ControlePastilhaKanbanForm(request.POST) 

        if form.is_valid():
            apontamento_data = form.cleaned_data
            peso_medido_kg = apontamento_data.get('peso')
            peso_10_botoes_g = apontamento_data.get('peso_10_botoes')
            
            grosas_produzidas = decimal.Decimal('0.0')
            peso_bruto_grosa_g = None

            if peso_10_botoes_g and peso_10_botoes_g > 0:
                peso_bruto_grosa_g = (peso_10_botoes_g / 10) * 144
                item_estoque.peso_bruto_grosa_medio = peso_bruto_grosa_g
                item_estoque.save(update_fields=['peso_bruto_grosa_medio'])
                
                if peso_medido_kg and peso_bruto_grosa_g > 0:
                    grosas_produzidas = (peso_medido_kg * 1000) / peso_bruto_grosa_g

            # Cria ou atualiza o saldo em estoque
            estoque, _ = EstoqueKanban.objects.get_or_create(item_estoque=item_estoque)
            estoque.saldo_peso_kg = F('saldo_peso_kg') + peso_medido_kg
            estoque.saldo_grosas_aproximado = F('saldo_grosas_aproximado') + grosas_produzidas
            estoque.save()

            # Registra o movimento de entrada no estoque
            MovimentoEstoqueKanban.objects.create(
                item_estoque=item_estoque,
                tipo_movimento=MovimentoEstoqueKanban.Tipo.ENTRADA_PRODUCAO,
                peso_movimentado_kg=peso_medido_kg,
                peso_bruto_grosa_no_momento=peso_bruto_grosa_g,
                grosas_movimentadas=grosas_produzidas,
                responsavel=apontamento_data.get('responsavel'),
                solicitacao_atendida=solicitacao,
                observacao=apontamento_data.get('observacao')
            )

            # Finaliza a solicitação
            solicitacao.status = SolicitacaoReposicaoKanban.Status.CONCLUIDA
            solicitacao.save(update_fields=['status'])

            messages.success(request, f"Apontamento para '{item_estoque}' salvo com sucesso. Estoque atualizado.")
            return redirect('producao:lista_ops_pastilha')

        context = self._get_common_context(solicitacao)
        context['form'] = form
        messages.error(request, "Erro de validação. Por favor, verifique os dados inseridos.")
        return render(request, self.template_name, context)

    def _get_common_context(self, solicitacao):
        """ Monta o dicionário de contexto para a view. """
        return {
            'solicitacao': solicitacao,
            'form': ControlePastilhaForm(), # Reutiliza o form
            'setor_nome': 'Controle de Pastilha - Reposição Kanban',
        }
    
class ListaOpsKanbanView(ListView):
    """
    Exibe a fila de produção para o setor Kanban com filtros e layout responsivo.
    """
    template_name = 'producao/lista_ops_kanban.html'
    context_object_name = 'ordens_producao'
    paginate_by = 20

    def get_queryset(self):
        status_de_producao = [
            OrdemProducaoStatus.EM_PRODUCAO,
            OrdemProducaoStatus.PARCIALMENTE_FINALIZADO
        ]
        
        queryset = OrdemProducao.objects.filter(
            is_kanban=True,
            status__in=status_de_producao
        ).prefetch_related(
            'controleproducaotornolaser_apontamentos',
            'demandas__pedido__cliente'
        ).order_by('tarja', 'data_emissao')

        # Aplica os filtros do formulário
        form = OpFilterForm(self.request.GET)
        if form.is_valid():
            numero_op = form.cleaned_data.get('numero_op')
            if numero_op: queryset = queryset.filter(numero_op__icontains=numero_op)
            tamanho = form.cleaned_data.get('tamanho')
            if tamanho: queryset = queryset.filter(tamanho__icontains=tamanho)
            material = form.cleaned_data.get('material')
            if material: queryset = queryset.filter(material__icontains=material)
            numero_pedido = form.cleaned_data.get('numero_pedido')
            if numero_pedido: queryset = queryset.filter(demandas__pedido__numero_pedido__icontains=numero_pedido)
            cliente = form.cleaned_data.get('cliente')
            if cliente: queryset = queryset.filter(demandas__pedido__cliente__nome__icontains=cliente)
        
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Prepara dados adicionais para o template (lógica original mantida)
        for op in context['ordens_producao']:
            total_produzido_grosas = sum(
                ap.producao_grosas for ap in op.controleproducaotornolaser_apontamentos.all() if ap.producao_grosas is not None
            )
            op.total_produzido_grosas = total_produzido_grosas
            op.saldo_pendente_grosas = (op.quantidade_programada_total or 0) - op.total_produzido_grosas

            item_estoque = ItemEstoqueKanban.objects.filter(
                material=op.material, cor=op.cor, tamanho=op.tamanho
            ).select_related('estoque').first()

            op.estoque_disponivel_kg = item_estoque.estoque.saldo_peso_kg if item_estoque and hasattr(item_estoque, 'estoque') else decimal.Decimal('0.0')
            
            clientes = {d.pedido.cliente.nome for d in op.demandas.all() if d.pedido and d.pedido.cliente}
            op.clientes_display = ', '.join(sorted(list(clientes))) or "-"
            pedidos = {d.pedido.numero_pedido for d in op.demandas.all() if d.pedido}
            op.pedidos_display = ', '.join(sorted(list(pedidos))) or "-"

        context['setor_nome'] = 'Fila de Produção - Kanban'
        context['setor_url'] = 'kanban'
        context['filter_form'] = OpFilterForm(self.request.GET or None)
        
        return context




class ListaOpsTornoLaserView(ListView): # Adicione seu Mixin aqui
    """
    Exibe a fila de produção para os setores de Torno e Laser com filtros e layout responsivo.
    """
    template_name = 'producao/lista_ops_torno_laser.html'
    context_object_name = 'ordens_producao'
    paginate_by = 20

    def get_queryset(self):
        setor_url = self.kwargs['setor'].upper()
        setor_obj = get_object_or_404(SetorModel, nome__iexact=setor_url)

        total_produzido_subquery = ControleProducaoTornoLaser.objects.filter(
            ordem_producao=OuterRef('pk')
        ).values('ordem_producao').annotate(total=Sum('producao_grosas')).values('total')

        queryset = OrdemProducao.objects.filter(
            is_kanban=False,
            status=OrdemProducaoStatus.EM_PRODUCAO,
            saldos_por_setor__setor=setor_obj,
            saldos_por_setor__saldo_peso__gt=0
        ).annotate(
            peso_recebido_no_setor=F('saldos_por_setor__saldo_peso'),
            total_produzido_grosas=Coalesce(Subquery(total_produzido_subquery, output_field=DecimalField()), decimal.Decimal('0.0'))
        ).annotate(
            saldo_pendente_grosas=F('quantidade_programada_total') - F('total_produzido_grosas')
        ).prefetch_related('demandas__pedido__cliente').order_by('tarja', 'data_emissao').distinct()
        
        # Aplica os filtros do formulário
        form = OpFilterForm(self.request.GET)
        if form.is_valid():
            numero_op = form.cleaned_data.get('numero_op')
            if numero_op: queryset = queryset.filter(numero_op__icontains=numero_op)
            tamanho = form.cleaned_data.get('tamanho')
            if tamanho: queryset = queryset.filter(tamanho__icontains=tamanho)
            material = form.cleaned_data.get('material')
            if material: queryset = queryset.filter(material__icontains=material)
            numero_pedido = form.cleaned_data.get('numero_pedido')
            if numero_pedido: queryset = queryset.filter(demandas__pedido__numero_pedido__icontains=numero_pedido)
            cliente = form.cleaned_data.get('cliente')
            if cliente: queryset = queryset.filter(demandas__pedido__cliente__nome__icontains=cliente)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setor_url = self.kwargs['setor'].upper()
        context['setor_nome'] = f'Fila de Produção - {setor_url.title()}'
        context['setor_url'] = setor_url.lower()
        context['filter_form'] = OpFilterForm(self.request.GET or None)

        # Prepara dados adicionais para o template (lógica original mantida)
        for op in context['ordens_producao']:
            clientes = {d.pedido.cliente.nome for d in op.demandas.all() if d.pedido and d.pedido.cliente}
            op.clientes_display = ', '.join(sorted(list(clientes))) or "-"
            pedidos = {d.pedido.numero_pedido for d in op.demandas.all() if d.pedido}
            op.pedidos_display = ', '.join(sorted(list(pedidos))) or "-"
            
            saldo_kg = op.peso_recebido_no_setor
            peso_grosa_g = op.peso_bruto_grosa
            if peso_grosa_g and peso_grosa_g > 0 and saldo_kg > 0:
                op.grosas_recebidas = (saldo_kg * 1000) / peso_grosa_g
            else:
                op.grosas_recebidas = decimal.Decimal('0.0')
        
        return context

# --- Lista e Apontamento Polimento
class ListaOpsPolimentoView(ListView):
    """
    Exibe a fila de produção e os apontamentos em andamento para o setor de Polimento,
    organizados em abas e com layout responsivo (cartões/tabela).
    Ambas as listas podem ser filtradas.
    """
    template_name = 'producao/lista_ops_polimento.html'
    
    def get_queryset(self):
        # O queryset principal não será usado diretamente, pois temos duas listas separadas.
        # Retornamos none() para evitar que o Django execute uma query desnecessária.
        return ItemDemandaProducao.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setor_polimento = get_object_or_404(SetorModel, nome__iexact='Polimento')
        
        # --- 1. Inicialização do Filtro e Abas ---
        filter_form = OpFilterForm(self.request.GET or None)
        active_tab = self.request.GET.get('tab', 'fila_producao')
        context['filter_form'] = filter_form
        context['active_tab'] = active_tab
        context['setor_nome'] = 'Polimento'

        # --- 2. Query para a Aba "Fila de Produção" ---
        # Subqueries para cálculos de peso
        item_peso_em_processo_subquery = ItemPolimento.objects.filter(
            item_demanda=OuterRef('pk'),
            apontamento__data_hora_fim__isnull=True
        ).values('item_demanda').annotate(total_peso=Sum('peso_carregado')).values('total_peso')

        op_peso_em_processo_subquery = ItemPolimento.objects.filter(
            item_demanda__ordem_producao=OuterRef('ordem_producao_id'),
            apontamento__data_hora_fim__isnull=True
        ).values('item_demanda__ordem_producao').annotate(total_op_peso=Sum('peso_carregado')).values('total_op_peso')

        op_peso_ja_processado_subquery = TransferenciaEntreSetores.objects.filter(
            ordem_producao=OuterRef('ordem_producao_id'),
            setor_origem=setor_polimento
        ).values('ordem_producao').annotate(total_processado=Sum('peso_transferido')).values('total_processado')

        # Base da query para itens na fila
        itens_qs = ItemDemandaProducao.objects.filter(
            Q(ordem_producao__saldos_por_setor__setor=setor_polimento,
              ordem_producao__saldos_por_setor__saldo_peso__gt=decimal.Decimal('0.001')) |
            Q(apontamentos_polimento__apontamento__data_hora_fim__isnull=True,
              ordem_producao__saldos_por_setor__setor=setor_polimento)
        ).select_related(
            'ordem_producao', 'pedido__cliente'
        ).annotate(
            saldo_bruto_op=F('ordem_producao__saldos_por_setor__saldo_peso'),
            peso_em_processo_item=Coalesce(Subquery(item_peso_em_processo_subquery, output_field=DecimalField()), decimal.Decimal('0.0')),
            peso_em_processo_op_total=Coalesce(Subquery(op_peso_em_processo_subquery, output_field=DecimalField()), decimal.Decimal('0.0')),
            peso_ja_processado=Coalesce(Subquery(op_peso_ja_processado_subquery, output_field=DecimalField()), decimal.Decimal('0.0'))
        ).annotate(
            saldo_restante=F('saldo_bruto_op') - F('peso_em_processo_op_total')
        ).distinct()

        # --- 3. Query para a Aba "Apontamentos em Andamento" ---
        apontamentos_qs = ControlePolimento.objects.filter(
            data_hora_fim__isnull=True
        ).prefetch_related(
            'itens_no_tambor__item_demanda__ordem_producao',
            'itens_no_tambor__item_demanda__pedido'
        ).select_related('tambor').order_by('-data_hora_inicio')

        # --- 4. Aplicação dos Filtros ---
        if filter_form.is_valid():
            numero_op = filter_form.cleaned_data.get('numero_op')
            tamanho = filter_form.cleaned_data.get('tamanho')
            cliente = filter_form.cleaned_data.get('cliente')
            numero_pedido = filter_form.cleaned_data.get('numero_pedido')
            acabamento = filter_form.cleaned_data.get('acabamento')
            
            # Aplica filtros na query da FILA
            if numero_op:
                itens_qs = itens_qs.filter(ordem_producao__numero_op__icontains=numero_op)
            if tamanho:
                itens_qs = itens_qs.filter(ordem_producao__tamanho__icontains=tamanho)
            if cliente:
                itens_qs = itens_qs.filter(pedido__cliente__nome__icontains=cliente)
            if numero_pedido:
                itens_qs = itens_qs.filter(pedido__numero_pedido__icontains=numero_pedido)
            if acabamento:
                itens_qs = itens_qs.filter(ordem_producao__acabamento=acabamento)

            # Aplica filtros na query de APONTAMENTOS
            if numero_op:
                apontamentos_qs = apontamentos_qs.filter(itens_no_tambor__item_demanda__ordem_producao__numero_op__icontains=numero_op)
            if tamanho:
                apontamentos_qs = apontamentos_qs.filter(itens_no_tambor__item_demanda__ordem_producao__tamanho__icontains=tamanho)
            if cliente:
                apontamentos_qs = apontamentos_qs.filter(itens_no_tambor__item_demanda__pedido__cliente__nome__icontains=cliente)
            if numero_pedido:
                apontamentos_qs = apontamentos_qs.filter(itens_no_tambor__item_demanda__pedido__numero_pedido__icontains=numero_pedido)
            if acabamento:
                apontamentos_qs = apontamentos_qs.filter(itens_no_tambor__item_demanda__ordem_producao__acabamento=acabamento)

        # Filtra apenas itens com saldo positivo para exibição
        itens_para_exibir = [
            item for item in itens_qs 
            if item.saldo_restante > decimal.Decimal('0.0001') or item.peso_em_processo_item > 0
        ]
        
        apontamentos_com_info = list(apontamentos_qs.distinct())

        for ap in apontamentos_com_info:
            op_numbers = set()
            pedido_numbers = set()
            for item in ap.itens_no_tambor.all():
                op_numbers.add(item.item_demanda.ordem_producao.numero_op)
                if item.item_demanda.pedido:
                    pedido_numbers.add(item.item_demanda.pedido.numero_pedido)
            
            ap.ops_display = ', '.join(sorted(list(op_numbers)))
            ap.pedidos_display = ', '.join(sorted(list(pedido_numbers)))

        context['itens_na_fila'] = sorted(itens_para_exibir, key=lambda x: (x.ordem_producao.tamanho, x.ordem_producao.numero_op))
        context['apontamentos_em_andamento'] = apontamentos_com_info
        
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        item_ids_selecionados = request.POST.getlist('item_selecionado')

        if not item_ids_selecionados:
            messages.error(request, "Nenhum item de produção foi selecionado.")
            return redirect('producao:lista_ops_polimento')

        selected_items = ItemDemandaProducao.objects.filter(pk__in=item_ids_selecionados).select_related('ordem_producao')
        
        # --- LÓGICA DE VALIDAÇÃO (permanece a mesma) ---
        if len(selected_items) > 1:
            tamanhos = {item.ordem_producao.tamanho for item in selected_items}
            acabamentos = {item.ordem_producao.acabamento for item in selected_items}

            if len(selected_items) > len(tamanhos):
                messages.error(request, "Não é permitido agrupar itens de mesmo tamanho no mesmo tambor.")
                return redirect('producao:lista_ops_polimento')
            
            if len(acabamentos) > 1:
                messages.error(request, "Não é permitido agrupar itens com tipos de acabamento diferentes.")
                return redirect('producao:lista_ops_polimento')

        # --- MUDANÇA PRINCIPAL ---
        # 1. Armazena os IDs selecionados na sessão do usuário
        request.session['polimento_agrupamento_ids'] = item_ids_selecionados
        
        # 2. Redireciona para uma nova URL de criação de apontamento
        return redirect('producao:apontamento_polimento_novo')


class ApontamentoPolimentoView(View):
    template_name = 'producao/apontamento_polimento.html'

    def get_formset(self, data=None, initial=None, queryset=None, extra=0):
        """Helper para criar a classe do formset dinamicamente."""
        ItemPolimentoFormSet = modelformset_factory(
            ItemPolimento,
            form=ItemPolimentoForm,
            formset=BaseItemPolimentoFormSet,
            extra=extra,
            can_delete=False
        )
        if data:
            return ItemPolimentoFormSet(data, prefix='items', queryset=queryset or ItemPolimento.objects.none())
        return ItemPolimentoFormSet(prefix='items', initial=initial, queryset=queryset or ItemPolimento.objects.none())

    def get(self, request, *args, **kwargs):
        apontamento_id = kwargs.get('apontamento_id')
        # ALTERAÇÃO CIRÚRGICA 1: Captura a origem da URL
        origem = request.GET.get('origem')
        
        if apontamento_id:
            apontamento = get_object_or_404(ControlePolimento, pk=apontamento_id)
            form = ApontamentoPolimentoForm(instance=apontamento)
            item_formset = self.get_formset(queryset=ItemPolimento.objects.filter(apontamento=apontamento))
            parada_formset = ParadaPolimentoFormSet(prefix='paradas', queryset=ParadaPolimento.objects.filter(apontamento_polimento=apontamento))
        
        else:
            item_ids = request.session.get('polimento_agrupamento_ids')
            if not item_ids:
                messages.error(request, "Nenhum item selecionado para o agrupamento.")
                return redirect('producao:lista_ops_polimento')

            apontamento = None
            form = ApontamentoPolimentoForm()
            
            itens_selecionados = ItemDemandaProducao.objects.filter(pk__in=item_ids).select_related('ordem_producao', 'pedido__cliente')
            initial_data = [{'item_demanda': item.pk} for item in itens_selecionados]
            
            item_formset = self.get_formset(initial=initial_data, extra=len(initial_data))
            
            for i, form_item in enumerate(item_formset.forms):
                if i < len(itens_selecionados):
                    form_item.instance.item_demanda = itens_selecionados[i]
            
            parada_formset = ParadaPolimentoFormSet(prefix='paradas', queryset=ParadaPolimento.objects.none())

        # ALTERAÇÃO CIRÚRGICA 2: Passa a origem para o contexto
        context = self._get_common_context(apontamento, form, item_formset, parada_formset, origem=origem)
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        apontamento_id = kwargs.get('apontamento_id')
        apontamento = get_object_or_404(ControlePolimento, pk=apontamento_id) if apontamento_id else None
        # ALTERAÇÃO CIRÚRGICA 3: Captura a origem do formulário
        origem = request.POST.get('origem')

        # ALTERAÇÃO CIRÚRGICA 4: Define a URL de retorno com base na origem
        redirect_url = reverse('producao:lista_ops_polimento')
        if origem == 'em_andamento':
            redirect_url = f"{redirect_url}?tab=em_andamento"

        if 'action_cancelar' in request.POST and apontamento:
            apontamento.delete()
            messages.warning(request, f"Apontamento #{apontamento.id} foi cancelado.")
            return redirect(redirect_url)

        form = ApontamentoPolimentoForm(request.POST, instance=apontamento)
        item_formset = self.get_formset(data=request.POST, queryset=ItemPolimento.objects.filter(apontamento=apontamento) if apontamento else ItemPolimento.objects.none())
        parada_formset = ParadaPolimentoFormSet(request.POST, prefix='paradas', queryset=ParadaPolimento.objects.filter(apontamento_polimento=apontamento) if apontamento else ParadaPolimento.objects.none())

        if form.is_valid() and item_formset.is_valid() and parada_formset.is_valid():
            
            if 'action_finalizar' in request.POST:
                itens_sem_destino = []
                for form_item in item_formset:
                    peso = form_item.cleaned_data.get('peso_carregado', 0)
                    destino = form_item.cleaned_data.get('proximo_setor')
                    if peso > 0 and not destino:
                        item_demanda = form_item.cleaned_data.get('item_demanda')
                        itens_sem_destino.append(item_demanda.ordem_producao.numero_op)

                if itens_sem_destino:
                    messages.error(request, f"Não é possível finalizar. As seguintes OPs precisam de um 'Próximo Setor' definido: {', '.join(set(itens_sem_destino))}")
                    context = self._get_common_context(apontamento, form, item_formset, parada_formset, origem=origem)
                    return render(request, self.template_name, context)

            apontamento_salvo = form.save(commit=False)
            if not apontamento:
                apontamento_salvo.data_hora_inicio = timezone.now()
            apontamento_salvo.save()

            itens = item_formset.save(commit=False)
            for item in itens:
                item.apontamento = apontamento_salvo
                item.save()
            item_formset.save_m2m()
            
            if 'polimento_agrupamento_ids' in request.session:
                del request.session['polimento_agrupamento_ids']
            
            paradas = parada_formset.save(commit=False)
            for parada in paradas:
                parada.apontamento_polimento = apontamento_salvo
                parada.save()
            for obj in parada_formset.deleted_objects:
                obj.delete()
            
            if 'action_finalizar' in request.POST:
                apontamento_salvo.data_hora_fim = timezone.now()
                apontamento_salvo.save()
                self._consumir_saldo_ops(apontamento_salvo)
                self._transferir_saldo_individualmente(item_formset, apontamento_salvo)
                messages.success(request, f"Apontamento de polimento #{apontamento_salvo.id} finalizado com sucesso!")
                return redirect(redirect_url)
            
            else:
                messages.success(request, "Andamento do apontamento salvo com sucesso.")
                # ALTERAÇÃO CIRÚRGICA 5: Adiciona o parâmetro de origem ao redirecionar após salvar
                redirect_edit_url = reverse('producao:apontamento_polimento', args=[apontamento_salvo.id])
                if origem:
                    redirect_edit_url += f"?origem={origem}"
                return redirect(redirect_edit_url)
        
        else:
            messages.error(request, "Erro de validação. Por favor, verifique os dados inseridos.")
            
            if not apontamento:
                item_ids = request.session.get('polimento_agrupamento_ids', [])
                itens_selecionados = ItemDemandaProducao.objects.filter(pk__in=item_ids).select_related('ordem_producao', 'pedido__cliente')
                
                for i, form_item in enumerate(item_formset.forms):
                    if i < len(itens_selecionados):
                        form_item.instance.item_demanda = itens_selecionados[i]

            context = self._get_common_context(apontamento, form, item_formset, parada_formset, origem=origem)
            return render(request, self.template_name, context)

    # ALTERAÇÃO CIRÚRGICA 6: Atualiza a assinatura do método
    def _get_common_context(self, apontamento, form, item_formset, parada_formset, origem=None):
        return {
            'apontamento': apontamento,
            'form': form,
            'item_formset': item_formset,
            'parada_formset': parada_formset,
            'setor_nome': 'Apontamento - Polimento',
            'origem': origem # Adiciona ao contexto
        }

    def _consumir_saldo_ops(self, apontamento):
        setor_polimento = get_object_or_404(SetorModel, nome__iexact='Polimento')
        for item_polido in apontamento.itens_no_tambor.all():
            op = item_polido.item_demanda.ordem_producao
            peso_consumido = item_polido.peso_carregado
            
            if peso_consumido > 0:
                saldo_op, _ = SaldoOPSetor.objects.get_or_create(
                    ordem_producao=op,
                    setor=setor_polimento
                )
                saldo_op.saldo_peso = F('saldo_peso') - peso_consumido
                saldo_op.save()

    def _transferir_saldo_individualmente(self, item_formset, apontamento):
        setor_origem = get_object_or_404(SetorModel, nome__iexact='Polimento')
        for form in item_formset:
            if form.is_valid() and form.has_changed():
                cleaned_data = form.cleaned_data
                setor_destino = cleaned_data.get('proximo_setor')
                peso_transferido = cleaned_data.get('peso_carregado')
                
                if not setor_destino or not peso_transferido or peso_transferido <= 0:
                    continue

                item_demanda = cleaned_data.get('item_demanda')
                op = item_demanda.ordem_producao

                TransferenciaEntreSetores.objects.create(
                    ordem_producao=op,
                    setor_origem=setor_origem,
                    setor_destino=setor_destino,
                    peso_transferido=peso_transferido,
                    responsavel=apontamento.responsavel
                )
                
                saldo_destino, _ = SaldoOPSetor.objects.get_or_create(
                    ordem_producao=op,
                    setor=setor_destino
                )
                saldo_destino.saldo_peso = F('saldo_peso') + peso_transferido
                saldo_destino.save()


# -- Escolha Final
class ListaOpsConferenciaView(ListView):
    """
    Exibe a fila de produção para o setor de Conferência (Escolha Final),
    com filtros e layout responsivo.
    """
    template_name = 'producao/lista_ops_conferencia.html'
    context_object_name = 'itens_no_setor'
    paginate_by = 20 # Adicionado para consistência

    def get_queryset(self):
        """
        Busca os itens de demanda na Escolha Final e aplica os filtros do formulário.
        """
        setor = get_object_or_404(SetorModel, nome__iexact='Escolha Final')

        queryset = ItemDemandaProducao.objects.filter(
            ordem_producao__saldos_por_setor__setor=setor,
            ordem_producao__saldos_por_setor__saldo_peso__gt=0
        ).select_related(
            'ordem_producao', 'pedido__cliente'
        ).annotate(
            saldo_no_setor=F('ordem_producao__saldos_por_setor__saldo_peso')
        ).order_by('ordem_producao__data_emissao', 'ordem_producao__numero_op').distinct()

        # Aplica os filtros do formulário
        form = OpFilterForm(self.request.GET)
        if form.is_valid():
            numero_op = form.cleaned_data.get('numero_op')
            if numero_op:
                queryset = queryset.filter(ordem_producao__numero_op__icontains=numero_op)
            
            tamanho = form.cleaned_data.get('tamanho')
            if tamanho:
                queryset = queryset.filter(ordem_producao__tamanho__icontains=tamanho)

            numero_pedido = form.cleaned_data.get('numero_pedido')
            if numero_pedido:
                queryset = queryset.filter(pedido__numero_pedido__icontains=numero_pedido)

            cliente = form.cleaned_data.get('cliente')
            if cliente:
                queryset = queryset.filter(pedido__cliente__nome__icontains=cliente)

        return queryset

    def get_context_data(self, **kwargs):
        """ 
        Adiciona o formulário de filtro e o saldo em grosas calculado ao contexto. 
        """
        context = super().get_context_data(**kwargs)
        context['setor_nome'] = 'Fila de Produção - Conferência'
        context['filter_form'] = OpFilterForm(self.request.GET or None)

        # Calcula o saldo em grosas para cada item
        for item in context['itens_no_setor']:
            saldo_kg = item.saldo_no_setor
            peso_grosa_g = item.ordem_producao.peso_liquido_grosa
            
            if peso_grosa_g and peso_grosa_g > 0:
                item.saldo_grosas_calculado = (saldo_kg * 1000) / peso_grosa_g
            else:
                item.saldo_grosas_calculado = decimal.Decimal('0.0')

        return context

class ApontamentoConferenciaView(View):
    template_name = 'producao/apontamento_conferencia.html'

    def get(self, request, *args, **kwargs):
        # Otimiza a consulta buscando todos os dados relacionados de uma vez
        item = get_object_or_404(
            ItemDemandaProducao.objects.select_related('ordem_producao', 'pedido__cliente'), 
            pk=kwargs.get('item_id')
        )
        form = ConferenciaEscolhaFinalForm(item_demanda=item)
        
        setor_conferencia = get_object_or_404(SetorModel, nome__iexact='Escolha Final')
        saldo_atual = SaldoOPSetor.objects.filter(
            ordem_producao=item.ordem_producao, setor=setor_conferencia
        ).first()

        context = {
            'item': item,
            'form': form,
            'setor_nome': 'Apontamento - Conferência',
            'saldo_disponivel': saldo_atual.saldo_peso if saldo_atual else 0
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        item = get_object_or_404(ItemDemandaProducao, pk=kwargs.get('item_id'))
        form = ConferenciaEscolhaFinalForm(request.POST, item_demanda=item)
        if form.is_valid():
            apontamento = form.save(commit=False)
            apontamento.item_demanda = item
            apontamento.data_hora_inicio = timezone.now()
            apontamento.data_hora_fim = timezone.now()
            apontamento.save()

            setor_origem = get_object_or_404(SetorModel, nome__iexact='Escolha Final')
            peso_a_transferir = form.cleaned_data.get('peso_a_transferir', 0) or 0
            proximo_setor = form.cleaned_data.get('proximo_setor')

            if peso_a_transferir > 0 and proximo_setor:
                saldo_op, _ = SaldoOPSetor.objects.get_or_create(ordem_producao=item.ordem_producao, setor=setor_origem)
                
                peso_real_a_debitar = min(saldo_op.saldo_peso, peso_a_transferir)
                
                saldo_op.saldo_peso = F('saldo_peso') - peso_real_a_debitar
                saldo_op.save()

                TransferenciaEntreSetores.objects.create(
                    ordem_producao=item.ordem_producao, 
                    setor_origem=setor_origem, 
                    setor_destino=proximo_setor,
                    peso_transferido=peso_real_a_debitar, 
                    responsavel=apontamento.responsavel
                )
                
                saldo_destino, _ = SaldoOPSetor.objects.get_or_create(ordem_producao=item.ordem_producao, setor=proximo_setor)
                saldo_destino.saldo_peso = F('saldo_peso') + peso_real_a_debitar
                saldo_destino.save()
                
                if proximo_setor.nome == 'CONTROLE DE QUALIDADE':
                    item.status_item = ItemDemandaStatus.AGUARDANDO_CONTROLE_QUALIDADE
                    item.save(update_fields=['status_item'])
            
            saldo_op, _ = SaldoOPSetor.objects.get_or_create(ordem_producao=item.ordem_producao, setor=setor_origem)
            saldo_op.refresh_from_db()
            if saldo_op.saldo_peso <= 0.001:
                messages.info(request, f"Todo o saldo da OP {item.ordem_producao.numero_op} foi processado neste setor.")

            messages.success(request, "Conferência finalizada com sucesso!")
            return redirect('producao:lista_ops_conferencia')
            
        return render(request, self.template_name, {'item': item, 'form': form, 'setor_nome': 'Apontamento - Conferência'})

class ListaOpsControleQualidadeView(ListView):
    """
    Exibe a fila de produção para o setor de Controle de Qualidade.
    Refatorada para buscar os dados do cliente e calcular o saldo em grosas.
    """
    template_name = 'producao/lista_ops_controle_qualidade.html'
    context_object_name = 'itens_no_setor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setor_nome'] = 'Fila de Produção - Controle de Qualidade'
        
        itens_em_andamento_ids = ControleQualidadeEsteira.objects.filter(
            data_hora_fim__isnull=True
        ).values_list('item_demanda_id', flat=True)
        
        context['itens_em_andamento_ids'] = list(itens_em_andamento_ids)
        
        # --- LÓGICA ADICIONADA PARA CÁLCULO DE GROSAS ---
        # Itera sobre os itens já buscados para adicionar o cálculo do saldo em grosas.
        for item in context['itens_no_setor']:
            saldo_kg = item.saldo_no_setor
            peso_grosa_g = item.ordem_producao.peso_liquido_grosa
            
            # Garante que o cálculo só seja feito se houver peso de grosa definido
            if peso_grosa_g and peso_grosa_g > 0:
                item.saldo_grosas_calculado = (saldo_kg * 1000) / peso_grosa_g
            else:
                item.saldo_grosas_calculado = decimal.Decimal('0.0')
        
        return context

    def get_queryset(self):
        setor = get_object_or_404(SetorModel, nome='CONTROLE DE QUALIDADE')
        
        # A consulta agora otimiza a busca pelo cliente.
        return ItemDemandaProducao.objects.filter(
            ordem_producao__saldos_por_setor__setor=setor,
            ordem_producao__saldos_por_setor__saldo_peso__gt=0
        ).exclude(
            status_item=ItemDemandaStatus.FINALIZADO
        ).select_related(
            'ordem_producao', 'pedido__cliente'
        ).annotate(
            saldo_no_setor=F('ordem_producao__saldos_por_setor__saldo_peso')
        ).order_by('ordem_producao__numero_op').distinct()


class ApontamentoControleQualidadeView(View):
    """
    Gerencia a tela de apontamento de Controle de Qualidade, lidando tanto com o
    início de uma nova inspeção quanto com a finalização de uma já existente.
    """
    template_name = 'producao/apontamento_controle_qualidade.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Método executado antes do GET ou POST para preparar dados comuns.
        """
        self.item = get_object_or_404(ItemDemandaProducao, pk=kwargs.get('item_id'))
        # Busca por um apontamento em andamento para este item específico
        self.apontamento_em_andamento = ControleQualidadeEsteira.objects.filter(
            item_demanda=self.item, data_hora_fim__isnull=True
        ).first()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """ Exibe o formulário de início ou de fim, dependendo do status da inspeção. """
        if self.apontamento_em_andamento:
            # Se já existe um apontamento, mostra o formulário de finalização
            form = ApontamentoCQFimForm(instance=self.apontamento_em_andamento, item_demanda=self.item)
        else:
            # Caso contrário, mostra o formulário para iniciar uma nova inspeção
            form = ApontamentoCQInicioForm()
        
        context = self._get_common_context(form)
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """ Processa o início ou a finalização de uma inspeção. """
        # Verifica se a ação é de iniciar uma nova inspeção
        if 'action_iniciar' in request.POST:
            form = ApontamentoCQInicioForm(request.POST)
            if form.is_valid():
                apontamento = form.save(commit=False)
                apontamento.item_demanda = self.item
                apontamento.data_hora_inicio = timezone.now()
                apontamento.save()
                messages.success(request, f"Inspeção para o item da OP {self.item.ordem_producao.numero_op} iniciada.")
                # Recarrega a mesma página, que agora estará no modo de finalização
                return redirect('producao:apontamento_controle_qualidade', item_id=self.item.id)
        
        # Se não for iniciar, a ação é de finalizar
        elif self.apontamento_em_andamento:
            form = ApontamentoCQFimForm(request.POST, instance=self.apontamento_em_andamento, item_demanda=self.item)
            if form.is_valid():
                apontamento_salvo = form.save(commit=False)
                apontamento_salvo.data_hora_fim = timezone.now()
                apontamento_salvo.save()

                # Lógica de transferência...
                peso_aprovado = form.cleaned_data.get('peso_total_aprovado') or 0
                peso_a_devolver = form.cleaned_data.get('peso_a_devolver') or 0
                setor_origem = get_object_or_404(SetorModel, nome='CONTROLE DE QUALIDADE')

                if peso_aprovado > 0:
                    op = self.item.ordem_producao
                    quantidade_grosas = (peso_aprovado * 1000) / op.peso_liquido_grosa if op.peso_liquido_grosa and op.peso_liquido_grosa > 0 else 0
                    setor_destino_nome = 'CONTAGEM ACIMA 80' if quantidade_grosas > 80 else 'CONTAGEM ATE 80'
                    setor_destino = get_object_or_404(SetorModel, nome=setor_destino_nome)
                    self._realizar_transferencia(self.item, setor_origem, setor_destino, peso_aprovado, apontamento_salvo.responsavel)
                    
                if peso_a_devolver > 0:
                    setor_conferencia = get_object_or_404(SetorModel, nome='Escolha Final')
                    self._realizar_transferencia(self.item, setor_origem, setor_conferencia, peso_a_devolver, apontamento_salvo.responsavel)

                # Atualiza o status do item se todo o saldo do setor foi consumido
                saldo_origem = SaldoOPSetor.objects.get(ordem_producao=self.item.ordem_producao, setor=setor_origem)
                if saldo_origem.saldo_peso <= decimal.Decimal('0.001'):
                    self.item.status_item = ItemDemandaStatus.FINALIZADO
                    self.item.save(update_fields=['status_item'])
                
                messages.success(request, "Controle de Qualidade finalizado com sucesso!")
                return redirect('producao:lista_ops_controle_qualidade')
        else:
            # Caso de erro (ex: tentar finalizar algo que não foi iniciado)
            messages.error(request, "Ação inválida ou a inspeção não foi encontrada.")
            return redirect('producao:lista_ops_controle_qualidade')

        # Se o formulário for inválido, renderiza a página novamente com os erros
        context = self._get_common_context(form)
        return render(request, self.template_name, context)

    def _get_common_context(self, form):
        """ Monta o dicionário de contexto comum. """
        setor_cq = get_object_or_404(SetorModel, nome='CONTROLE DE QUALIDADE')
        saldo_atual = SaldoOPSetor.objects.filter(ordem_producao=self.item.ordem_producao, setor=setor_cq).first()

        # --- CORREÇÃO APLICADA AQUI ---
        # Calcula o peso de 10 botões no backend
        peso_10_botoes = 0
        peso_grosa = self.item.ordem_producao.peso_liquido_grosa
        if peso_grosa and peso_grosa > 0:
            peso_10_botoes = (peso_grosa / 144) * 10

        return {
            'apontamento': self.apontamento_em_andamento,
            'item': self.item,
            'form': form,
            'setor_nome': 'Apontamento - Controle de Qualidade',
            'saldo_disponivel': saldo_atual.saldo_peso if saldo_atual else 0,
            'peso_10_botoes': peso_10_botoes, # Envia o valor calculado para o template
        }

    def _realizar_transferencia(self, item, setor_origem, setor_destino, peso, responsavel):
        """ Função auxiliar para criar a transferência e atualizar os saldos. """
        TransferenciaEntreSetores.objects.create(
            ordem_producao=item.ordem_producao, setor_origem=setor_origem,
            setor_destino=setor_destino, peso_transferido=peso, responsavel=responsavel
        )
        SaldoOPSetor.objects.filter(
            ordem_producao=item.ordem_producao, setor=setor_origem
        ).update(saldo_peso=F('saldo_peso') - peso)
        saldo_destino, _ = SaldoOPSetor.objects.get_or_create(
            ordem_producao=item.ordem_producao, setor=setor_destino
        )
        saldo_destino.saldo_peso = F('saldo_peso') + peso
        saldo_destino.save()

# -- Contagem e Embalagem
class ListaOpsContagemView(ListView):
    """
    Exibe as filas de produção para o setor de Contagem, separadas por
    tamanho de lote em abas. A listagem é baseada nos Itens de Demanda.
    Refatorada para buscar os dados do cliente e calcular o saldo em grosas.
    """
    template_name = 'producao/lista_ops_contagem.html'
    context_object_name = 'itens_pequenos_lotes' # Padrão para a primeira aba

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        setor_grandes_nome = 'CONTAGEM ACIMA 80'
        setor_pequenos_nome = 'CONTAGEM ATE 80'

        setor_grandes = get_object_or_404(SetorModel, nome=setor_grandes_nome)
        
        # --- CONSULTA CORRIGIDA ---
        # O select_related agora busca o cliente de forma otimizada.
        context['itens_grandes_lotes'] = ItemDemandaProducao.objects.filter(
            ordem_producao__saldos_por_setor__setor=setor_grandes,
            ordem_producao__saldos_por_setor__saldo_peso__gt=0
        ).select_related(
            'ordem_producao', 'pedido__cliente'
        ).annotate(
            saldo_no_setor=F('ordem_producao__saldos_por_setor__saldo_peso')
        ).order_by('ordem_producao__numero_op').distinct()

        # --- LÓGICA ADICIONADA PARA CÁLCULO DE GROSAS ---
        # Itera sobre as duas listas para adicionar o cálculo do saldo em grosas.
        for item_list in [context['itens_pequenos_lotes'], context['itens_grandes_lotes']]:
            for item in item_list:
                saldo_kg = item.saldo_no_setor
                peso_grosa_g = item.ordem_producao.peso_liquido_grosa
                
                if peso_grosa_g and peso_grosa_g > 0 and saldo_kg > 0:
                    item.saldo_grosas_calculado = (saldo_kg * 1000) / peso_grosa_g
                else:
                    item.saldo_grosas_calculado = decimal.Decimal('0.0')

        context['setor_origem_pequenos'] = setor_pequenos_nome
        context['setor_origem_grandes'] = setor_grandes_nome
        
        context['active_tab'] = self.request.GET.get('tab', 'pequenos')
        context['setor_nome'] = 'Fila de Produção - Contagem e Embalagem'
        return context

    def get_queryset(self):
        """ Retorna a queryset para a primeira aba (lotes pequenos). """
        setor_pequenos = get_object_or_404(SetorModel, nome='CONTAGEM ATE 80')
        
        # --- CONSULTA CORRIGIDA ---
        # O select_related agora busca o cliente de forma otimizada.
        return ItemDemandaProducao.objects.filter(
            ordem_producao__saldos_por_setor__setor=setor_pequenos,
            ordem_producao__saldos_por_setor__saldo_peso__gt=0
        ).select_related(
            'ordem_producao', 'pedido__cliente'
        ).annotate(
            saldo_no_setor=F('ordem_producao__saldos_por_setor__saldo_peso')
        ).order_by('ordem_producao__numero_op').distinct()


class ApontamentoContagemView(View):
    """
    Gerencia o apontamento de Contagem Final para um Item de Demanda.
    O processo é instantâneo e agora gera o saldo em grosas para a Embalagem.
    """
    template_name = 'producao/apontamento_contagem.html'

    def get(self, request, *args, **kwargs):
        # Otimiza a consulta buscando todos os dados relacionados de uma vez
        item = get_object_or_404(
            ItemDemandaProducao.objects.select_related('ordem_producao', 'pedido__cliente'), 
            pk=kwargs.get('item_id')
        )
        form = ContagemFinalForm()
        
        setor_nome = self.kwargs.get('setor_origem')
        setor_contagem = get_object_or_404(SetorModel, nome=setor_nome)
        saldo_atual = SaldoOPSetor.objects.filter(
            ordem_producao=item.ordem_producao, setor=setor_contagem
        ).first()

        context = {
            'item': item,
            'form': form,
            'setor_nome': 'Apontamento - Contagem Final',
            'saldo_disponivel': saldo_atual.saldo_peso if saldo_atual else 0
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        item = get_object_or_404(ItemDemandaProducao, pk=kwargs.get('item_id'))
        form = ContagemFinalForm(request.POST)

        if form.is_valid():
            apontamento = form.save(commit=False)
            apontamento.ordem_producao = item.ordem_producao
            apontamento.data_hora_inicio = timezone.now()
            apontamento.data_hora_fim = timezone.now()
            apontamento.save()

            pesagem_str = form.cleaned_data.get('pesagem')
            total_embalagens = form.cleaned_data.get('total_embalagem', 0)
            
            match = re.match(r'G_(\d+)', pesagem_str)
            grosas_por_embalagem = int(match.group(1)) if match else 0
            
            total_grosas_calculada = decimal.Decimal(grosas_por_embalagem * total_embalagens)

            if total_grosas_calculada > 0:
                saldo_embalagem, created = SaldoItemEmbalagem.objects.get_or_create(
                    item_demanda=item
                )
                saldo_embalagem.saldo_grosas = F('saldo_grosas') + total_grosas_calculada
                saldo_embalagem.save()
                messages.info(request, f"{total_grosas_calculada} grosas foram transferidas para o saldo da Embalagem.")

            setor_nome = self.kwargs.get('setor_origem')
            setor_origem = get_object_or_404(SetorModel, nome=setor_nome)
            
            saldo_op = get_object_or_404(
                SaldoOPSetor, 
                ordem_producao=item.ordem_producao, 
                setor=setor_origem
            )
            
            saldo_op.saldo_peso = 0
            saldo_op.save()

            messages.success(request, f"Contagem final para a OP {item.ordem_producao.numero_op} registrada com sucesso!")
            return redirect('producao:lista_ops_contagem')
        
        setor_nome = self.kwargs.get('setor_origem')
        setor_contagem = get_object_or_404(SetorModel, nome=setor_nome)
        saldo_atual = SaldoOPSetor.objects.filter(
            ordem_producao=item.ordem_producao, setor=setor_contagem
        ).first()

        context = {
            'item': item,
            'form': form,
            'setor_nome': 'Apontamento - Contagem Final',
            'saldo_disponivel': saldo_atual.saldo_peso if saldo_atual else 0
        }
        return render(request, self.template_name, context)
# -- Lista e Apontamento do Tingimento
class ListaOpsTingimentoView(ListView):
    """
    Lista os itens de demanda para o tingimento e os lotes em andamento,
    organizados em abas, com filtros e layout responsivo.
    """
    template_name = 'producao/lista_ops_tingimento.html'
    context_object_name = 'itens_para_tingir'
    paginate_by = 20

    def get_queryset(self):
        setor_tingimento_nome = 'TINGIMENTO'
        
        queryset = ItemDemandaProducao.objects.filter(
            ordem_producao__requer_tingimento=True,
            ordem_producao__saldos_por_setor__setor__nome=setor_tingimento_nome,
            ordem_producao__saldos_por_setor__saldo_peso__gt=0
        ).exclude(
            status_item=ItemDemandaStatus.FINALIZADO
        ).select_related(
            'ordem_producao', 'pedido__cliente'
        ).annotate(
            saldo_no_setor=F('ordem_producao__saldos_por_setor__saldo_peso')
        ).distinct().order_by('cor_final', 'ordem_producao__tamanho')

        # Aplica os filtros do formulário
        form = OpFilterForm(self.request.GET)
        if form.is_valid():
            numero_op = form.cleaned_data.get('numero_op')
            if numero_op:
                queryset = queryset.filter(ordem_producao__numero_op__icontains=numero_op)
            
            tamanho = form.cleaned_data.get('tamanho')
            if tamanho:
                queryset = queryset.filter(ordem_producao__tamanho__icontains=tamanho)

            numero_pedido = form.cleaned_data.get('numero_pedido')
            if numero_pedido:
                queryset = queryset.filter(pedido__numero_pedido__icontains=numero_pedido)

            cliente = form.cleaned_data.get('cliente')
            if cliente:
                queryset = queryset.filter(pedido__cliente__nome__icontains=cliente)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['setor_nome'] = 'Tingimento'
        context['active_tab'] = self.request.GET.get('tab', 'fila_producao')
        context['filter_form'] = OpFilterForm(self.request.GET or None)

        # Busca a lista de lotes em andamento para a segunda aba
        context['lotes_em_andamento'] = LoteTingimento.objects.filter(status='EM_ANDAMENTO').prefetch_related('itens_no_lote__item_demanda__ordem_producao')
        
        # Calcula o saldo em grosas para cada item na fila
        for item in context['itens_para_tingir']:
            saldo_kg = item.saldo_no_setor
            peso_grosa_g = item.ordem_producao.peso_liquido_grosa
            
            if peso_grosa_g and peso_grosa_g > 0:
                item.saldo_grosas_calculado = (saldo_kg * 1000) / peso_grosa_g
            else:
                item.saldo_grosas_calculado = decimal.Decimal('0.0')

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        item_ids = request.POST.getlist('item_selecionado')
        if not item_ids:
            messages.error(request, "Nenhum item foi selecionado para o tingimento.")
            return redirect('producao:lista_ops_tingimento')

        itens_selecionados = ItemDemandaProducao.objects.filter(pk__in=item_ids).select_related('ordem_producao')

        primeiro_item = itens_selecionados.first()
        cor_final_alvo = primeiro_item.cor_final
        tamanhos_e_artigos = {}
        for item in itens_selecionados:
            if item.cor_final != cor_final_alvo:
                messages.error(request, "Erro de agrupamento: Todos os itens devem ter a mesma Cor Final.")
                return redirect('producao:lista_ops_tingimento')
            
            tamanho = item.ordem_producao.tamanho
            artigo = item.ordem_producao.artigo
            
            if tamanho in tamanhos_e_artigos and tamanhos_e_artigos[tamanho] != artigo:
                messages.error(request, f"Erro de agrupamento: Itens de tamanho '{tamanho}' devem ser do mesmo artigo.")
                return redirect('producao:lista_ops_tingimento')
            
            tamanhos_e_artigos[tamanho] = artigo

        novo_lote = LoteTingimento.objects.create(cor_final_alvo=cor_final_alvo)
        for item in itens_selecionados:
            ItemTingimento.objects.create(
                lote=novo_lote,
                item_demanda=item
            )

        messages.success(request, f"Lote de tingimento para a cor '{cor_final_alvo}' criado. Inicie o primeiro apontamento.")
        return redirect('producao:apontamento_tingimento', lote_id=novo_lote.id)

class ApontamentoTingimentoView(View):
    template_name = 'producao/apontamento_tingimento.html'

    def get(self, request, *args, **kwargs):
        context = self._get_common_context(request, **kwargs)
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        lote = get_object_or_404(LoteTingimento, pk=kwargs.get('lote_id'))
        action = request.POST.get('action', '')

        if not action:
            messages.error(request, "Ação inválida.")
            return redirect('producao:apontamento_tingimento', lote_id=lote.pk)
        
        if action == 'iniciar_lancamento':
            return self._handle_iniciar_lancamento(request, lote)
        if action == 'finalizar_lote':
            return self._handle_finalizar_lote(request, lote)
        if action == 'cancelar_lote':
            return self._handle_cancelar_lote(request, lote)
        
        if action == 'salvar_destinos':
            return self._handle_salvar_destinos(request, lote)

        try:
            action_name, lancamento_id_str = action.rsplit('_', 1)
            lancamento_id = int(lancamento_id_str)
        except (IndexError, ValueError):
            messages.error(request, "Ação ou ID de lançamento inválido.")
            return redirect('producao:apontamento_tingimento', lote_id=lote.pk)

        if action_name == 'salvar_lancamento':
            return self._handle_salvar_ou_finalizar_lancamento(request, lote, lancamento_id, finalizar=False)
        if action_name == 'finalizar_lancamento':
            return self._handle_salvar_ou_finalizar_lancamento(request, lote, lancamento_id, finalizar=True)
        if action_name == 'cancelar_lancamento':
            return self._handle_cancelar_lancamento(request, lote, lancamento_id)

        messages.error(request, "Ação desconhecida.")
        return redirect('producao:apontamento_tingimento', lote_id=lote.pk)

    def _get_common_context(self, request, **kwargs):
        lote = get_object_or_404(LoteTingimento, pk=kwargs.get('lote_id'))
        
        # --- INÍCIO DA LÓGICA CORRIGIDA ---
        
        # 1. Cria o formset com os itens do lote
        item_formset = ItemTingimentoFormSet(
            queryset=lote.itens_no_lote.all().select_related(
                'item_demanda__ordem_producao', 'item_demanda__pedido'
            ), 
            prefix='itens'
        )

        # 2. Cria um dicionário para mapear o saldo de cada OP
        op_ids = [form.instance.item_demanda.ordem_producao_id for form in item_formset]
        saldos_qs = SaldoOPSetor.objects.filter(
            ordem_producao_id__in=op_ids,
            setor__nome='TINGIMENTO'
        )
        saldos_map = {saldo.ordem_producao_id: saldo.saldo_peso for saldo in saldos_qs}

        # 3. Itera sobre o formset JÁ CRIADO e adiciona o saldo a cada instância
        for form in item_formset:
            op_id = form.instance.item_demanda.ordem_producao_id
            # O atributo 'saldo_no_setor_kg' é adicionado à instância do formulário
            form.instance.saldo_no_setor_kg = saldos_map.get(op_id, decimal.Decimal('0.0'))
            
        # --- FIM DA LÓGICA CORRIGIDA ---

        lancamentos_em_andamento = lote.lancamentos.filter(data_hora_fim__isnull=True).order_by('data_hora_inicio')
        forms_em_andamento = []
        for lancamento in lancamentos_em_andamento:
            for item_do_lote in lote.itens_no_lote.all():
                CargaLancamentoTingimento.objects.get_or_create(lancamento=lancamento, item_tingimento=item_do_lote)

            forms_em_andamento.append({
                'lancamento': lancamento,
                'form_fim': LancamentoTingimentoFimForm(prefix=f'fim_{lancamento.id}', instance=lancamento),
                'formset_cargas': CargaLancamentoFormSet(prefix=f'cargas_{lancamento.id}', queryset=lancamento.cargas.all().select_related('item_tingimento__item_demanda__ordem_producao')),
                'formset_paradas': ParadaTingimentoFormSet(prefix=f'paradas_{lancamento.id}', queryset=lancamento.paradas.all())
            })

        return {
            'lote': lote,
            'item_formset': item_formset,
            'forms_em_andamento': forms_em_andamento,
            'form_inicio': LancamentoTingimentoInicioForm(prefix='inicio'),
            'lancamentos_finalizados': lote.lancamentos.filter(data_hora_fim__isnull=False).order_by('-data_hora_fim'),
            'parada_formset_template': ParadaTingimentoFormSet(prefix='paradas_template'),
            'setor_nome': 'Apontamento - Tingimento'
        }

    def _handle_iniciar_lancamento(self, request, lote):
        form = LancamentoTingimentoInicioForm(request.POST, prefix='inicio')
        if form.is_valid():
            lancamento = form.save(commit=False)
            lancamento.lote = lote
            lancamento.data_hora_inicio = timezone.now()
            lancamento.save()
            messages.success(request, f"Novo lançamento para o lote #{lote.id} iniciado.")
        else:
            messages.error(request, f"Erro ao iniciar lançamento: {form.errors.as_text()}")
        return redirect('producao:apontamento_tingimento', lote_id=lote.pk)

    def _handle_salvar_destinos(self, request, lote):
        item_formset = ItemTingimentoFormSet(request.POST, prefix='itens', queryset=lote.itens_no_lote.all())
        if item_formset.is_valid():
            item_formset.save()
            messages.success(request, "Destinos dos itens salvos com sucesso.")
        else:
            messages.error(request, f"Erro ao salvar destinos: {item_formset.errors}")
        return redirect('producao:apontamento_tingimento', lote_id=lote.pk)

    def _handle_salvar_ou_finalizar_lancamento(self, request, lote, lancamento_id, finalizar=False):
        lancamento = get_object_or_404(LancamentoTingimento, pk=lancamento_id, lote=lote)
        form = LancamentoTingimentoFimForm(request.POST, prefix=f'fim_{lancamento.id}', instance=lancamento)
        cargas_formset = CargaLancamentoFormSet(request.POST, prefix=f'cargas_{lancamento.id}', queryset=lancamento.cargas.all())
        paradas_formset = ParadaTingimentoFormSet(request.POST, prefix=f'paradas_{lancamento.id}', queryset=lancamento.paradas.all())
        item_formset = ItemTingimentoFormSet(request.POST, prefix='itens', queryset=lote.itens_no_lote.all())

        if form.is_valid() and cargas_formset.is_valid() and paradas_formset.is_valid() and item_formset.is_valid():
            item_formset.save()
            lancamento_salvo = form.save(commit=False)
            if finalizar:
                lancamento_salvo.data_hora_fim = timezone.now()
            lancamento_salvo.save()
            cargas_formset.save()
            paradas = paradas_formset.save(commit=False)
            for parada in paradas:
                parada.lancamento_tingimento = lancamento_salvo
                parada.save()
            for obj in paradas_formset.deleted_objects:
                obj.delete()
            
            if finalizar:
                messages.success(request, f"Lançamento #{lancamento.id} finalizado e destinos dos itens atualizados.")
            else:
                messages.success(request, f"Progresso do Lançamento #{lancamento.id} e destinos dos itens salvos.")
        else:
            error_messages = f"Form Lançamento: {form.errors.as_text()} | Form Cargas: {cargas_formset.errors} | Form Paradas: {paradas_formset.errors} | Form Itens: {item_formset.errors}"
            messages.error(request, f"Erro ao salvar. Verifique os dados. Detalhes: {error_messages}")
        return redirect('producao:apontamento_tingimento', lote_id=lote.pk)

    def _handle_cancelar_lancamento(self, request, lote, lancamento_id):
        lancamento = get_object_or_404(LancamentoTingimento, pk=lancamento_id, lote=lote)
        if lancamento.data_hora_fim is not None:
            messages.error(request, "Não é possível cancelar um lançamento já finalizado.")
        else:
            lancamento.delete()
            messages.warning(request, f"Lançamento #{lancamento.id} cancelado.")
        return redirect('producao:apontamento_tingimento', lote_id=lote.pk)

    def _handle_cancelar_lote(self, request, lote):
        if lote.lancamentos.exists():
            messages.error(request, "Não é possível cancelar um lote que já possui lançamentos. Cancele os lançamentos primeiro.")
            return redirect('producao:apontamento_tingimento', lote_id=lote.pk)
        lote.delete()
        messages.warning(request, f"Lote de tingimento #{lote.id} foi cancelado.")
        return redirect('producao:lista_ops_tingimento')


    def _handle_finalizar_lote(self, request, lote):
        if lote.lancamentos.filter(data_hora_fim__isnull=True).exists():
            messages.error(request, "Não é possível finalizar o lote. Existem lançamentos em andamento.")
            return redirect('producao:apontamento_tingimento', lote_id=lote.pk)

        responsavel_final = lote.lancamentos.order_by('-data_hora_fim').first().responsavel if lote.lancamentos.exists() else None

        for item_tingido in lote.itens_no_lote.all():
            peso_total = item_tingido.peso_total_processado
            setor_destino = item_tingido.proximo_setor

            if not setor_destino:
                messages.error(request, f"Não é possível finalizar o lote. O item {item_tingido.item_demanda} não tem um setor de destino definido.")
                return redirect('producao:apontamento_tingimento', lote_id=lote.pk)

            if peso_total > 0:
                self._realizar_transferencia_final(item_tingido, peso_total, setor_destino, responsavel_final)
        
        lote.status = LoteTingimento.Status.FINALIZADO
        lote.observacao_final = request.POST.get('observacao_final', '')
        lote.save()
        messages.success(request, f"Lote de tingimento #{lote.id} finalizado e saldos transferidos.")
        return redirect('producao:lista_ops_tingimento')

    def _realizar_transferencia_final(self, item_tingido, peso_total_processado, setor_destino, responsavel):
        setor_origem_nome = 'TINGIMENTO'
        
        try:
            saldo_origem_obj = SaldoOPSetor.objects.get(
                ordem_producao=item_tingido.item_demanda.ordem_producao,
                setor__nome=setor_origem_nome
            )
        except SaldoOPSetor.DoesNotExist:
            return

        peso_a_transferir = min(saldo_origem_obj.saldo_peso, peso_total_processado)
        
        if peso_a_transferir > 0:
            saldo_origem_obj.saldo_peso = F('saldo_peso') - peso_a_transferir
            saldo_origem_obj.save()
            
            TransferenciaEntreSetores.objects.create(
                ordem_producao=item_tingido.item_demanda.ordem_producao,
                setor_origem=saldo_origem_obj.setor,
                setor_destino=setor_destino,
                peso_transferido=peso_a_transferir,
                responsavel=responsavel
            )
            
            saldo_destino, _ = SaldoOPSetor.objects.get_or_create(
                ordem_producao=item_tingido.item_demanda.ordem_producao,
                setor=setor_destino,
                defaults={'saldo_peso': 0}
            )
            saldo_destino.saldo_peso = F('saldo_peso') + peso_a_transferir
            saldo_destino.save()



# -- Detalhes da Ordem Producao
class OrdemProducaoDetailView(DetailView):
    """
    Exibe uma tela com todos os detalhes de uma Ordem de Produção específica.
    Refatorada para usar os novos modelos Cliente e Representante.
    """
    model = OrdemProducao
    template_name = 'producao/detalhes_op.html'
    context_object_name = 'op'
    pk_url_kwarg = 'op_id'

    def get_object(self, queryset=None):
        # Otimiza a busca inicial da OP, já carregando os dados do cliente e representante
        # para os pedidos associados.
        return OrdemProducao.objects.prefetch_related(
            'demandas__pedido__cliente__representante'
        ).get(pk=self.kwargs.get(self.pk_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        op = self.get_object()

        # Adiciona dados relacionados para uma visão completa
        # A otimização principal já foi feita no get_object com prefetch_related
        context['demandas'] = op.demandas.all().order_by('pedido__numero_pedido')
        context['saldos'] = op.saldos_por_setor.select_related('setor').order_by('setor__nome')
        context['transferencias'] = op.transferencias.select_related('setor_origem', 'setor_destino', 'responsavel').order_by('-data_transferencia')
        
        # Apontamentos de cada setor (versões completas para o histórico)
        context['apontamentos_pastilha'] = op.controlepastilha_apontamentos.select_related('responsavel').order_by('-data_hora_fim')
        context['apontamentos_torno_laser'] = op.controleproducaotornolaser_apontamentos.select_related('responsavel', 'maquina').order_by('-data_hora_fim')
        
        apontamentos_polimento_qs = ControlePolimento.objects.filter(
            itens_demanda_agrupados__ordem_producao=op
        ).select_related('tambor', 'responsavel').order_by('-data_hora_fim').distinct()

        for apontamento in apontamentos_polimento_qs:
            peso_op_no_apontamento = ItemPolimento.objects.filter(
                apontamento=apontamento,
                item_demanda__ordem_producao=op
            ).aggregate(total_peso=Sum('peso_carregado'))['total_peso'] or 0
            apontamento.peso_desta_op = peso_op_no_apontamento
            
        context['apontamentos_polimento'] = apontamentos_polimento_qs
        
        context['apontamentos_tingimento'] = LancamentoTingimento.objects.filter(
            lote__itens_no_lote__item_demanda__ordem_producao=op
        ).select_related('responsavel').order_by('-data_hora_fim').distinct()
        
        context['apontamentos_conferencia'] = ConferenciaEscolhaFinal.objects.filter(
            item_demanda__ordem_producao=op
        ).select_related('responsavel').order_by('-data_hora_fim')
        
        context['apontamentos_cq'] = ControleQualidadeEsteira.objects.filter(
            item_demanda__ordem_producao=op
        ).select_related('responsavel', 'responsavel_2', 'maquina').order_by('-data_hora_fim')

        context['apontamentos_contagem'] = op.contagemfinal_apontamentos.select_related('responsavel').order_by('-data_hora_fim')
        
        # --- LÓGICA PARA OBSERVAÇÕES ---
        # A otimização no get_object já torna este acesso eficiente
        observacoes_pedidos = set()
        for demanda in op.demandas.all():
            if demanda.pedido and demanda.pedido.observacao_detalhada:
                observacoes_pedidos.add(demanda.pedido.observacao_detalhada)
        context['observacoes_pedidos_unicas'] = list(observacoes_pedidos)

        context['demandas_com_obs'] = op.demandas.exclude(
            Q(observacao_item_pedido__exact='', observacao_item_pedido__isnull=True) &
            Q(observacao_pcp__exact='', observacao_pcp__isnull=True)
        )

        context['reprogramacoes_com_obs'] = op.reprogramacoes.exclude(
            Q(observacao__exact='') | Q(observacao__isnull=True)
        ).select_related('responsavel')

        context['apontamentos_pastilha_com_obs'] = context['apontamentos_pastilha'].exclude(Q(observacao__exact='') | Q(observacao__isnull=True))
        context['apontamentos_torno_laser_com_obs'] = context['apontamentos_torno_laser'].exclude(Q(observacao__exact='') | Q(observacao__isnull=True))
        context['apontamentos_polimento_com_obs'] = context['apontamentos_polimento'].exclude(Q(observacao__exact='') | Q(observacao__isnull=True))
        context['apontamentos_tingimento_com_obs'] = context['apontamentos_tingimento'].exclude(Q(observacao__exact='') | Q(observacao__isnull=True))
        context['apontamentos_conferencia_com_obs'] = context['apontamentos_conferencia'].exclude(Q(observacao__exact='') | Q(observacao__isnull=True))
        context['apontamentos_cq_com_obs'] = context['apontamentos_cq'].exclude(Q(observacao__exact='') | Q(observacao__isnull=True))
        context['apontamentos_contagem_com_obs'] = context['apontamentos_contagem'].exclude(Q(observacao__exact='') | Q(observacao__isnull=True))
        
        # Receita química
        receitas_calculadas = op.get_receita_calculada()
        if receitas_calculadas:
            codigos_componentes = set()
            for dados_camada in receitas_calculadas.values():
                for componente in dados_camada.get('receita', []):
                    codigos_componentes.add(componente['codigo_componente'])
            
            nomes_map = {}
            if codigos_componentes:
                produtos_erp = Pro01.objects.using('acedata').filter(procod__in=list(codigos_componentes)).values('procod', 'pronom')
                nomes_map = {p['procod'].strip(): p['pronom'].strip() for p in produtos_erp}

            for nome_camada, dados_camada in receitas_calculadas.items():
                dados_camada['nome_camada_display'] = nome_camada.replace('_', ' ').title()
                for componente in dados_camada.get('receita', []):
                    codigo = componente['codigo_componente']
                    componente['nome_componente'] = nomes_map.get(codigo, f'NOME NÃO ENCONTRADO')
        
        context['receitas_calculadas'] = receitas_calculadas

        return context



# --- NOVAS VIEWS PARA EMBALAGEM E EXPEDIÇÃO (FLUXO CENTRADO NO CLIENTE) ---

class FilaEmbalagemView(ListView):
    """
    Exibe a fila de trabalho para o setor de Embalagem, listando
    os CLIENTES que possuem itens com saldo a serem embalados.
    """
    model = Cliente
    template_name = 'producao/fila_embalagem.html'
    context_object_name = 'clientes'

    def get_queryset(self):
        # Encontra os IDs de clientes que têm pelo menos um item com saldo de embalagem
        clientes_com_saldo_ids = SaldoItemEmbalagem.objects.filter(
            saldo_grosas__gt=0
        ).values_list('item_demanda__pedido__cliente_id', flat=True).distinct()

        # Retorna a lista de objetos Cliente correspondentes
        return Cliente.objects.filter(pk__in=clientes_com_saldo_ids).order_by('nome')


class ApontamentoClienteEmbalagemView(DetailView):
    """
    Painel de controle para embalar todos os pedidos pendentes de um cliente específico.
    """
    model = Cliente
    template_name = 'producao/apontamento_cliente_embalagem.html'
    context_object_name = 'cliente'
    pk_url_kwarg = 'cliente_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()

        # Itens do cliente que ainda têm saldo para serem embalados, agrupados por pedido
        itens_pendentes_qs = ItemDemandaProducao.objects.filter(
            pedido__cliente=cliente,
            saldo_embalagem__saldo_grosas__gt=0
        ).select_related('ordem_producao', 'saldo_embalagem', 'pedido').order_by('pedido__numero_pedido', 'item_pedido_erp')
        
        pedidos_agrupados = defaultdict(list)
        for item in itens_pendentes_qs:
            pedidos_agrupados[item.pedido].append(item)

        context['pedidos_com_itens_pendentes'] = dict(pedidos_agrupados)

        # Caixas que estão abertas para este cliente
        context['caixas_abertas'] = cliente.caixas.filter(status=Caixa.Status.EM_EMBALAGEM).order_by('id')
        
        # Formulários para as ações na página
        context['form_abrir_caixa'] = AbrirCaixaForm()
        context['form_add_item'] = AdicionarItemCaixaForm()
        
        # Histórico de caixas já fechadas para este cliente
        context['caixas_fechadas'] = cliente.caixas.filter(
            status=Caixa.Status.AGUARDANDO_CONFERENCIA
        ).prefetch_related('itens_na_caixa__item_demanda__ordem_producao').order_by('-id')

        return context


class AbrirCaixaView(LoginRequiredMixin, View):
    """ Processa a criação de uma nova caixa para um cliente. """
    def post(self, request, *args, **kwargs):
        cliente = get_object_or_404(Cliente, pk=kwargs.get('cliente_id'))
        form = AbrirCaixaForm(request.POST)

        if form.is_valid():
            nova_caixa = form.save(commit=False)
            nova_caixa.cliente = cliente
            nova_caixa.save() 
            messages.success(request, f"Caixa #{nova_caixa.id} aberta para o cliente {cliente.nome}.")
        else:
            messages.error(request, f"Não foi possível abrir a caixa. Erros: {form.errors.as_text()}")
        
        return redirect('producao:apontamento_cliente_embalagem', cliente_id=cliente.id)


class AdicionarItemACaixaView(LoginRequiredMixin, View):
    """ Processa a adição de um item de demanda a uma caixa existente. """
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_demanda_id')
        caixa_id = request.POST.get('caixa_id')
        
        item = get_object_or_404(ItemDemandaProducao, pk=item_id)
        caixa = get_object_or_404(Caixa, pk=caixa_id, status=Caixa.Status.EM_EMBALAGEM)
        
        form = AdicionarItemCaixaForm(request.POST, item_demanda=item)

        if form.is_valid():
            quantidade_embalada = form.cleaned_data['quantidade_embalada']
            
            item_caixa, created = ItemCaixa.objects.get_or_create(
                caixa=caixa,
                item_demanda=item,
                defaults={'quantidade_embalada': quantidade_embalada}
            )
            if not created:
                item_caixa.quantidade_embalada = F('quantidade_embalada') + quantidade_embalada
                item_caixa.save()

            saldo_obj = item.saldo_embalagem
            saldo_obj.saldo_grosas = F('saldo_grosas') - quantidade_embalada
            saldo_obj.save()
            
            messages.success(request, f"{quantidade_embalada} GRS do item da OP {item.ordem_producao.numero_op} adicionadas à Caixa #{caixa.id}.")
        else:
            messages.error(request, f"Erro ao adicionar item: {form.errors.as_text()}")

        return redirect('producao:apontamento_cliente_embalagem', cliente_id=item.pedido.cliente.id)


class FecharCaixaView(LoginRequiredMixin, View):
    """ Muda o status de uma caixa para 'Aguardando Conferência'. """
    def post(self, request, *args, **kwargs):
        caixa = get_object_or_404(Caixa, pk=kwargs.get('caixa_id'))
        
        if not caixa.itens_na_caixa.exists():
            messages.warning(request, f"Não é possível fechar a Caixa #{caixa.id} pois ela está vazia.")
        else:
            caixa.status = Caixa.Status.AGUARDANDO_CONFERENCIA
            caixa.data_fechamento = timezone.now()
            caixa.save()
            messages.info(request, f"Caixa #{caixa.id} fechada e enviada para a Expedição.")

        return redirect('producao:apontamento_cliente_embalagem', cliente_id=caixa.cliente.id)


class FilaExpedicaoView(ListView):
    """ Exibe a fila de trabalho para o setor de Expedição, listando os CLIENTES. """
    model = Cliente
    template_name = 'producao/fila_expedicao.html'
    context_object_name = 'clientes'

    def get_queryset(self):
        # Encontra os IDs de clientes que têm caixas aguardando conferência
        clientes_com_caixas_ids = Caixa.objects.filter(
            status=Caixa.Status.AGUARDANDO_CONFERENCIA
        ).values_list('cliente_id', flat=True).distinct()

        return Cliente.objects.filter(pk__in=clientes_com_caixas_ids).order_by('nome')


class DetalheClienteExpedicaoView(DetailView):
    model = Cliente
    template_name = 'producao/detalhe_cliente_expedicao.html'
    context_object_name = 'cliente'
    pk_url_kwarg = 'cliente_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()

        # Busca as caixas que estão aguardando conferência
        caixas_qs = cliente.caixas.filter(
            status=Caixa.Status.AGUARDANDO_CONFERENCIA
        ).prefetch_related('itens_na_caixa__item_demanda__ordem_producao').order_by('id')

        # --- INÍCIO DA CORREÇÃO ---
        # Cria uma lista para armazenar cada caixa junto com seu respectivo formset de itens
        caixas_com_formsets = []
        for caixa in caixas_qs:
            # Instancia o formset para os itens da caixa atual
            item_formset = ConferenciaItemCaixaFormSet(
                queryset=caixa.itens_na_caixa.all(),
                prefix=f'caixa_{caixa.id}'  # Adiciona um prefixo único para cada formset
            )
            caixas_com_formsets.append({
                'caixa': caixa,
                'formset': item_formset
            })
        
        context['caixas_para_conferir'] = caixas_com_formsets
        # --- FIM DA CORREÇÃO ---

        # Histórico de caixas já conferidas (lógica original mantida)
        context['caixas_conferidas'] = cliente.caixas.filter(
            status=Caixa.Status.CONFERIDA
        ).prefetch_related('itens_na_caixa__item_demanda__ordem_producao').order_by('-data_conferencia')

        # Formulário para o modal de conferência (lógica original mantida)
        context['form_conferencia'] = ConferenciaCaixaForm()
        
        return context
  
class ConferenciaCaixaView(LoginRequiredMixin, View):
    """ Lida com o modal de conferência de uma caixa. """
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        caixa = get_object_or_404(Caixa, pk=kwargs.get('caixa_id'))
        form = ConferenciaCaixaForm(request.POST, instance=caixa)
        formset = ConferenciaItemCaixaFormSet(request.POST, queryset=caixa.itens_na_caixa.all())

        if form.is_valid() and formset.is_valid():
            caixa_conferida = form.save(commit=False)
            caixa_conferida.status = Caixa.Status.CONFERIDA
            caixa_conferida.data_conferencia = timezone.now()
            caixa_conferida.save()
            
            formset.save() # Salva os checkboxes

            messages.success(request, f"Conferência da Caixa #{caixa.id} salva com sucesso.")
        else:
            messages.error(request, f"Erro na conferência: {form.errors.as_text()} {formset.errors}")

        return redirect('producao:detalhe_cliente_expedicao', cliente_id=caixa.cliente.id)

class PedidoExpedicaoDetailView(DetailView):
    model = Pedido
    template_name = 'producao/detalhes_pedido_expedicao.html'
    context_object_name = 'pedido'
    pk_url_kwarg = 'pedido_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedido = self.get_object()

        apontamentos_embalagem = ApontamentoEmbalagem.objects.filter(
            item_demanda__pedido=pedido
        ).select_related(
            'item_demanda__ordem_producao',
            'responsavel'
        ).order_by('numero_caixa')

        info_caixas = defaultdict(lambda: {'itens': [], 'tam_cx': None, 'tipo_caixa': None, 'peso_caixa': 0, 'total_grosas': 0, 'conferencia': None, 'itens_conferidos': {}})
        
        for ap in apontamentos_embalagem:
            caixa = info_caixas[ap.numero_caixa]
            caixa['itens'].append(ap)
            caixa['total_grosas'] += ap.quantidade_embalada
            if not caixa['tam_cx']: caixa['tam_cx'] = ap.get_tam_cx_display()
            if not caixa['tipo_caixa']: caixa['tipo_caixa'] = ap.get_tipo_caixa_display()
            if not caixa['peso_caixa']: caixa['peso_caixa'] = ap.peso_caixa

        conferencias = ConferenciaCaixaExpedicao.objects.filter(pedido=pedido).prefetch_related('itens_conferidos')
        conferencias_map = {c.numero_caixa: c for c in conferencias}

        for num_caixa, dados_caixa in info_caixas.items():
            conferencia = conferencias_map.get(num_caixa)
            if conferencia:
                dados_caixa['conferencia'] = conferencia
                dados_caixa['itens_conferidos'] = {ic.apontamento_embalagem_id for ic in conferencia.itens_conferidos.all()}

        context['info_caixas'] = dict(sorted(info_caixas.items()))
        context['form_conferencia'] = ConferenciaCaixaForm()
        
        return context

class SalvarConferenciaCaixaView(View):
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        pedido_id = kwargs.get('pedido_id')
        numero_caixa = kwargs.get('numero_caixa')
        pedido = get_object_or_404(Pedido, pk=pedido_id)

        conferencia, created = ConferenciaCaixaExpedicao.objects.get_or_create(
            pedido=pedido,
            numero_caixa=numero_caixa
        )

        form = ConferenciaCaixaForm(request.POST, instance=conferencia)
        if not form.is_valid():
            messages.error(request, f"Erro de validação: {form.errors.as_json()}")
            return redirect('producao:detalhes_pedido_expedicao', pedido_id=pedido_id)
        
        conferencia = form.save(commit=False)
        
        if conferencia.status == 'PENDENTE':
            conferencia.status = 'EM_CONFERENCIA'
            conferencia.data_inicio_conferencia = timezone.now()

        # Salva o progresso dos checkboxes
        itens_na_caixa = ApontamentoEmbalagem.objects.filter(item_demanda__pedido=pedido, numero_caixa=numero_caixa)
        itens_checados_ids = request.POST.getlist('itens_conferidos')
        
        for ap in itens_na_caixa:
            item_conferencia, _ = ItemConferenciaCaixa.objects.get_or_create(
                conferencia_caixa=conferencia,
                apontamento_embalagem=ap
            )
            item_conferencia.conferido = str(ap.id) in itens_checados_ids
            item_conferencia.save()

        action = request.POST.get('action')
        if action == 'finalizar':
            total_itens_na_caixa = itens_na_caixa.count()
            total_itens_checados = len(itens_checados_ids)

            if total_itens_checados < total_itens_na_caixa:
                messages.error(request, "Não é possível finalizar. Todos os itens da caixa devem ser conferidos.")
            elif not conferencia.peso_conferido or conferencia.peso_conferido <= 0:
                messages.error(request, "Não é possível finalizar. O peso final da caixa deve ser informado.")
            else:
                conferencia.status = 'FINALIZADA'
                conferencia.data_finalizacao = timezone.now()
                messages.success(request, f"Conferência da Caixa #{numero_caixa} finalizada com sucesso!")
        else:
            messages.success(request, f"Progresso da conferência da Caixa #{numero_caixa} salvo.")

        conferencia.save()
        return redirect('producao:detalhes_pedido_expedicao', pedido_id=pedido_id)
    