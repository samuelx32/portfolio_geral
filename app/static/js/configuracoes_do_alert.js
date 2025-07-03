// Função para exibir o alerta
function showAlert(message,type) {
    const alertBox = document.getElementById("custom-alert");
    const alertMessage = document.getElementById("alert-message");

    // Define a mensagem
    alertMessage.textContent = message;

    // Aplica a cor do tipo (sucesso, erro, etc.)
    alertBox.style.backgroundColor = type === "error" ? "#f44336" : "#4caf50";

    // Exibe o alerta
    alertBox.classList.remove("hidden");
    alertBox.classList.add("visible");

    // Se a mensagem for sobre mudança nos índices monetários então a mensagem só some quando o usuário fecha ela.
    if (message != 'Mudança no Ipca' && message != 'Mudança da Selic' && message != 'Mudança nos dois indices'){
        // Oculta o alerta automaticamente após 3 segundos
        setTimeout(() => {
            closeAlert();
        }, 3000);
    }
    
    
    
}


// Função para fechar o alerta
function closeAlert() {
    const alertBox = document.getElementById("custom-alert");
    alertBox.classList.remove("visible");
    alertBox.classList.add("hidden");
}

function resetar_mensagem(){
    $.ajax({
        url: '/resetar_msg',  // URL da rota Flask
        type: 'GET',
        dataType: 'json',  // Espera-se uma resposta JSON
        success: function(response) {
          //$('#cpfMsg').text(response.mensagem);
        },
        error: function(xhr, status, error) {
            console.error('Erro na solicitação AJAX:', status, error);
            $('#cpfMsg').text('Ocorreu um erro ao resetar a mensagem.');
        }
    });
}


function abrirMenu(){
    const elemento = document.getElementById("menu-lateral");
    const elemento2 = document.getElementById("menu-lateral-encolhido");


    if (elemento.classList.contains("hidden")) {
        elemento.classList.remove("hidden");
        elemento2.classList.add("hidden");
    } else {
        elemento2.classList.remove("hidden");
        elemento.classList.add("hidden");
    }
}