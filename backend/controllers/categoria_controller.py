from flask import jsonify, request

from backend.services.categoria_services import (
    AtualizarCategoriaService,
    CadastrarCategoriaService,
    ExcluirCategoriaService,
    ListarCategoriasService,
)


class CategoriaController:
    @staticmethod
    def listar():
        return jsonify(ListarCategoriasService.executar()), 200

    @staticmethod
    def cadastrar():
        categoria = CadastrarCategoriaService.executar(request.get_json(silent=True) or {})
        return jsonify(categoria), 201

    @staticmethod
    def atualizar(categoria_id):
        categoria = AtualizarCategoriaService.executar(
            categoria_id, request.get_json(silent=True) or {}
        )
        return jsonify(categoria), 200

    @staticmethod
    def excluir(categoria_id):
        return jsonify(ExcluirCategoriaService.executar(categoria_id)), 200
