import {
    atualizarCategoria,
    cadastrarCategoria,
    excluirCategoria,
    listarCategorias
} from "./api.js";
import {
    escapar,
    mostrarToast,
    plural,
    vazio
} from "./ui.js";

const estado = {
    categorias: []
};

const renderizarCategorias = () => {
    const termo = document.getElementById("category-search").value
        .trim()
        .toLowerCase();
    const categorias = estado.categorias.filter(categoria => (
        `${categoria.nome} ${categoria.descricao}`.toLowerCase().includes(termo)
    ));

    document.getElementById("category-grid").innerHTML = categorias.map(categoria => `
        <article class="category-card">
            <div class="category-card-top">
                <span class="category-symbol">${escapar(categoria.nome.slice(0, 2).toUpperCase())}</span>
                <div class="card-actions">
                    <button class="icon-button" type="button" data-action="edit-category" data-id="${categoria.id_categoria}" title="Editar categoria">✎</button>
                    <button class="icon-button danger" type="button" data-action="delete-category" data-id="${categoria.id_categoria}" title="Excluir categoria">×</button>
                </div>
            </div>
            <h2>${escapar(categoria.nome)}</h2>
            <p class="category-description">${escapar(categoria.descricao)}</p>
            <div class="category-footer">
                <span>${plural(categoria.quantidade_produtos, "produto vinculado", "produtos vinculados")}</span>
            </div>
        </article>
    `).join("") || vazio("Nenhuma categoria encontrada.");
};

const carregarCategorias = async () => {
    estado.categorias = await listarCategorias();
    renderizarCategorias();
};

const abrirCategoria = categoria => {
    document.getElementById("category-form").reset();
    document.getElementById("category-id").value = categoria?.id_categoria || "";
    document.getElementById("category-name").value = categoria?.nome || "";
    document.getElementById("category-description").value = categoria?.descricao || "";
    document.getElementById("category-dialog-title").textContent = categoria
        ? "Alterar categoria"
        : "Nova categoria";
    document.getElementById("category-dialog").showModal();
};

const tratarAcaoCategoria = async evento => {
    const botao = evento.target.closest("[data-action]");

    if (!botao) {
        return;
    }

    const id = Number(botao.dataset.id);

    if (botao.dataset.action === "edit-category") {
        abrirCategoria(
            estado.categorias.find(categoria => categoria.id_categoria === id)
        );
        return;
    }

    if (!window.confirm("Deseja realmente excluir esta categoria?")) {
        return;
    }

    try {
        await excluirCategoria(id);
        await carregarCategorias();
        mostrarToast("Categoria excluída");
    } catch (erro) {
        mostrarToast(erro.message, true);
    }
};

const salvarCategoria = async evento => {
    evento.preventDefault();
    const id = document.getElementById("category-id").value;
    const dados = {
        nome: document.getElementById("category-name").value,
        descricao: document.getElementById("category-description").value
    };

    try {
        if (id) {
            await atualizarCategoria(id, dados);
        } else {
            await cadastrarCategoria(dados);
        }

        document.getElementById("category-dialog").close();
        await carregarCategorias();
        mostrarToast(id ? "Categoria atualizada" : "Categoria cadastrada");
    } catch (erro) {
        mostrarToast(erro.message, true);
    }
};

export const iniciarCategorias = async () => {
    await carregarCategorias();
    document.getElementById("new-category").addEventListener(
        "click",
        () => abrirCategoria()
    );
    document.getElementById("category-search").addEventListener(
        "input",
        renderizarCategorias
    );
    document.getElementById("category-grid").addEventListener(
        "click",
        tratarAcaoCategoria
    );
    document.getElementById("category-form").addEventListener(
        "submit",
        salvarCategoria
    );
};
