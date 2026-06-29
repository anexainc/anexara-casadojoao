// Esta função garante que o script espere o jQuery do Django carregar
var rodarScriptReserva = function($) {
    $(document).ready(function() {
        console.log("Script AnexaRA carregado e jQuery pronto!");

        function carregarMesasLivres() {
            var data = $('#id_data').val();
            var tipo = $('#id_tipo_reserva').val();
            var pessoas = $('#id_numero_pessoas').val();
            var campoMesa = $('#id_mesa');

            if (data && tipo && pessoas) {
                var url = '/admin/buscar-mesas/?data=' + data + '&tipo=' + tipo + '&pessoas=' + pessoas;
                console.log("Buscando em: " + url);

                fetch(url)
                    .then(response => response.json())
                    .then(dados => {
                        // Limpa o select real
                        campoMesa.empty();
                        campoMesa.append('<option value="">---------</option>');
                        
                        if (dados.length > 0) {
                            dados.forEach(function(item) {
                                campoMesa.append('<option value="' + item.id + '">' + item.descricao + '</option>');
                            });
                            
                            // Seleciona a primeira mesa disponível
                            $('#id_mesa option:eq(1)').prop('selected', true);
                        }
                    })
                    .catch(error => console.error('Erro no Fetch:', error));
            }
        }

        // Escuta mudanças nos campos (usando delegação para garantir que funcione nas abas)
        $(document).on('change', '#id_data, #id_tipo_reserva, #id_numero_pessoas', function() {
            carregarMesasLivres();
        });
    });
};

// Inicialização segura do jQuery do Django
if (typeof django !== 'undefined' && typeof django.jQuery !== 'undefined') {
    rodarScriptReserva(django.jQuery);
} else {
    window.addEventListener('load', function() {
        if (typeof django !== 'undefined' && typeof django.jQuery !== 'undefined') {
            rodarScriptReserva(django.jQuery);
        }
    });
}