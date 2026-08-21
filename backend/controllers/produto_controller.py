from flask import jsonify, request

from backend.services.produto_services import (
    AtualizarProdutoService,
    CadastrarProdutoService,
    ExcluirProdutoService,
    ListarProdutosService,
)


class ProdutoController:
    @staticmethod
    def listar():
        produtos = ListarProdutosService.executar(
            busca=request.args.get("busca"),
            categoria_id=request.args.get("categoria_id", type=int),
        )
        return jsonify(produtos), 200

    @staticmethod
    def cadastrar():
        produto = CadastrarProdutoService.executar(request.get_json(silent=True) or {})
        return jsonify(produto), 201

    @staticmethod
    def atualizar(produto_id):
        produto = AtualizarProdutoService.executar(
            produto_id, request.get_json(silent=True) or {}
        )
        return jsonify(produto), 200

    @staticmethod
    def excluir(produto_id):
        return jsonify(ExcluirProdutoService.executar(produto_id)), 200
