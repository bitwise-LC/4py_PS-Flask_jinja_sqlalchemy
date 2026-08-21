from sqlalchemy.exc import IntegrityError

from backend.database import db
from backend.models.categoria import Categoria
from backend.services.exceptions import ConflitoError, RecursoNaoEncontradoError
from backend.services.validacoes import texto_obrigatorio


class ListarCategoriasService:
    @staticmethod
    def executar():
        return [categoria.to_dict() for categoria in Categoria.listar_todos()]


class CadastrarCategoriaService:
    @staticmethod
    def executar(dados):
        nome = texto_obrigatorio(dados, "nome", 2)
        descricao = texto_obrigatorio(dados, "descricao", 3)
        if Categoria.buscar_por_nome(nome):
            raise ConflitoError("Já existe uma categoria com esse nome")
        try:
            return Categoria(nome=nome, descricao=descricao).salvar().to_dict()
        except IntegrityError:
            db.session.rollback()
            raise ConflitoError("Já existe uma categoria com esse nome")


class AtualizarCategoriaService:
    @staticmethod
    def executar(categoria_id, dados):
        categoria = Categoria.buscar_por_id(categoria_id)
        if not categoria:
            raise RecursoNaoEncontradoError("Categoria não encontrada")
        nome = texto_obrigatorio(dados, "nome", 2)
        descricao = texto_obrigatorio(dados, "descricao", 3)
        existente = Categoria.buscar_por_nome(nome)
        if existente and existente.id_categoria != categoria.id_categoria:
            raise ConflitoError("Já existe uma categoria com esse nome")
        try:
            return categoria.atualizar(nome, descricao).to_dict()
        except IntegrityError:
            db.session.rollback()
            raise ConflitoError("Já existe uma categoria com esse nome")


class ExcluirCategoriaService:
    @staticmethod
    def executar(categoria_id):
        categoria = Categoria.buscar_por_id(categoria_id)
        if not categoria:
            raise RecursoNaoEncontradoError("Categoria não encontrada")
        if categoria.produtos:
            raise ConflitoError("A categoria possui produtos vinculados e não pode ser excluída")
        categoria.deletar()
        return {"id_categoria": categoria_id, "mensagem": "Categoria excluída"}
