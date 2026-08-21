import { iniciarNotificacoes } from "./notificacoes.js";
import { iniciarDialogos, mostrarToast } from "./ui.js";

const inicializadores = {
    dashboard: async () => {
        const { iniciarDashboard } = await import("./dashboard.js");
        await iniciarDashboard();
    },
    estoque: async () => {
        const { iniciarEstoque } = await import("./estoque.js");
        await iniciarEstoque();
    },
    categorias: async () => {
        const { iniciarCategorias } = await import("./categorias.js");
        await iniciarCategorias();
    },
    calendario: async () => {
        const { iniciarCalendario } = await import("./calendario.js");
        await iniciarCalendario();
    }
};

const iniciar = async () => {
    iniciarDialogos();
    const iniciarPagina = inicializadores[document.body.dataset.page];

    try {
        await Promise.all([
            iniciarNotificacoes(),
            iniciarPagina ? iniciarPagina() : Promise.resolve()
        ]);
    } catch (erro) {
        mostrarToast(erro.message, true);
    }
};

iniciar();
