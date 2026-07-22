document.addEventListener("DOMContentLoaded", function () {
    const mensagemVazia = document.getElementById("mensagem-vazia");
    const mensagemErro = document.getElementById("mensagem-erro");
    const inputBusca = document.getElementById("busca");

    const table = new Tabulator("#agenda-table", {
        layout: "fitColumns",
        placeholder: "Nenhum agendamento disponível.",
        columns: [
            { title: "Data", field: "data", sorter: "date" },
            { title: "Horário", field: "horario" },
            { title: "Paciente", field: "paciente" },
            { title: "CPF", field: "cpf" },
            { title: "Médico", field: "medico" },
            { title: "Especialidade", field: "especialidade" },
            { title: "Convênio", field: "convenio" },
            { title: "Status", field: "status" },
        ],
    });

    function carregarAgendamentos(termoBusca) {
        mensagemErro.style.display = "none";
        mensagemVazia.style.display = "none";

        const params = termoBusca ? `?busca=${encodeURIComponent(termoBusca)}` : "";

        fetch(`/api/agenda/dados${params}`)
            .then((response) => {
                if (!response.ok) {
                    return response.json().then((body) => {
                        throw new Error(body.erro || "Erro ao carregar agendamentos.");
                    });
                }
                return response.json();
            })
            .then((resultado) => {
                table.setData(resultado.dados);
                if (resultado.dados.length === 0) {
                    mensagemVazia.style.display = "block";
                }
            })
            .catch((erro) => {
                mensagemErro.textContent = erro.message;
                mensagemErro.style.display = "block";
                table.setData([]);
            });
    }

    let debounceTimer;
    inputBusca.addEventListener("input", function () {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            carregarAgendamentos(inputBusca.value);
        }, 300);
    });

    carregarAgendamentos("");
});