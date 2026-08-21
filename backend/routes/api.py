from flask import Blueprint

from backend.controllers.categoria_controller import CategoriaController
from backend.controllers.lote_controller import LoteController
from backend.controllers.produto_controller import ProdutoController


api_bp = Blueprint("api", __name__, url_prefix="/api")

api_bp.add_url_rule("/categorias", endpoint="listar_categorias", view_func=CategoriaController.listar, methods=["GET"])
api_bp.add_url_rule("/categorias", endpoint="cadastrar_categoria", view_func=CategoriaController.cadastrar, methods=["POST"])
api_bp.add_url_rule("/categorias/<int:categoria_id>", endpoint="atualizar_categoria", view_func=CategoriaController.atualizar, methods=["PUT"])
api_bp.add_url_rule("/categorias/<int:categoria_id>", endpoint="excluir_categoria", view_func=CategoriaController.excluir, methods=["DELETE"])
api_bp.add_url_rule("/produtos", endpoint="listar_produtos", view_func=ProdutoController.listar, methods=["GET"])
api_bp.add_url_rule("/produtos", endpoint="cadastrar_produto", view_func=ProdutoController.cadastrar, methods=["POST"])
api_bp.add_url_rule("/produtos/<int:produto_id>", endpoint="atualizar_produto", view_func=ProdutoController.atualizar, methods=["PUT"])
api_bp.add_url_rule("/produtos/<int:produto_id>", endpoint="excluir_produto", view_func=ProdutoController.excluir, methods=["DELETE"])
api_bp.add_url_rule("/lotes", endpoint="listar_lotes", view_func=LoteController.listar, methods=["GET"])
api_bp.add_url_rule("/lotes/alertas", endpoint="listar_alertas_lotes", view_func=LoteController.listar_alertas, methods=["GET"])
api_bp.add_url_rule("/lotes", endpoint="cadastrar_lote", view_func=LoteController.cadastrar, methods=["POST"])
api_bp.add_url_rule("/lotes/<int:lote_id>", endpoint="atualizar_lote", view_func=LoteController.atualizar, methods=["PUT"])
api_bp.add_url_rule("/lotes/<int:lote_id>", endpoint="excluir_lote", view_func=LoteController.excluir, methods=["DELETE"])
api_bp.add_url_rule("/painel", endpoint="gerar_painel", view_func=LoteController.painel, methods=["GET"])
