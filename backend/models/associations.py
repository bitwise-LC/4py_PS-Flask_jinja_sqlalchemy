from backend.database import db


produto_categoria = db.Table(
    "produto_categoria",
    db.Column("produto_id", db.Integer, db.ForeignKey("produtos.id_produto"), primary_key=True),
    db.Column("categoria_id", db.Integer, db.ForeignKey("categorias.id_categoria"), primary_key=True),
)
