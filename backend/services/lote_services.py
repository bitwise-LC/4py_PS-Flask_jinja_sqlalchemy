from sqlalchemy.exc import IntegrityError

from backend.database import db
from backend.models.lote import Lote
from backend.models.produto import Produto
from backend.repositories.lote_repository import LoteRepository
from backend.services.exceptions import ConflitoError, RecursoNaoEncontradoError, RegraNegocioError
from backend.services.validacoes import data_iso_obrigatoria, inteiro_positivo, texto_obrigatorio


def validar_dados_lote(dados):
    numero = texto_obrigatorio(dados, "n_lote", 2).upper()
    fabricacao = data_iso_obrigatoria(dados, "data_fabricacao")
    validade = data_iso_obrigatoria(dados, "validade")
    quantidade = inteiro_positivo(dados, "quantidade_produtos")
    produto_id = inteiro_positivo(dados, "produto_id")
    produto = Produto.buscar_por_id(produto_id)
    if not produto:
        raise RegraNegocioError("Produto informado não existe")
    if validade < fabricacao:
        raise RegraNegocioError("A validade não pode ser anterior à data de fabricação")
    return numero, fabricacao, validade, quantidade, produto


class ListarLotesService:
    @staticmethod
    def executar(status=None, produto_id=None, busca=None):
        status_validos = {None, "", "vencido", "critico", "atencao", "valido"}
        if status not in status_validos:
            raise RegraNegocioError("Status de validade inválido")
        if produto_id:
            try:
                produto_id = int(produto_id)
            except ValueError:
                raise RegraNegocioError("Produto inválido")
        lotes = LoteRepository.listar_com_filtros(status, produto_id, busca)
        return [lote.to_dict() for lote in lotes]


class ListarAlertasValidadeService:
    @staticmethod
    def executar():
        lotes = LoteRepository.listar_alertas_validade()
        return [lote.to_dict() for lote in lotes]


class CadastrarLoteService:
    @staticmethod
    def executar(dados):
        numero, fabricacao, validade, quantidade, produto = validar_dados_lote(dados)
        if LoteRepository.buscar_por_numero(numero):
            raise ConflitoError("Já existe um lote com esse número")
        try:
            lote = Lote(
                n_lote=numero,
                data_fabricacao=fabricacao,
                validade=validade,
                quantidade_produtos=quantidade,
                produto=produto,
            )
            return lote.salvar().to_dict()
        except IntegrityError:
            db.session.rollback()
            raise ConflitoError("Já existe um lote com esse número")


class AtualizarLoteService:
    @staticmethod
    def executar(lote_id, dados):
        lote = Lote.buscar_por_id(lote_id)
        if not lote:
            raise RecursoNaoEncontradoError("Lote não encontrado")
        numero, fabricacao, validade, quantidade, produto = validar_dados_lote(dados)
        existente = LoteRepository.buscar_por_numero(numero)
        if existente and existente.id_lote != lote.id_lote:
            raise ConflitoError("Já existe um lote com esse número")
        try:
            return lote.atualizar(numero, fabricacao, validade, quantidade, produto).to_dict()
        except IntegrityError:
            db.session.rollback()
            raise ConflitoError("Já existe um lote com esse número")


class ExcluirLoteService:
    @staticmethod
    def executar(lote_id):
        lote = Lote.buscar_por_id(lote_id)
        if not lote:
            raise RecursoNaoEncontradoError("Lote não encontrado")
        lote.deletar()
        return {"id_lote": lote_id, "mensagem": "Lote excluído"}


class GerarPainelValidadeService:
    @staticmethod
    def executar():
        return LoteRepository.gerar_resumo_validade()
