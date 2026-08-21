from flask import jsonify, request

from backend.services.lote_services import (
    AtualizarLoteService,
    CadastrarLoteService,
    ExcluirLoteService,
    GerarPainelValidadeService,
    ListarAlertasValidadeService,
    ListarLotesService,
)

class LoteController:
    @staticmethod
    def listar():
        lotes = ListarLotesService.executar(
            status=request.args.get("status"),
            produto_id=request.args.get("produto_id"),
            busca=request.args.get("busca"),
        )
        return jsonify(lotes), 200

    @staticmethod
    def listar_alertas():
        return jsonify(ListarAlertasValidadeService.executar()), 200

    @staticmethod
    def cadastrar():
        lote = CadastrarLoteService.executar(request.get_json(silent=True) or {})
        return jsonify(lote), 201

    @staticmethod
    def atualizar(lote_id):
        lote = AtualizarLoteService.executar(
            lote_id, request.get_json(silent=True) or {}
        )
        return jsonify(lote), 200

    @staticmethod
    def excluir(lote_id):
        return jsonify(ExcluirLoteService.executar(lote_id)), 200

    @staticmethod
    def painel():
        return jsonify(GerarPainelValidadeService.executar()), 200
