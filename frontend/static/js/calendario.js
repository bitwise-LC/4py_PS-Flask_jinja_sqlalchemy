import { listarLotes } from "./api.js";
import {
    dataLocal,
    escapar,
    formatarNumero,
    rotuloStatus,
    vazio
} from "./ui.js";

const estado = {
    lotes: [],
    mes: new Date(new Date().getFullYear(), new Date().getMonth(), 1)
};

const chaveData = data => {
    const ano = data.getFullYear();
    const mes = String(data.getMonth() + 1).padStart(2, "0");
    const dia = String(data.getDate()).padStart(2, "0");
    return `${ano}-${mes}-${dia}`;
};

const mostrarDia = data => {
    document.querySelectorAll(".calendar-day").forEach(dia => {
        dia.classList.toggle("selected", dia.dataset.date === data);
    });

    const lotes = estado.lotes.filter(lote => lote.validade === data);
    document.getElementById("calendar-detail-title").textContent = (
        new Intl.DateTimeFormat("pt-BR", {
            day: "2-digit",
            month: "long",
            year: "numeric"
        }).format(dataLocal(data))
    );
    document.getElementById("calendar-detail-list").innerHTML = lotes.map(lote => `
        <article class="calendar-lot">
            <strong>${escapar(lote.produto.nome)}</strong>
            <small>Lote ${escapar(lote.n_lote)} · ${formatarNumero(lote.quantidade_produtos)} unidades</small>
            <span class="status ${lote.status_validade}">${rotuloStatus(lote.status_validade)}</span>
        </article>
    `).join("") || vazio("Nenhum lote vence nesta data.");
};

const criarDia = (data, mesAtual, hoje) => {
    const chave = chaveData(data);
    const lotes = estado.lotes.filter(lote => lote.validade === chave);
    const classes = ["calendar-day"];

    if (data.getMonth() !== mesAtual) {
        classes.push("other-month");
    }

    if (chave === hoje) {
        classes.push("today");
    }

    if (lotes.length) {
        classes.push("has-batches");
    }

    const marcadores = lotes.slice(0, 8).map(lote => (
        `<i class="calendar-marker ${lote.status_validade}" title="${escapar(lote.produto.nome)}"></i>`
    )).join("");

    return `
        <div class="${classes.join(" ")}" data-date="${chave}">
            <span class="calendar-number">${data.getDate()}</span>
            <div class="calendar-markers">${marcadores}</div>
        </div>
    `;
};

const renderizarCalendario = () => {
    const ano = estado.mes.getFullYear();
    const mes = estado.mes.getMonth();
    const primeiroDia = new Date(ano, mes, 1);
    const inicio = new Date(ano, mes, 1 - primeiroDia.getDay());
    const hoje = chaveData(new Date());
    const dias = [];

    document.getElementById("calendar-title").textContent = (
        new Intl.DateTimeFormat("pt-BR", {
            month: "long",
            year: "numeric"
        }).format(estado.mes)
    );

    for (let indice = 0; indice < 42; indice += 1) {
        const data = new Date(
            inicio.getFullYear(),
            inicio.getMonth(),
            inicio.getDate() + indice
        );
        dias.push(criarDia(data, mes, hoje));
    }

    document.getElementById("calendar-days").innerHTML = dias.join("");
};

const alterarMes = deslocamento => {
    estado.mes = new Date(
        estado.mes.getFullYear(),
        estado.mes.getMonth() + deslocamento,
        1
    );
    renderizarCalendario();
};

export const iniciarCalendario = async () => {
    estado.lotes = await listarLotes();
    renderizarCalendario();

    const primeiroLote = estado.lotes.find(lote => {
        const validade = dataLocal(lote.validade);
        return validade.getMonth() === estado.mes.getMonth()
            && validade.getFullYear() === estado.mes.getFullYear();
    });

    if (primeiroLote) {
        mostrarDia(primeiroLote.validade);
    }

    document.getElementById("calendar-previous").addEventListener(
        "click",
        () => alterarMes(-1)
    );
    document.getElementById("calendar-next").addEventListener(
        "click",
        () => alterarMes(1)
    );
    document.getElementById("calendar-days").addEventListener("click", evento => {
        const dia = evento.target.closest(".calendar-day");

        if (dia) {
            mostrarDia(dia.dataset.date);
        }
    });
};
