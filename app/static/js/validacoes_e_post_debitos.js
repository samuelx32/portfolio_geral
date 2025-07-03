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



function validarDataOficio(data) {
    // Verifica se a data está no formato correto usando uma expressão regular
    const regexData = /^(\d{2})\/(\d{2})\/(\d{4})$/;
    const match = data.match(regexData);

    if (!match) return false; // Retorna falso se não estiver no formato dd/mm/aaaa

    const dia = parseInt(match[1], 10);
    const mes = parseInt(match[2], 10);
    const ano = parseInt(match[3], 10);

    const dataAtual = new Date();
    const anoAtual = dataAtual.getFullYear();

    // Verifica se o ano é válido (atual ou anterior)
    if (ano > anoAtual) return false;

    // Verifica se o mês está entre 1 e 12
    if (mes < 1 || mes > 12) return false;

    // Verifica se o dia é válido para o mês e ano especificados
    const ultimoDiaMes = new Date(ano, mes, 0).getDate();
    if (dia < 1 || dia > ultimoDiaMes) return false;

    if (ano < 2000) return false;

    return true; // Data é válida
}

function validarVencimento(data,vencimento){

    const regexData = /^(\d{2})\/(\d{2})\/(\d{4})$/;
    const match = vencimento.match(regexData);

    if (!match) return false; // Retorna falso se não estiver no formato dd/mm/aaaa

    const dia = parseInt(match[1], 10);
    const mes = parseInt(match[2], 10);
    const ano = parseInt(match[3], 10);

    const match2 = data.match(regexData);

    if (!match2) return false; // Retorna falso se não estiver no formato dd/mm/aaaa

    const dia2 = parseInt(match2[1], 10);
    const mes2 = parseInt(match2[2], 10);
    const ano2 = parseInt(match2[3], 10);


    // Verifica se o mês está entre 1 e 12
    if (mes < 1 || mes > 12) return false;

    // Verifica se o dia é válido para o mês e ano especificados
    const ultimoDiaMes = new Date(ano, mes, 0).getDate();
    if (dia < 1 || dia > ultimoDiaMes) return false;

    if (ano < 2000) return false;

    if (ano2 > ano && mes2 > mes) return false;
    if (ano2 == ano && mes2 > mes) return false;
    if (ano2 == ano && mes2 == mes && dia2 >= dia) return false;
    

    return true;
}

function validarNumProcesso(processo){
    let regexData = /^(\d{6})\/(\d{4})$/;
    let match = processo.match(regexData);

    if (!match) {
        regexData = /^(\d{7})\/(\d{4})$/;
        match = processo.match(regexData);

        if(!match) return false;
    };

    const ano = parseInt(match[2],10);
    const dataAtual = new Date();
    const anoAtual = dataAtual.getFullYear();

    // Verifica se o ano é válido (atual ou anterior)
    if (ano > anoAtual) return false;

    return true;
}


function verificaStatus(vencimento,status){
    let dataAtual = new Date();

    // Criar a string da data no formato "DD/MM/YYYY"
    dataAtual = `${String(dataAtual.getDate()).padStart(2, '0')}/` +
                `${String(dataAtual.getMonth() + 1).padStart(2, '0')}/` +
                `${dataAtual.getFullYear()}`;

      
    dataAtual = new Date(dataAtual);
    let data2 = new Date(vencimento);
    if (data2 < dataAtual) return 'vencido'

    return status
}

// Evento de envio do formulário
$('#formDebito').on('submit', function(e) {
    e.preventDefault(); // Previne o envio do formulário por padrão

    let num_oficio = $('#num_oficio').val();
    let data_oficio = $('#data_oficio').val();
    let vencimento = $('#vencimento').val();
    let processo = $('#processo').val();
    let valor = $('#valor').val();
    let id_devedor = $('#id_devedor').val();
    let status = $('#status').val();
    let saldo_atual = $('#saldo_atual').val();
    // Verifica se o CNPJ é válido
    
    

    if (!validarDataOficio(data_oficio)){
        showAlert("Data do Ofício Inválida","error");
        return false;
    }
    
    if (!validarVencimento(data_oficio,vencimento)){
        showAlert("Data do Vencimento Inválida","error");
        return false;
    }

    if(!validarNumProcesso(processo)){
        showAlert("Número do processo inválido.","error");
        return false;
    }

    status = verificaStatus(vencimento,status)

    // Se o CNPJ for válido, envia o formulário com AJAX
    $.ajax({
        url: '/inserir_debito',
        type: 'POST',
        data: { 
            num_oficio: num_oficio,
            data_oficio: data_oficio,
            vencimento: vencimento,
            processo: processo,
            valor: valor,
            id_devedor: id_devedor,
            status: status,
            saldo_atual: saldo_atual,
         },
        success: function(response) {
            window.location.href = 'http://localhost:5000/formulario_debitos';
        },
        error: function() {
            
            showAlert("Erro na requisição...","error");
        }
    });
});



// Evento de envio do formulário de alteração
$('#formAlterarDebito').on('submit', function(e) {
    e.preventDefault(); // Previne o envio do formulário por padrão
    let id = $('#id_alt').val();
    let num_oficio = $('#num_oficio').val();
    let data_oficio = $('#data_oficio').val();
    let vencimento = $('#vencimento').val();
    let processo = $('#processo').val();
    let valor = $('#valor').val();
    let id_devedor = $('#id_devedor').val();
    let status = $('#status').val();
    let saldo_atual = $('#saldo_atual').val();
    // Verifica se o CNPJ é válido
    
    

    if (!validarDataOficio(data_oficio)){
        showAlert("Data do Ofício Inválida","error");
        return false;
    }
    
    if (!validarVencimento(data_oficio,vencimento)){
        showAlert("Data do Vencimento Inválida","error");
        return false;
    }

    if(!validarNumProcesso(processo)){
        showAlert("Número do processo inválido.","error");
        return false;
    }

    status = verificaStatus(vencimento,status)

    // Se o CNPJ for válido, envia o formulário com AJAX
    $.ajax({
        url: '/alterar_debito',
        type: 'POST',
        data: { 
            id: id,
            num_oficio: num_oficio,
            data_oficio: data_oficio,
            vencimento: vencimento,
            processo: processo,
            valor: valor,
            id_devedor: id_devedor,
            status: status,
            saldo_atual: saldo_atual,
         },
        success: function(response) {
            window.location.href = 'http://localhost:5000/lista_debitos';
        },
        error: function() {
            
            showAlert("Erro na requisição...","error");
        }
    });
});