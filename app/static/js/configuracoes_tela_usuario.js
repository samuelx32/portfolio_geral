function ativar_modal_tarefa(id){
    const elemento = document.getElementById('custom-confirm-tarefa');
    document.getElementById("id-modal-usuario").value = id;
    
    elemento.classList.remove('hidden');

}

function desativar_modal_tarefa(){
    const elemento = document.getElementById('custom-confirm-tarefa');
    elemento.classList.add('hidden');
}


$(document).ready(function() {
    $('.formModal-tarefa').on('submit', function(e) {
        e.preventDefault();

        let id = $(this).find('#id-usuario[data-id]').val();
        
        ativar_modal_tarefa(id)

    });
    
});




