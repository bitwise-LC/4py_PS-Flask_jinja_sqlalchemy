export const escapar = valor => String(valor ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

export const dataLocal = valor => new Date(`${valor}T12:00:00`);

export const formatarData = valor => (
    new Intl.DateTimeFormat("pt-BR").format(dataLocal(valor))
);

export const formatarNumero = valor => (
    new Intl.NumberFormat("pt-BR").format(Number(valor || 0))
);

export const plural = (quantidade, singular, pluralTexto) => (
    `${quantidade} ${quantidade === 1 ? singular : pluralTexto}`
);

export const rotuloStatus = status => ({
    vencido: "Vencido",
    critico: "Crítico",
    atencao: "Atenção",
    valido: "Válido"
})[status] || status;

export const descreverPrazo = lote => {
    const dias = Number(lote.dias_para_vencer);

    if (lote.status_validade === "vencido") {
        const atraso = Math.abs(dias);
        return `Venceu há ${plural(atraso, "dia", "dias")}`;
    }

    if (dias === 0) {
        return "Vence hoje";
    }

    return `Vence em ${plural(dias, "dia", "dias")}`;
};

export const vazio = mensagem => (
    `<div class="empty-state">${escapar(mensagem)}</div>`
);

let tempoToast;

export const mostrarToast = (mensagem, erro = false) => {
    const toast = document.getElementById("toast");
    toast.textContent = mensagem;
    toast.className = erro ? "toast visible error" : "toast visible";
    clearTimeout(tempoToast);
    tempoToast = setTimeout(() => {
        toast.className = "toast";
    }, 3200);
};

export const iniciarDialogos = () => {
    document.querySelectorAll("[data-close-dialog]").forEach(botao => {
        botao.addEventListener("click", () => {
            botao.closest("dialog").close();
        });
    });

    document.querySelectorAll("dialog").forEach(dialogo => {
        dialogo.addEventListener("click", evento => {
            if (evento.target === dialogo) {
                dialogo.close();
            }
        });
    });
};
