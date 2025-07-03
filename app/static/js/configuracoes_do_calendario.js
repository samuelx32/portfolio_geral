function paraISO(dataBr) {
  const [dia, mes, ano] = dataBr.split('/');
  return `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`;
}


// Armazena o id do evento visualizado temporariamente
let eventoVisualizado = null; 

document.addEventListener('DOMContentLoaded', function () {

  document.getElementById('aprovar').addEventListener('click', () => {
  const id = document.getElementById("modal-id").innerText

  fetch('/aprovar-ferias', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id: id,
        })
      })
      .then(res => {
        if (res.ok) {
          alert("Solicitação enviada!");
          // Remove visualização
          if (eventoVisualizado) {
            eventoVisualizado.remove();
            eventoVisualizado = null;
          }
          // Recarrega os eventos, se necessário
          calendar.refetchEvents();
        } else {
          alert("Erro ao solicitar.");
        }
      });
    });

document.getElementById('recusar').addEventListener('click', () => {
  const id = document.getElementById("modal-id").innerText

  fetch('/recusar-ferias', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id: id,
        })
      })
      .then(res => {
        if (res.ok) {
          alert("Solicitação enviada!");
          // Remove visualização
          if (eventoVisualizado) {
            eventoVisualizado.remove();
            eventoVisualizado = null;
          }
          // Recarrega os eventos, se necessário
          calendar.refetchEvents();
        } else {
          alert("Erro ao solicitar.");
        }
      });
    });

document.getElementById('excluir').addEventListener('click', () => {
  const id = document.getElementById("modal-id").innerText

  fetch('/excluir-ferias', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id: id,
        })
      })
      .then(res => {
        if (res.ok) {
          alert("Solicitação enviada!");
          // Remove visualização
          if (eventoVisualizado) {
            eventoVisualizado.remove();
            eventoVisualizado = null;
          }
          // Recarrega os eventos, se necessário
          calendar.refetchEvents();
        } else {
          alert("Erro ao solicitar.");
        }
      });
    });

  document.getElementById('visualizar').addEventListener('click', () => {
        const inicio = document.getElementById('data_inicio').value;
        const fim = document.getElementById('data_fim').value;
      
        if (!inicio || !fim) {
          alert("Preencha ambas as datas.");
          return;
        }
      
        const inicioIso = paraISO(inicio);
        const fimIso = new Date(new Date(paraISO(fim)).getTime() + 86400000).toISOString().split('T')[0];
      
        // Remove visualização anterior
        if (eventoVisualizado) {
          eventoVisualizado.remove();
        }
      
        // Adiciona evento temporário
        eventoVisualizado = calendar.addEvent({
          start: inicioIso,
          end: fimIso,
          display: 'background',
          extendedProps: { tipo: 'visualizacao', situacao: 'SELECIONADO' }
        });
  });

  document.getElementById('remover').addEventListener('click', () => {
        if (eventoVisualizado) {
          eventoVisualizado.remove();
          eventoVisualizado = null;
        }
  });

  document.getElementById('solicitar').addEventListener('click', () => {
      const inicio = document.getElementById('data_inicio').value;
      const fim = document.getElementById('data_fim').value;
      const categoria = document.getElementById('categoria').value;
    
      if (!inicio || !fim) {
        alert("Preencha ambas as datas.");
        return;
      }
    
      fetch('/agendamentos', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          inicio: paraISO(inicio),
          fim: paraISO(fim),
          categoria: categoria,
        })
      })
      .then(res => {
        if (res.ok) {
          alert("Solicitação enviada!");
          // Remove visualização
          if (eventoVisualizado) {
            eventoVisualizado.remove();
            eventoVisualizado = null;
          }
          // Recarrega os eventos, se necessário
          calendar.refetchEvents();
        } else {
          alert("Erro ao solicitar.");
        }
      });
    });
    


    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialDate: '2025-06-01', //Mês Inicial do Calendário
      initialView: 'dayGridMonth', //Visualização dos dias separados por mês
      locale: 'pt-br',
      events: "/agendamentos",
      eventDidMount: function(info) {
          const situacao = info.event.extendedProps.situacao;

          let cor = '';
          switch (situacao) {
              case 'APROVADO':
              cor = '#088A08'; // verde
              break;
              case 'RECUSADO':
              cor = '#B40404'; // vermelho
              break;
              case 'EM ANALISE':
              cor = '#DF7401'; // laranja
              break;
              case 'SELECIONADO':
              cor = '#B40404'; 
              break;
              default:
              cor = '#9E9E9E'; // cinza para desconhecidos
          }

          // Aplica a cor de fundo
          info.el.style.backgroundColor = cor;

          // Se quiser, pode também alterar o texto
          info.el.title = situacao;
      },
      eventClick: function(info) {
        const evento = info.event;
        
        // Preenche seu modal com os dados do evento
        document.getElementById('modal-titulo').innerText = `Evento: ${evento.title || 'Sem título'}`;
        // document.getElementById('modal-inicio').innerText = `Início: ${evento.startStr}`;
        // document.getElementById('modal-fim').innerText = `Fim: ${evento.endStr || evento.startStr}`;
        // document.getElementById('modal-categoria').innerText = `Categoria: ${evento.extendedProps.categoria || '-'}`;
        document.getElementById('modal-situacao').innerText = `Situação: ${evento.extendedProps.situacao || '-'}`;
        document.getElementById('modal-id').innerText = `ID: ${evento.extendedProps.identificador || '-'}`
        // Exibe o modal
        document.getElementById('meu-modal').style.display = 'block';
      },
    //   dateClick: function(info) {
    //   const titulo = prompt("Título do evento:");
    //   if (titulo) {
    //       const novoEvento = {
    //       title: titulo,
    //       start: info.dateStr,
    //       dayMaxEvents: 3,  // no máximo 3 eventos por dia
    //       allDay: true
    //       };
    //       fetch("/eventos", {
    //       method: "POST",
    //       headers: { "Content-Type": "application/json" },
    //       body: JSON.stringify(novoEvento)
    //       })
    //       .then(res => res.json())
    //       .then(() => {
    //       calendar.refetchEvents(); // recarrega todos os eventos do backend
    //       });
    //   }
    //   }
    });
    calendar.render();

    function atualizarCalendario() {
        const mes = parseInt(document.getElementById('mes_filtro').value);
        const ano = parseInt(document.getElementById('ano_filtro').value);
    
        if (mes >= 1 && mes <= 12 && ano > 1000) {
          const data = `${ano}-${String(mes).padStart(2, '0')}-01`;
          calendar.gotoDate(data);
        }
    }


    // Atualiza ao digitar ou mudar os valores
    document.getElementById('mes_filtro').addEventListener('input', atualizarCalendario);
    document.getElementById('ano_filtro').addEventListener('input', atualizarCalendario);

    
});

