from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from types import SimpleNamespace

# Importa os models do app sisven_core
from sisven_core.models import Ped01, ComLogPedRepCli, Representante, Cliente
# Importa o model de cliente do ERP Acedata para a consulta de fallback
from acedata_core.models import Ter01
from .forms import ComLogForm


class BuscarPedidoView(View):
    """
    View (CBV) acionada por JavaScript para buscar e exibir os detalhes de um pedido.
    """

    def get(self, request, *args, **kwargs):
        pedido_id = request.GET.get('pedido')
        if not pedido_id:
            return HttpResponse("", status=400)

        try:
            # --- FILTRO DE SEGURANÇA CORRIGIDO ---
            # 1. Valida se o usuário está logado e possui um last_name (que armazena o repcod).
            if not request.user.is_authenticated or not request.user.last_name:
                return HttpResponseForbidden("Acesso negado. Informações de representante inválidas.")

            # 2. Converte o last_name (repcod) para inteiro para a consulta.
            representante_codigo = int(request.user.last_name)

            # 3. Busca o pedido garantindo que o pedcod E o pedrepcod correspondam.
            # Isso impede que um representante consulte o pedido de outro.
            pedido = Ped01.objects.select_related('representante').get(
                pedcod=pedido_id,
                pedrepcod=representante_codigo
            )
            # --- FIM DO FILTRO ---

            pedido.cliente_info = None

            if pedido.cliente_id:
                try:
                    # A busca para exibição é sempre no banco de dados ACEDATA
                    cliente_erp = Ter01.objects.using('acedata').get(terdoc=pedido.cliente_id)
                    pedido.cliente_info = SimpleNamespace(
                        clicod=cliente_erp.terdoc,
                        clinom=cliente_erp.ternom
                    )
                except Ter01.DoesNotExist:
                    pedido.cliente_info = SimpleNamespace(
                        clicod=pedido.cliente_id,
                        clinom=f"Cliente cód. {pedido.cliente_id} (Não encontrado em Acedata)"
                    )

            context = {'pedido': pedido}
            return render(request, 'sisven_pedidos/partials/_pedido_details.html', context)

        except (ValueError, Ped01.DoesNotExist):
            # Captura erro se last_name não for um número ou se o pedido não for encontrado/pertencer ao usuário.
            html = "<div class='alert alert-danger mt-3'>Pedido não encontrado ou não pertence a você.</div>"
            return HttpResponse(html, status=404)


class ComLogCreateView(TemplateView):
    """
    View para a página de criação do Log de Comissão.
    """
    template_name = 'sisven_pedidos/informar_rep_subordinado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', ComLogForm())
        context['titulo'] = "Informar Comissão para Representante Subordinado"
        return context

    def post(self, request, *args, **kwargs):
        form = ComLogForm(request.POST)

        if form.is_valid():
            pedido_id = form.cleaned_data['pedido']
            subordinado = form.cleaned_data['representante_subordinado']

            try:
                pedido = Ped01.objects.get(pedcod=pedido_id)
                principal = pedido.representante

                # --- LÓGICA DE SALVAMENTO ---
                # Instancia um objeto Cliente em memória com o código do cliente do pedido.
                if not pedido.cliente_id:
                    messages.error(request, f'O pedido {pedido_id} não possui um código de cliente associado.')
                    return self.render_to_response(self.get_context_data(form=form))

                cliente_para_salvar = Cliente(clicod=pedido.cliente_id)

                # Validações de negócio
                if not subordinado:
                    messages.error(request, 'O campo "Representante Subordinado" é obrigatório.')
                    return self.render_to_response(self.get_context_data(form=form))

                if principal == subordinado:
                    messages.error(request,
                                   'O representante subordinado não pode ser o mesmo que o representante principal do pedido.')
                    return self.render_to_response(self.get_context_data(form=form))

                if ComLogPedRepCli.objects.filter(pedido=pedido).exists():
                    messages.warning(request, f'Já existe um lançamento de comissão para o pedido {pedido_id}.')
                    return self.render_to_response(self.get_context_data(form=form))

                # Cria o registro no banco de dados usando a instância em memória do cliente
                ComLogPedRepCli.objects.create(
                    pedido=pedido,
                    representante_principal=principal,
                    representante_subordinado=subordinado,
                    cliente=cliente_para_salvar,
                    data_pedido=pedido.peddat
                )

                messages.success(request,
                                 f'Comissão do pedido {pedido_id} lançada com sucesso para o representante {subordinado.nome}!')
                return redirect('sisven_pedidos:comlog_create')

            except Ped01.DoesNotExist:
                messages.error(request, 'O número do pedido informado não existe.')

        return self.render_to_response(self.get_context_data(form=form))

