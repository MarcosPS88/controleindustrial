// /static/js/ficha_tecnica_cadastro.js

// Executa o código somente quando o DOM (Document Object Model) estiver completamente carregado.
// Isso garante que todos os elementos HTML estejam disponíveis para manipulação antes que o script tente acessá-los.
$(document).ready(function() {
    // Comentário: As URLs para as chamadas AJAX (para buscar artigos e ferramentas)
    // e os dados iniciais das fotos do artigo (se estiver editando uma ficha existente)
    // são esperados como variáveis globais definidas no template HTML antes de carregar este script.
    // O template deve ter um bloco <script> que define window.ajaxUrls e window.initialArtigoFotosJson.
    // Exemplo no template (dentro do {% block extra_js %} ou similar):
    // <script>
    // window.ajaxUrls = {
    //     searchArtigos: "{% url 'ajax_search_artigos' %}", searchFerramentas: "{% url 'ajax_search_ferramentas' %}",
    //     getFuracaoPadrao: "{% url 'ajax_get_furacao_padrao' %}", calculaVelocidade: "{% url 'ajax_calcula_velocidade' %}" };
    // window.initialArtigoFotosJson = '{{ initial_artigo_fotos_json|escapejs }}';
    // </script>
    // <script src="{% static 'global/js/ficha_tecnica_cadastro.js' %}"></script>


    // --- Variáveis para a Pesquisa de Artigo ---
    // Obtém a referência ao elemento HTML do modal de pesquisa de artigo pelo seu ID.
    const modalPesquisaArtigoElement = document.getElementById('modalPesquisaArtigo');
    // Cria uma instância do modal Bootstrap. Isso permite usar métodos como .show() e .hide().
    // Verifica se o elemento foi encontrado antes de criar a instância.
    const modalPesquisaArtigo = modalPesquisaArtigoElement ? new bootstrap.Modal(modalPesquisaArtigoElement) : null;
    // Obtém referências aos elementos de input e resultados dentro do modal de artigo usando jQuery.
    const inputPesquisaArtigoModal = $('#inputPesquisaArtigoModal');
    const resultadosPesquisaArtigoModal = $('#resultadosPesquisaArtigoModal');
    // Obtém referências aos campos no formulário principal que exibirão/armazenarão o artigo selecionado.
    const artigoDisplayInput = $('#id_artigo_display');
    const artigoOriginalSelect = $('#id_artigo');
    // Campos relacionados ao artigo e tamanho
    const $idTamanho = $('#id_tamanho'); // Este é o select de Tamanho do formulário principal
    const $idVelocidadeOp1Display = $('#id_velocidade_op1_display'); // Campo de exibição da velocidade OP1
    const $idVelocidadeOp2Display = $('#id_velocidade_op2_display'); // Campo de exibição da velocidade OP2

    // Obtém referências aos elementos onde as fotos do artigo serão exibidas.
    const artigoFotosContainer = $('#artigoFotosContainer'); 
    const artigoFotosPlaceholder = $('#artigoFotosPlaceholder'); // O parágrafo inicial "Selecione um artigo...".

    // Função para exibir as fotos no container
    // Recebe uma array de objetos de foto (cada objeto deve ter url e descricao_campo_tratada).
    function displayArtigoFotos(fotosArray) {
        // Limpa qualquer conteúdo anterior no container de fotos.
        artigoFotosContainer.empty();
        // Verifica se há fotos na array recebida e se a array não está vazia.
        if (fotosArray && fotosArray.length > 0) {
            // Esconde o placeholder "Selecione um artigo..." se houver fotos para exibir.
            if(artigoFotosPlaceholder) artigoFotosPlaceholder.hide();
            // Itera sobre cada objeto de foto na array.
            fotosArray.forEach(function(foto) {
                // Cria a string HTML para exibir uma única foto.
                let fotoHtml = `
                    <div class="col-6 mb-2 text-center">
                        <a href="${foto.url}" data-bs-toggle="tooltip" data-bs-placement="top" title="Ampliar: ${foto.descricao_campo_tratada || 'Imagem'}" target="_blank" class="d-inline-block">
                            <img src="${foto.url}" class="img-thumbnail" alt="${foto.descricao_campo_tratada}" style="width: 75px; height: 75px; object-fit: contain; border-radius: 0.5rem;">
                        </a>
                        <small class="d-block text-muted" style="font-size: 0.65rem; line-height: 1.1;">${foto.descricao_campo_tratada}</small>
                    </div>`;
                // Adiciona o HTML da foto ao container.
                artigoFotosContainer.append(fotoHtml);
            });
            // Re-inicializa tooltips para os novos elementos que foram adicionados dinamicamente.
            var tooltipTriggerList = [].slice.call(artigoFotosContainer[0].querySelectorAll('[data-bs-toggle="tooltip"]'))
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl)
            });
        } else {
            if(artigoFotosPlaceholder) artigoFotosPlaceholder.hide();
             artigoFotosContainer.html('<div class="col-12"><p class="text-muted small p-2 text-center">Nenhuma imagem para este artigo ou artigo não selecionado.</p></div>');
        }
    }

    // Variável para armazenar a descrição do material do artigo selecionado
    let materialDescricaoDoArtigoSelecionado = artigoDisplayInput.data('initial-material-descricao') || '';

    // --- Carregamento Inicial das Fotos do Artigo ---
    if (window.initialArtigoFotosJson && window.initialArtigoFotosJson !== "[]" && window.initialArtigoFotosJson !== "\"[]\"") {
        try {
            const initialFotos = JSON.parse(window.initialArtigoFotosJson);
            displayArtigoFotos(initialFotos);
        } catch (e) {
            console.error("Erro ao parsear JSON das fotos iniciais:", e, window.initialArtigoFotosJson);
            displayArtigoFotos([]);
        }
    } else {
        displayArtigoFotos([]);
    }

    // --- Lógica de Pesquisa de Artigo (no Modal) ---
    let pesquisaArtigoTimeout;
    inputPesquisaArtigoModal.on('keyup', function() {
        clearTimeout(pesquisaArtigoTimeout);
        const query = $(this).val().trim();

        if (query.length === 0) {
            resultadosPesquisaArtigoModal.html('<p class="text-muted small p-2">Digite para pesquisar.</p>');
            return;
        }
        resultadosPesquisaArtigoModal.html('<div class="text-center p-3"><div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Buscando...</span></div></div>');

        pesquisaArtigoTimeout = setTimeout(function() {
            $.ajax({
                url: window.ajaxUrls.searchArtigos,
                data: { 'q': query },
                dataType: 'json',
                success: function(data) {
                    resultadosPesquisaArtigoModal.empty();
                    if (data.artigos && data.artigos.length > 0) {
                        const ul = $('<ul class="list-group list-group-flush"></ul>');
                        data.artigos.forEach(function(artigo) {
                            const fotosJsonString = JSON.stringify(artigo.fotos).replace(/'/g, "&apos;").replace(/"/g, "&quot;");
                            ul.append(
                                `<li class="list-group-item list-group-item-action list-group-item-light p-2"
                                    data-id="${artigo.id}"
                                    data-descricao="${artigo.descricao}"
                                    data-material-id="${artigo.material_id || ''}"
                                    data-material-descricao="${artigo.material_descricao || ''}"
                                    data-fotos='${fotosJsonString}'
                                    style="cursor: pointer; font-size: 0.85rem;">
                                    ${artigo.descricao}
                                 </li>`
                            );
                        });
                        resultadosPesquisaArtigoModal.append(ul);
                    } else {
                        resultadosPesquisaArtigoModal.html('<p class="text-warning small p-2">Nenhum artigo encontrado com o termo pesquisado. Verifique se o artigo está cadastrado.</p>');
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.error("Erro na busca de artigos:", textStatus, errorThrown);
                    resultadosPesquisaArtigoModal.html('<p class="text-danger small p-2">Erro ao realizar a pesquisa. Verifique o console para detalhes.</p>');
                }
            });
        }, 350);
    });

    // --- Lógica de Seleção de Artigo (no Modal) ---
    resultadosPesquisaArtigoModal.on('click', 'li', function() {
        const artigoId = $(this).data('id');
        const artigoDescricao = $(this).data('descricao');
        const materialDescricao = $(this).data('material-descricao');
        const fotosJsonString = $(this).attr('data-fotos');
        let artigoFotos = [];
        try {
            artigoFotos = JSON.parse(fotosJsonString.replace(/&apos;/g, "'").replace(/&quot;/g, '"'));
        } catch (e) {
            console.error("Erro ao parsear JSON das fotos do artigo selecionado:", e, fotosJsonString);
        }

        artigoDisplayInput.val(artigoDescricao);
        artigoOriginalSelect.val(artigoId).trigger('change');
        materialDescricaoDoArtigoSelecionado = materialDescricao;

        if(modalPesquisaArtigo) modalPesquisaArtigo.hide();
        inputPesquisaArtigoModal.val('');
        resultadosPesquisaArtigoModal.html('<p class="text-muted small p-2">Nenhum resultado para exibir. Realize uma busca.</p>');

        displayArtigoFotos(artigoFotos);
        calcula_velocidade();
    });

    // --- Lógica para Pesquisa de Ferramenta (para Etapas) ---
    const modalPesquisaFerramentaElement = document.getElementById('modalPesquisaFerramenta');
    const modalPesquisaFerramenta = modalPesquisaFerramentaElement ? new bootstrap.Modal(modalPesquisaFerramentaElement) : null;
    const inputPesquisaFerramentaModal = $('#inputPesquisaFerramentaModal');
    const resultadosPesquisaFerramentaModal = $('#resultadosPesquisaFerramentaModal');
    let currentFerramentaDisplayTarget = null;
    let currentFerramentaValueTarget = null;

    $(document).on('click', '.btn-pesquisa-ferramenta', function() {
        const displayTargetSelector = $(this).data('display-target');
        const valueTargetSelector = $(this).data('value-target');
        currentFerramentaDisplayTarget = $(displayTargetSelector);
        currentFerramentaValueTarget = $(valueTargetSelector);
        inputPesquisaFerramentaModal.val('');
        resultadosPesquisaFerramentaModal.html('<p class="text-muted small p-2">Nenhum resultado para exibir. Realize uma busca.</p>');
    });

    let pesquisaFerramentaTimeout;
    inputPesquisaFerramentaModal.on('keyup', function() {
        clearTimeout(pesquisaFerramentaTimeout);
        const query = $(this).val().trim();
        if (query.length === 0) {
            resultadosPesquisaFerramentaModal.html('<p class="text-muted small p-2">Digite para pesquisar.</p>');
            return;
        }
        resultadosPesquisaFerramentaModal.html('<div class="text-center p-3"><div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Buscando...</span></div></div>');
        pesquisaFerramentaTimeout = setTimeout(function() {
            $.ajax({
                url: window.ajaxUrls.searchFerramentas,
                data: { 'q': query },
                dataType: 'json',
                success: function(data) {
                    resultadosPesquisaFerramentaModal.empty();
                    if (data.ferramentas && data.ferramentas.length > 0) {
                        const ul = $('<ul class="list-group list-group-flush"></ul>');
                        data.ferramentas.forEach(function(ferramenta) {
                            ul.append(
                                `<li class="list-group-item list-group-item-action list-group-item-light p-2"
                                    data-id="${ferramenta.id}"
                                    data-descricao="${ferramenta.descricao}"
                                    style="cursor: pointer; font-size: 0.85rem;">
                                    ${ferramenta.descricao}
                                 </li>`
                            );
                        });
                        resultadosPesquisaFerramentaModal.append(ul);
                    } else {
                        resultadosPesquisaFerramentaModal.html('<p class="text-warning small p-2">Nenhuma ferramenta encontrada.</p>');
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.error("Erro na busca de ferramentas:", textStatus, errorThrown);
                    resultadosPesquisaFerramentaModal.html('<p class="text-danger small p-2">Erro ao realizar a pesquisa.</p>');
                }
            });
        }, 350);
    });

    resultadosPesquisaFerramentaModal.on('click', 'li', function() {
        if (!currentFerramentaDisplayTarget || !currentFerramentaValueTarget) {
            console.warn("Alvo da ferramenta não definido. Clique no botão de pesquisa ao lado do campo da ferramenta.");
            return;
        }
        const ferramentaId = $(this).data('id');
        const ferramentaDescricao = $(this).data('descricao');
        currentFerramentaDisplayTarget.val(ferramentaDescricao);
        currentFerramentaValueTarget.val(ferramentaId).trigger('change');
        if(modalPesquisaFerramenta) modalPesquisaFerramenta.hide();
    });

    // --- Melhoria de Usabilidade: Adicionar Placeholders ---
    $('input[type="text"].form-control').each(function() {
        if (!$(this).attr('placeholder')) {
            const label = $(`label[for="${$(this).attr('id')}"]`).text().replace(':', '').trim();
            if (label) {
                $(this).attr('placeholder', label);
            }
        }
    });

    // --- Inicialização de Tooltips ---
    var tooltipTriggerListGlobal = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerListGlobal.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // --- Lógica para Operação 2 ---
    const $selectQuantidadeOp = $('#id_quantidade_op'); // ID do campo quantidade_op do form principal
    const $fieldsetOperacao2 = $('#operacao2_fieldset'); // ID do fieldset/div que engloba a OP2

    function habilita_2_op(selectElement) {
        if (!selectElement || !$fieldsetOperacao2.length) return;

        if ($(selectElement).val() == '1') { // Se for apenas 1 operação
            $fieldsetOperacao2.hide();
            // Limpar campos do formset da operação 2 (índices 5 a 9)
            for (let i = 5; i <= 9; i++) {
                $(`#id_etapas-${i}-tipo_torneamento`).val('').trigger('change');
                $(`#id_etapas-${i}-ferramenta`).val('').trigger('change'); // Campo oculto da ferramenta
                $(`#id_etapas-${i}-ferramenta_display`).val(''); // Campo de display da ferramenta
                $(`#id_etapas-${i}-espessura`).val('');
                $(`#id_etapas-${i}-observacao`).val('');
                if ($(`#id_etapas-${i}-DELETE`).length) { // Se o campo DELETE existir
                    $(`#id_etapas-${i}-DELETE`).prop('checked', false);
                }
            }
            $idVelocidadeOp2Display.val(''); // Limpa o campo de velocidade da OP2
        } else {
            $fieldsetOperacao2.show();
        }
        calcula_velocidade(); // Recalcula velocidade após mostrar/esconder OP2
    }

    if ($selectQuantidadeOp.length) {
        habilita_2_op($selectQuantidadeOp[0]); // Chamada inicial
        $selectQuantidadeOp.on('change', function() {
            habilita_2_op(this);
        });
    }

    // --- Lógica para Furação ---
    const $divFuraCamposGeral = $('#div_fura_campos_geral');
    const $divFuraBroca1F = $('#div_fura_broca_1f');
    const $divsFura2F4F = $('#div_fura_broca_2f, #div_fura_broca_4f, #div_fura_abertura_2f, #div_fura_abertura_4f');
    // const $divFuraAlturaControl = $('#div_fura_altura_control'); // Não usado diretamente, mas pode ser útil para layout
    const $inputsFuracao = $('#id_broca_1f, #id_broca_2f, #id_broca_4f, #id_abertura_2f, #id_abertura_4f');

    function getTipoTorneamentoMandril5Selector(opNum) {
        const formsetIndex = (opNum === 1) ? 4 : 9;
        return `#id_etapas-${formsetIndex}-tipo_torneamento`;
    }
    function getObservacaoMandril5Selector(opNum) {
        const formsetIndex = (opNum === 1) ? 4 : 9;
        return `#id_etapas-${formsetIndex}-observacao`;
    }

    function limparCamposTipoObservacaoMandril5(opNumLimpar) {
        const tipoSelector = getTipoTorneamentoMandril5Selector(opNumLimpar);
        const obsSelector = getObservacaoMandril5Selector(opNumLimpar);
        $(tipoSelector).val('').trigger('change');
        $(obsSelector).val('');
    }

    function verifica_furacao(tipoMandril5Id, opNumOrigem) {
        if (!$idTamanho.val() && tipoMandril5Id) {
            alert("Por favor, selecione o Tamanho do artigo antes de definir a furação.");
            limparCamposTipoObservacaoMandril5(opNumOrigem);
            $divFuraCamposGeral.hide();
            return;
        }
        // $inputsFuracao.val(''); // MOVIMENTADO: Limpeza será condicional

        if (opNumOrigem === 1 && tipoMandril5Id) {
            limparCamposTipoObservacaoMandril5(2);
        } else if (opNumOrigem === 2 && tipoMandril5Id) {
            limparCamposTipoObservacaoMandril5(1);
            
        }

        if (!tipoMandril5Id) {
            $divFuraCamposGeral.hide();
            return;
        }

        const tipoIdStr = String(tipoMandril5Id);
        const furos_1_ids = ['31', '24', '20', '35']; // IDs dos tipos para 1 furo (ajuste conforme seus IDs)

        if (tipoIdStr === '23') { // '23' é o ID para furação padrão
            $inputsFuracao.val(''); // Limpa os campos ANTES de buscar o padrão
            $divFuraBroca1F.hide();
            $('#div_fura_2f_4f_container').show();
            if ($idTamanho.val()) {
                $.ajax({
                    url: window.ajaxUrls.getFuracaoPadrao,
                    data: { 'tamanho_id': $idTamanho.val() },
                    dataType: 'json',
                    success: function(data) {
                        if (data.sucesso) {
                            $('#id_broca_2f').val(data.broca_2f || '');
                            $('#id_broca_4f').val(data.broca_4f || '');
                            $('#id_abertura_2f').val(data.abertura_2f || '');
                            $('#id_abertura_4f').val(data.abertura_4f || '');
                        } else {
                            console.warn("Furação padrão não encontrada para o tamanho:", $idTamanho.val(), data.mensagem);
                        }
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.error("Erro ao buscar furação padrão:", textStatus, errorThrown);
                    }
                });
            }
        } else if (furos_1_ids.includes(tipoIdStr)) {
            $divFuraBroca1F.show();
            $('#div_fura_2f_4f_container').hide(); // Esconde o container dos campos 2F e 4F
            // Não limpa os inputs aqui, preserva valores existentes.
        } else {
            // Outros tipos de furação (não padrão '23', não 1 furo) ou furação manual
            // Não limpa os inputs aqui, preserva valores existentes.
            $divFuraBroca1F.hide();
            $('#div_fura_2f_4f_container').show(); // Mostra o container dos campos 2F e 4F
        }
        $divFuraCamposGeral.show();
    }
    $divFuraCamposGeral.hide();

    // --- Lógica para Cálculo de Velocidade ---
    function calcula_velocidade() {
        if (!$idTamanho.val() || !artigoOriginalSelect.val()) {
            $idVelocidadeOp1Display.val('');
            $idVelocidadeOp2Display.val('');
            return;
        }

        let dataPayload = {
            tamanho_id: $idTamanho.val(),
            material_ficha: materialDescricaoDoArtigoSelecionado,
            enviar_para1_ficha: $('#id_enviar_para1').val() || '',
            enviar_para2_ficha: $('#id_enviar_para2').val() || ''
        };

        for (let op = 1; op <= 2; op++) {
            for (let mandril = 1; mandril <= 5; mandril++) {
                const formsetIndex = (op === 1) ? mandril - 1 : (mandril - 1) + 5;
                const tipoId = $(`#id_etapas-${formsetIndex}-tipo_torneamento`).val();
                dataPayload[`tipo_op${op}_${mandril}`] = tipoId || '';
            }
        }

        $.ajax({
            url: window.ajaxUrls.calculaVelocidade,
            data: dataPayload,
            dataType: 'json',
            success: function(data) {
                if (data.sucesso) {
                    $idVelocidadeOp1Display.val(data.vel_op1 || '');
                    $idVelocidadeOp2Display.val(data.vel_op2 || '');
                } else {
                    console.warn("Erro ao calcular velocidade:", data.mensagem);
                    $idVelocidadeOp1Display.val('');
                    $idVelocidadeOp2Display.val('');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("Erro na chamada AJAX para calcular velocidade:", textStatus, errorThrown);
                $idVelocidadeOp1Display.val('');
                $idVelocidadeOp2Display.val('');
            }
        });
    }

    // --- Event Listeners ---
    $(document).on('change', `${getTipoTorneamentoMandril5Selector(1)}, ${getTipoTorneamentoMandril5Selector(2)}`, function() {
        const fieldId = $(this).attr('id');
        const opNumOrigem = fieldId.includes('etapas-4') ? 1 : (fieldId.includes('etapas-9') ? 2 : null);
        if (opNumOrigem) {
            const tipoMandril5Id = $(this).val();
            verifica_furacao(tipoMandril5Id, opNumOrigem);
        }
        calcula_velocidade();
    });

    $(document).on('change', 'select[id^="id_etapas-"][id$="-tipo_torneamento"]', function() {
        // Evita chamar verifica_furacao duas vezes se for um dos mandris 5
        const fieldId = $(this).attr('id');
        if (!fieldId.includes('etapas-4-tipo_torneamento') && !fieldId.includes('etapas-9-tipo_torneamento')) {
            // Se não for mandril 5, apenas calcula velocidade
        }
        calcula_velocidade();
    });

    $('#id_enviar_para1, #id_enviar_para2, #id_enviar_para3').on('change', function() {
        calcula_velocidade();
    });
    
    $idTamanho.on('change', function() {
        calcula_velocidade();

        const tipoOp1_Mandril5_val = $(getTipoTorneamentoMandril5Selector(1)).val();
        const tipoOp2_Mandril5_val = $(getTipoTorneamentoMandril5Selector(2)).val();

        // Reavalia a furação para OP1 Mandril 5, se um tipo estiver selecionado.
        // A função verifica_furacao (modificada) decidirá se limpa (para ID '23') ou preserva.
        if (tipoOp1_Mandril5_val) {
            verifica_furacao(tipoOp1_Mandril5_val, 1);
        }

        // Reavalia a furação para OP2 Mandril 5, se um tipo estiver selecionado.
        if (tipoOp2_Mandril5_val) {
            verifica_furacao(tipoOp2_Mandril5_val, 2);
        }

        // Se nenhum tipo de furação estiver selecionado em nenhum dos mandris 5,
        // e a seção de furação estava visível, ela deve ser escondida.
        if (!tipoOp1_Mandril5_val && !tipoOp2_Mandril5_val) {
            $divFuraCamposGeral.hide();
        }
        // A limpeza explícita foi removida. A função verifica_furacao lida com a limpeza
        // apenas quando o tipo de furação é '23' (padrão).
    });

    artigoOriginalSelect.on('change', calcula_velocidade);

    if ($idTamanho.val() && artigoOriginalSelect.val()) {
        calcula_velocidade();
    }

    const tipoOp1_Mandril5_inicial = $(getTipoTorneamentoMandril5Selector(1)).val();
    if (tipoOp1_Mandril5_inicial) {
        verifica_furacao(tipoOp1_Mandril5_inicial, 1);
    }
    const tipoOp2_Mandril5_inicial = $(getTipoTorneamentoMandril5Selector(2)).val();
    if (tipoOp2_Mandril5_inicial) {
        verifica_furacao(tipoOp2_Mandril5_inicial, 2);
    }

    // --- Constantes para a lógica de habilitação de campos por tipo de torneamento ---
    const TIPOS_V_V_V_V = ['1', '3', '7', '15'];
    const TIPOS_V_F_F_V = ['2', '6', '8', '9', '11', '12', '13', '17', '18', '19', '20', '21', '22', '23', '24', '25', '31', '32', '33', '34', '35'];
    const TIPOS_V_V_F_V = ['4', '5', '10', '14', '16', '30', '36']; // IDs 31, 32 removidos pois estavam duplicados em V_F_F_V

    // --- Função para gerenciar habilitação/limpeza de campos da etapa baseado no Tipo de Torneamento ---
    function gerenciarCamposEtapaPorTipo(tipoIdSelecionado, formPrefix) {
        // Não aplicar esta lógica para os mandris de furação (mandril 5 de cada OP)
        // Mandril 5 OP1 = etapas-4, Mandril 5 OP2 = etapas-9
        if (formPrefix === 'etapas-4' || formPrefix === 'etapas-9') {
            return;
        }

        const $ferramentaDisplayInput = $(`#id_${formPrefix}-ferramenta_display`);
        const $ferramentaHiddenSelect = $(`#id_${formPrefix}-ferramenta`);
        const $espessuraInput = $(`#id_${formPrefix}-espessura`);
        const $observacaoInput = $(`#id_${formPrefix}-observacao`);
        const $btnPesquisaFerramenta = $(`.btn-pesquisa-ferramenta[data-form-prefix="${formPrefix}"]`);

        // Default: Desabilitar e limpar campos antes de aplicar regras específicas do tipo
        // Isso garante que, ao mudar de um tipo para outro, os campos sejam resetados corretamente.
        if ($espessuraInput.length) $espessuraInput.prop('disabled', true).val('');
        if ($observacaoInput.length) $observacaoInput.prop('disabled', true).val(''); // Observação também começa desabilitada e é habilitada conforme a regra
        if ($btnPesquisaFerramenta.length) $btnPesquisaFerramenta.prop('disabled', true);
        if ($ferramentaHiddenSelect.length) $ferramentaHiddenSelect.val('');
        if ($ferramentaDisplayInput.length) $ferramentaDisplayInput.val('');


        const tipoIdStr = String(tipoIdSelecionado);

        if (TIPOS_V_V_V_V.includes(tipoIdStr)) {
            // console.log(`FormPrefix: ${formPrefix}, Tipo: ${tipoIdStr} - Entrou em V_V_V_V`);
            if ($espessuraInput.length) $espessuraInput.prop('disabled', false);
            if ($observacaoInput.length) $observacaoInput.prop('disabled', false);
            if ($btnPesquisaFerramenta.length) $btnPesquisaFerramenta.prop('disabled', false);
        } else if (TIPOS_V_F_F_V.includes(tipoIdStr)) {
            // console.log(`FormPrefix: ${formPrefix}, Tipo: ${tipoIdStr} - Entrou em V_F_F_V`);
            // Ferramenta é considerada "desabilitada" (valor limpo), mas o botão de pesquisa fica habilitado (conforme lógica original)
            if ($ferramentaHiddenSelect.length) $ferramentaHiddenSelect.val('');
            if ($ferramentaDisplayInput.length) $ferramentaDisplayInput.val('');
            // Espessura desabilitada e limpa
            if ($espessuraInput.length) $espessuraInput.prop('disabled', true).val('');
            // Observação habilitada
            if ($observacaoInput.length) $observacaoInput.prop('disabled', false);
            // Botão de pesquisa de ferramenta DESABILITADO para esta condição
            if ($btnPesquisaFerramenta.length) $btnPesquisaFerramenta.prop('disabled', true);
        } else if (TIPOS_V_V_F_V.includes(tipoIdStr)) {
            // console.log(`FormPrefix: ${formPrefix}, Tipo: ${tipoIdStr} - Entrou em V_V_F_V`);
            // Espessura desabilitada e limpa
            if ($espessuraInput.length) $espessuraInput.prop('disabled', true).val('');
            // Observação habilitada
            if ($observacaoInput.length) $observacaoInput.prop('disabled', false);
            // Botão de pesquisa de ferramenta habilitado (não era explicitamente desabilitado na lógica original para este caso)
            if ($btnPesquisaFerramenta.length) $btnPesquisaFerramenta.prop('disabled', false);
        }
        // Se o tipoIdSelecionado não se encaixar em nenhuma categoria, os campos permanecerão desabilitados e limpos (devido ao reset no início da função).
    }

    // --- Lógica para limpar campos da etapa quando Tipo Torneamento é esvaziado ---
    // E para gerenciar campos quando um tipo é selecionado
    $(document).on('change', 'select[id^="id_etapas-"][id$="-tipo_torneamento"]', function() {
        const tipoIdSelecionado = $(this).val();
        const idCompleto = $(this).attr('id');
        const idParts = idCompleto.split('-');
        const formPrefix = idParts[0].substring(3) + '-' + idParts[1]; // ex: "etapas-0"

        if (tipoIdSelecionado === '') {
            // Extrai o prefixo do formset do ID do campo, ex: "etapas-0"
            // O ID é algo como "id_etapas-0-tipo_torneamento"
            // const idParts = $(this).attr('id').split('-'); // Já calculado acima
            // const formPrefix = idParts[0].substring(3) + '-' + idParts[1]; // Já calculado acima

            // Limpar campo Ferramenta (display e hidden)
            const $ferramentaDisplayInput = $(`#id_${formPrefix}-ferramenta_display`);
            if ($ferramentaDisplayInput.length) {
                $ferramentaDisplayInput.val('');
            }
            const $ferramentaHiddenSelect = $(`#id_${formPrefix}-ferramenta`);
            if ($ferramentaHiddenSelect.length) {
                $ferramentaHiddenSelect.val('').trigger('change'); // trigger change para outras lógicas
            }

            // Limpar campo Espessura
            const $espessuraInput = $(`#id_${formPrefix}-espessura`);
            if ($espessuraInput.length) {
                $espessuraInput.val('');
            }

            // Limpar campo Observacao
            $(`#id_${formPrefix}-observacao`).val('');
        }

        // Gerencia os campos da etapa (Ferramenta, Espessura, Observação) com base no tipo selecionado
        // Esta função só atuará se tipoIdSelecionado NÃO for vazio e não for mandril de furação.
        gerenciarCamposEtapaPorTipo(tipoIdSelecionado, formPrefix);

        // Lógica existente para furação e cálculo de velocidade
        const opNumOrigem = idCompleto.includes('etapas-4') ? 1 : (idCompleto.includes('etapas-9') ? 2 : null);
        if (opNumOrigem) { // Se for um mandril 5 (furação)
            verifica_furacao(tipoIdSelecionado, opNumOrigem);
        }
        
        // Calcula velocidade em todas as mudanças de tipo de torneamento
        calcula_velocidade();
    });
}); // Fim de $(document).ready()
