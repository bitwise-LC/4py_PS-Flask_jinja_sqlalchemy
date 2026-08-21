import os
from pathlib import Path

from flask import Flask, jsonify, render_template

from backend.database import db
from backend.services.exceptions import RegraNegocioError


def create_app(test_config=None):
    raiz = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=str(raiz / "frontend" / "templates"),
        static_folder=str(raiz / "frontend" / "static"),
        static_url_path="/static",
    )
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "desenvolvimento-local"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///validade.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)

    from backend.models import Categoria, Lote, Produto
    from backend.routes.api import api_bp

    app.register_blueprint(api_bp)

    @app.get("/")
    @app.get("/dashboard")
    def dashboard():
        return render_template("dashboard.html", pagina="dashboard")

    @app.get("/calendario")
    def calendario():
        return render_template("calendario.html", pagina="calendario")

    @app.get("/estoque")
    def estoque():
        return render_template("estoque.html", pagina="estoque")

    @app.get("/categorias")
    def categorias():
        return render_template("categorias.html", pagina="categorias")

    @app.get("/api/saude")
    def saude():
        return jsonify({"status": "ok"})

    @app.errorhandler(RegraNegocioError)
    def tratar_regra_negocio(erro):
        return jsonify({"erro": str(erro)}), erro.status_code

    @app.errorhandler(404)
    def tratar_nao_encontrado(erro):
        return jsonify({"erro": "Rota não encontrada"}), 404

    app.json.ensure_ascii = False

    with app.app_context():
        db.create_all()

    return app
