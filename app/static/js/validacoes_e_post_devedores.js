$(document).ready(function() {
    //
    
});

// Função de validação de CNPJ
function validarCNPJ(cnpj) {
    cnpj = cnpj.replace(/[^\d]+/g, ''); // Remove tudo que não é número

    if (cnpj.length !== 14) return false;

    // Verificação de CNPJs inválidos conhecidos
    if (/^(\d)\1{13}$/.test(cnpj)) return false;

    // Valida os dígitos verificadores
    let tamanho = cnpj.length - 2;
    let numeros = cnpj.substring(0, tamanho);
    let digitos = cnpj.substring(tamanho);
    let soma = 0;
    let pos = tamanho - 7;

    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) pos = 9;
    }

    let resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(0)) return false;

    tamanho += 1;
    numeros = cnpj.substring(0, tamanho);
    soma = 0;
    pos = tamanho - 7;

    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) pos = 9;
    }

    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(1)) return false;

    return true;
}


function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, ''); // Remove tudo que não é número

    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false; // Verifica o tamanho e CPFs inválidos conhecidos

    let soma = 0;
    let resto;

    // Validação do primeiro dígito verificador
    for (let i = 1; i <= 9; i++) {
        soma += parseInt(cpf.charAt(i - 1)) * (11 - i);
    }

    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.charAt(9))) return false;

    soma = 0;

    // Validação do segundo dígito verificador
    for (let i = 1; i <= 10; i++) {
        soma += parseInt(cpf.charAt(i - 1)) * (12 - i);
    }

    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.charAt(10))) return false;

    return true; // CPF válido
}



function ativar_modal(cnpj,nome,valor){
    const elemento = document.getElementById('custom-confirm');
    document.getElementById("cnpj_mod_simples").value = cnpj;
    document.getElementById("nome_mod_simples").value = nome;
    document.getElementById("valor_mod_simples").value = valor;
    // document.getElementById("cnpj_mod_pix").value = cnpj;
    // document.getElementById("nome_mod_pix").value = nome;
    // document.getElementById("valor_mod_pix").value = valor;
    elemento.classList.remove('hidden');

}

function desativar_modal(){
    const elemento = document.getElementById('custom-confirm');
    elemento.classList.add('hidden');
}

function ativar_modal_baixa(){
    const elemento = document.getElementById('custom-confirm-baixa');
    elemento.classList.remove('hidden');
}

function desativar_modal_baixa(){
    const elemento = document.getElementById('custom-confirm-baixa');
    elemento.classList.add('hidden');
}

function ativar_modal_baixa2(dataId){
    const elemento = document.querySelector(`[data-id="${dataId}"]`);
    if (elemento) {
        elemento.classList.remove('hidden');
    }

}

function desativar_modal_baixa2(dataId){
    const elemento = document.querySelector(`[data-id="${dataId}"]`);
    if (elemento) {
        elemento.classList.add('hidden');
    }
}

$('.formModal').on('submit', function(e) {
    e.preventDefault();

    let cnpj = $(this).find('#cnpj_mod[data-id]').val();
    let nome = $(this).find('#nome_mod[data-id]').val();
    let valor = $(this).find('#valor_mod[data-id]').val();

    ativar_modal(cnpj,nome,valor)

});

$('.formModalBaixa').on('submit', function(e) {
    e.preventDefault();

    ativar_modal_baixa()

});

// Evento de envio do formulário
$('#formDevedor').on('submit', function(e) {
    e.preventDefault(); // Previne o envio do formulário por padrão

    let pessoa = $('#pessoa').val();
    let id = $('#id').val();
    let cnpj = $('#cnpj').val();
    let cpf = $('#cpf').val();
    let nome = $('#nome').val();
    let endereco = $('#endereco').val();
    let email = $('#email').val();
    let contrato = $('#contrato').val();
    let contato = $('#contatos').val();
    let tratamento = $('#tratamento').val();
    let pronome = $('#pronome').val();
    
    // Verifica se o CNPJ é válido
    
    if (!validarCNPJ(cnpj) && pessoa == 'cnpj') {
        showAlert("CNPJ inválido!","error");
        return false;
    }

    if (!validarCPF(cpf) && pessoa == 'cpf') {
        showAlert("CPF inválido!","error");
        return false;
    }



    // Se o CNPJ for válido, envia o formulário com AJAX
    $.ajax({
        url: '/inserir_devedor',
        type: 'POST',
        data: { 
            nome: nome,
            cnpj: cnpj,
            cpf: cpf,
            endereco: endereco,
            email:email,
            contrato:contrato,
            contato: contato,
            pronome: pronome,
            tratamento: tratamento,
         },
        success: function(response) {
            //showAlert(response,"success");
            window.location.href = 'http://localhost:5000/formulario_devedores';
            
        },
        error: function() {
            //showAlert("Erro na requisição...","error");
            
        }
    });
});


// Evento de envio do formulário mas para alterar o elemento
$('#formDevedorAlterar').on('submit', function(e) {
    e.preventDefault(); // Previne o envio do formulário por padrão

    let pessoa = $('#pessoa').val();
    let id = $('#id_alt').val();
    let cnpj = $('#cnpj').val();
    let cpf = $('#cpf').val();
    let nome = $('#nome').val();
    let endereco = $('#endereco').val();
    let email = $('#email').val();
    let contrato = $('#contrato').val();
    let contatos = $('#contatos').val();
    
    let tratamento = $('#tratamento').val();
    let pronome = $('#pronome').val();
    // Verifica se o CNPJ é válido
    
    if (!validarCNPJ(cnpj) && pessoa == 'cnpj') {
        showAlert("CNPJ inválido!","error");
        return false;
    }

    if (!validarCPF(cpf) && pessoa == 'cpf') {
        showAlert("CPF inválido!","error");
        return false;
    }



    // Se o CNPJ for válido, envia o formulário com AJAX
    $.ajax({
        url: '/alterar_devedor',
        type: 'POST',
        data: { 
            id: id,
            nome: nome,
            cnpj: cnpj,
            cpf: cpf,
            endereco: endereco,
            email:email,
            contrato:contrato,
            contatos: contatos,
            pronome: pronome,
            tratamento: tratamento
         },
        success: function(response) {
            window.location.href = 'http://localhost:5000/lista_devedores';
        },
        error: function() {
            
        }
    });
});




