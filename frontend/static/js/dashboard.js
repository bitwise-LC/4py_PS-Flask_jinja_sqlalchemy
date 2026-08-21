import { buscarPainel } from "./api.js";
import {
    escapar,
    formatarData,
    formatarNumero,
    plural,
    rotuloStatus,
    vazio
} from "./ui.js";

const preencherIndicadores = painel => {
    const campos = {
        "dashboard-total-lotes": painel.total_lotes,
        "dashboard-total-unidades": formatarNumero(painel.total_unidades),
        "dashboard-vencidos": painel.vencidos,
        "dashboard-criticos": painel.criticos,
        "dashboard-atencao": painel.atencao,
        "dashboard-validos": painel.validos
    };

    Object.entries(campos).forEach(([id, valor]) => {
        document.getElementById(id).textContent = valor;
    });
};

const renderizarProximosVencimentos = lotes => {
    document.getElementById("dashboard-proximos").innerHTML = lotes.map(lote => `
        <article class="upcoming-item">
            <div>
                <strong>${escapar(lote.produto.nome)}</strong>
                <small>${escapar(lote.produto.codigo_produto)} · lote ${escapar(lote.n_lote)}</small>
            </div>
            <div>
                <strong>${formatarData(lote.validade)}</strong>
                <small>${plural(lote.dias_para_vencer, "dia restante", "dias restantes")}</small>
            </div>
            <span class="status ${lote.status_validade}">${rotuloStatus(lote.status_validade)}</span>
        </article>
    `).join("") || vazio("Nenhum vencimento futuro cadastrado.");
};

const preencherPercentual = percentual => {
    document.getElementById("dashboard-percentual").textContent = `${percentual}%`;
    document.getElementById("validity-donut").style.setProperty(
        "--valid-percent",
        `${percentual}%`
    );
};

export const iniciarDashboard = async () => {
    const painel = await buscarPainel();
    preencherIndicadores(painel);
    renderizarProximosVencimentos(painel.proximos_vencimentos);
    preencherPercentual(painel.percentual_validos);
};
