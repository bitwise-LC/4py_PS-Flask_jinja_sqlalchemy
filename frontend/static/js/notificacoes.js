import { listarAlertasValidade } from "./api.js";
import {
    descreverPrazo,
    escapar,
    formatarData,
    vazio
} from "./ui.js";

const abrirNotificacoes = () => {
    document.getElementById("notification-drawer").classList.add("open");
    document.getElementById("drawer-overlay").classList.add("open");
};

const fecharNotificacoes = () => {
    document.getElementById("notification-drawer").classList.remove("open");
    document.getElementById("drawer-overlay").classList.remove("open");
};

const renderizarNotificacoes = alertas => {
    const contador = document.getElementById("notification-count");
    contador.textContent = String(alertas.length);
    contador.hidden = alertas.length === 0;
    document.getElementById("notification-list").innerHTML = alertas.map(lote => `
        <article class="notification-item">
            <span class="notification-icon">!</span>
            <div>
                <strong>${escapar(lote.produto.nome)} · ${escapar(lote.n_lote)}</strong>
                <small>${descreverPrazo(lote)}. Validade: ${formatarData(lote.validade)}.</small>
            </div>
        </article>
    `).join("") || vazio("Nenhum lote vencido ou próximo do vencimento.");
};

export const carregarNotificacoes = async () => {
    try {
        renderizarNotificacoes(await listarAlertasValidade());
    } catch (erro) {
        document.getElementById("notification-list").innerHTML = vazio(
            "Não foi possível carregar as notificações."
        );
    }
};

export const iniciarNotificacoes = async () => {
    document.getElementById("open-notifications").addEventListener(
        "click",
        abrirNotificacoes
    );
    document.getElementById("close-notifications").addEventListener(
        "click",
        fecharNotificacoes
    );
    document.getElementById("drawer-overlay").addEventListener(
        "click",
        fecharNotificacoes
    );
    await carregarNotificacoes();
};
