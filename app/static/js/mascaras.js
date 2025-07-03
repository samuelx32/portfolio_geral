$(document).ready(function() {
    $('#pessoa').change(function() {
        selecionar_pessoa()
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const cnpjInput = document.getElementById('cnpj');
    
    cnpjInput.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Remove tudo o que não for número
        value = value.replace(/\D/g, '');
        
        // Aplica a máscara
        if (value.length <= 2){
            value = value.replace(/^(\d{2})/, '$1');
        }else if (value.length <= 5){
                value = value.replace(/^(\d{2})(\d{0,3})/, '$1.$2');
        }else if (value.length <= 8){
                value = value.replace(/^(\d{2})(\d{0,3})(\d{0,3})/, '$1.$2.$3');
        }else if (value.length <= 12) {
            value = value.replace(/^(\d{2})(\d{0,3})(\d{0,3})(\d{0,4})/, '$1.$2.$3/$4');
        }else{
            value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{0,4})(\d{0,2})/, '$1.$2.$3/$4-$5');
        }
        
        // Atualiza o valor do campo
        e.target.value = value;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const cpfInput = document.getElementById('cpf');
    
    cpfInput.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Remove tudo o que não for número
        value = value.replace(/\D/g, '');
        
        // Aplica a máscara
        if (value.length <= 3){
            value = value.replace(/^(\d{0,3})/, '$1');
        }else if (value.length <= 6){
                value = value.replace(/^(\d{0,3})(\d{0,3})/, '$1.$2');
        }else if (value.length <= 9){
                value = value.replace(/^(\d{0,3})(\d{0,3})(\d{0,3})/, '$1.$2.$3');
        }else if (value.length <= 11) {
            value = value.replace(/^(\d{0,3})(\d{0,3})(\d{0,3})(\d{0,4})/, '$1.$2.$3-$4');
        }
        
        // Atualiza o valor do campo
        e.target.value = value;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const dataInput = document.getElementById('data_oficio');
    
    dataInput.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Remove tudo o que não for número
        value = value.replace(/\D/g, '');
        
        // Aplica a máscara
        if (value.length <= 2){
            value = value.replace(/^(\d{0,2})/, '$1');
        }else if (value.length <= 4){
                value = value.replace(/^(\d{0,2})(\d{0,2})/, '$1/$2');
        }else if (value.length <= 8){
                value = value.replace(/^(\d{0,2})(\d{0,2})(\d{0,4})/, '$1/$2/$3');
        }
        
        // Atualiza o valor do campo
        e.target.value = value;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const dataInput = document.getElementById('data_inicio');
    
    dataInput.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Remove tudo o que não for número
        value = value.replace(/\D/g, '');
        
        // Aplica a máscara
        if (value.length <= 2){
            value = value.replace(/^(\d{0,2})/, '$1');
        }else if (value.length <= 4){
                value = value.replace(/^(\d{0,2})(\d{0,2})/, '$1/$2');
        }else if (value.length <= 8){
                value = value.replace(/^(\d{0,2})(\d{0,2})(\d{0,4})/, '$1/$2/$3');
        }
        
        // Atualiza o valor do campo
        e.target.value = value;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const dataInput = document.getElementById('data_fim');
    
    dataInput.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Remove tudo o que não for número
        value = value.replace(/\D/g, '');
        
        // Aplica a máscara
        if (value.length <= 2){
            value = value.replace(/^(\d{0,2})/, '$1');
        }else if (value.length <= 4){
                value = value.replace(/^(\d{0,2})(\d{0,2})/, '$1/$2');
        }else if (value.length <= 8){
                value = value.replace(/^(\d{0,2})(\d{0,2})(\d{0,4})/, '$1/$2/$3');
        }
        
        // Atualiza o valor do campo
        e.target.value = value;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const dataInput = document.getElementById('vencimento');
    
    dataInput.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Remove tudo o que não for número
        value = value.replace(/\D/g, '');
        
        // Aplica a máscara
        if (value.length <= 2){
            value = value.replace(/^(\d{0,2})/, '$1');
        }else if (value.length <= 4){
                value = value.replace(/^(\d{0,2})(\d{0,2})/, '$1/$2');
        }else if (value.length <= 8){
                value = value.replace(/^(\d{0,2})(\d{0,2})(\d{0,4})/, '$1/$2/$3');
        }
        
        // Atualiza o valor do campo
        e.target.value = value;
    });
});

function formatarValor(valor) {
    // Remove caracteres não numéricos
    valor = valor.replace(/\D/g, '');

    // Adiciona a formatação do valor
    if (valor === '') return 'R$ 0,00';
    
    // Adiciona o separador de milhar e decimal
    valor = (parseInt(valor) / 100).toFixed(2).replace('.', ',');
    
    // Adiciona o símbolo da moeda
    return `R$ ${valor.replace(/\B(?=(\d{3})+(?!\d))/g, '.')}`;
}

// Código ajax para troca automática de cpf para cpnj, pessoa jurídica ou física
function selecionar_pessoa() {
    var pessoa = $('#pessoa').val();
    
    $.ajax({
        url: '/selecionar_pessoa',  // Assegure-se de usar a URL correta que pode ser renderizada com url_for no Flask
        type: "POST",
        data: {pessoa: pessoa},
        success: function(response) {
            // $('#cpfMsg').text(response.mensagem);
	    if (response.mensagem == "cnpj") {
                $('#div-cpf').addClass('sleep-campo');
                $('#div-cnpj').removeClass('sleep-campo'); 
                $('#cnpj').prop('required', true);
                $('#cnpj').prop('disabled', false);
                $('#cpf').prop('disabled', true);
                $('#cpf').prop('required', false);
        } else if  (response.mensagem == "cpf"){
                $('#div-cnpj').addClass('sleep-campo'); 
                $('#div-cpf').removeClass('sleep-campo');
                $('#cpf').prop('required', true);
                $('#cpf').prop('disabled', false);
                $('#cnpj').prop('disabled', true);
                $('#cnpj').prop('required', false);
        }
        },
        error: function() {
            // $('#cpfMsg').text('Erro ao validar CPF.');
	        //$('#div-cnpj').removeClass('sleep-campo');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const valorInput = document.getElementById('valor');
    const saldoInput = document.getElementById('saldo_atual');
    const valor2Inputs = document.getElementsByClassName('valor_baixa'); 
    console.log(valor2Inputs);
    
    valorInput.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Formata o valor e atualiza o campo
        e.target.value = formatarValor(value);
    });

    saldoInput.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Formata o valor e atualiza o campo
        e.target.value = formatarValor(value);
    });

    valor2Inputs.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Formata o valor e atualiza o campo
        e.target.value = formatarValor(value);
    });
    

    // Adiciona evento para cada input com a classe "valor_baixa"
    valor2Inputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            e.target.value = formatarValor(e.target.value);
        });
    });
});