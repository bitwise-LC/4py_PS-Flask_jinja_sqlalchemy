from sqlalchemy.exc import IntegrityError

from backend.database import db
from backend.models.categoria import Categoria
from backend.models.produto import Produto
from backend.repositories.produto_repository import ProdutoRepository
from backend.services.exceptions import ConflitoError, RecursoNaoEncontradoError, RegraNegocioError
from backend.services.validacoes import texto_obrigatorio


def obter_categorias(dados):
    ids = dados.get("categorias_ids")
    if not isinstance(ids, list) or not ids:
        raise RegraNegocioError("Selecione pelo menos uma categoria")
    categorias = []
    for categoria_id in set(ids):
        try:
            categoria = Categoria.buscar_por_id(int(categoria_id))
        except (TypeError, ValueError):
            categoria = None
        if not categoria:
            raise RegraNegocioError("Uma das categorias informadas não existe")
        categorias.append(categoria)
    return categorias


class ListarProdutosService:
    @staticmethod
    def executar(busca=None, categoria_id=None):
        produtos = ProdutoRepository.listar_com_filtros(busca, categoria_id)
        return [produto.to_dict() for produto in produtos]


class CadastrarProdutoService:
    @staticmethod
    def executar(dados):
        codigo = texto_obrigatorio(dados, "codigo_produto", 2).upper()
        nome = texto_obrigatorio(dados, "nome", 2)
        descricao = texto_obrigatorio(dados, "descricao", 3)
        categorias = obter_categorias(dados)
        if ProdutoRepository.buscar_por_codigo(codigo):
            raise ConflitoError("Já existe um produto com esse código")
        try:
            produto = Produto(codigo_produto=codigo, nome=nome, descricao=descricao, categorias=categorias)
            return produto.salvar().to_dict()
        except IntegrityError:
            db.session.rollback()
            raise ConflitoError("Já existe um produto com esse código")


class AtualizarProdutoService:
    @staticmethod
    def executar(produto_id, dados):
        produto = Produto.buscar_por_id(produto_id)
        if not produto:
            raise RecursoNaoEncontradoError("Produto não encontrado")
        codigo = texto_obrigatorio(dados, "codigo_produto", 2).upper()
        nome = texto_obrigatorio(dados, "nome", 2)
        descricao = texto_obrigatorio(dados, "descricao", 3)
        categorias = obter_categorias(dados)
        existente = ProdutoRepository.buscar_por_codigo(codigo)
        if existente and existente.id_produto != produto.id_produto:
            raise ConflitoError("Já existe um produto com esse código")
        try:
            return produto.atualizar(codigo, nome, descricao, categorias).to_dict()
        except IntegrityError:
            db.session.rollback()
            raise ConflitoError("Já existe um produto com esse código")


class ExcluirProdutoService:
    @staticmethod
    def executar(produto_id):
        produto = Produto.buscar_por_id(produto_id)
        if not produto:
            raise RecursoNaoEncontradoError("Produto não encontrado")
        if produto.lotes:
            raise ConflitoError("O produto possui lotes vinculados e não pode ser excluído")
        produto.deletar()
        return {"id_produto": produto_id, "mensagem": "Produto excluído"}
