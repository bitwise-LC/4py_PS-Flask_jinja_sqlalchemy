const requisicao = async (url, opcoes = {}) => {
    const configuracao = {
        ...opcoes,
        headers: {
            "Content-Type": "application/json",
            ...(opcoes.headers || {})
        }
    };
    const resposta = await fetch(url, configuracao);
    const dados = await resposta.json();

    if (!resposta.ok) {
        throw new Error(dados.erro || "Não foi possível concluir a operação");
    }

    return dados;
};

const criarConsulta = filtros => {
    const parametros = new URLSearchParams();

    Object.entries(filtros).forEach(([chave, valor]) => {
        if (valor !== undefined && valor !== null && valor !== "") {
            parametros.set(chave, valor);
        }
    });

    const consulta = parametros.toString();
    return consulta ? `?${consulta}` : "";
};

const enviarJson = (metodo, dados) => ({
    method: metodo,
    body: JSON.stringify(dados)
});

export const buscarPainel = () => requisicao("/api/painel");

export const listarAlertasValidade = () => requisicao("/api/lotes/alertas");

export const listarCategorias = () => requisicao("/api/categorias");

export const cadastrarCategoria = dados => (
    requisicao("/api/categorias", enviarJson("POST", dados))
);

export const atualizarCategoria = (id, dados) => (
    requisicao(`/api/categorias/${id}`, enviarJson("PUT", dados))
);

export const excluirCategoria = id => (
    requisicao(`/api/categorias/${id}`, { method: "DELETE" })
);

export const listarProdutos = (filtros = {}) => (
    requisicao(`/api/produtos${criarConsulta(filtros)}`)
);

export const cadastrarProduto = dados => (
    requisicao("/api/produtos", enviarJson("POST", dados))
);

export const atualizarProduto = (id, dados) => (
    requisicao(`/api/produtos/${id}`, enviarJson("PUT", dados))
);

export const excluirProduto = id => (
    requisicao(`/api/produtos/${id}`, { method: "DELETE" })
);

export const listarLotes = (filtros = {}) => (
    requisicao(`/api/lotes${criarConsulta(filtros)}`)
);

export const cadastrarLote = dados => (
    requisicao("/api/lotes", enviarJson("POST", dados))
);

export const atualizarLote = (id, dados) => (
    requisicao(`/api/lotes/${id}`, enviarJson("PUT", dados))
);

export const excluirLote = id => (
    requisicao(`/api/lotes/${id}`, { method: "DELETE" })
);
