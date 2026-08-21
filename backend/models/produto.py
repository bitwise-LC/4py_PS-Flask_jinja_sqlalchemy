from backend.database import db
from backend.models.associations import produto_categoria


class Produto(db.Model):
    __tablename__ = "produtos"

    id_produto = db.Column(db.Integer, primary_key=True)
    codigo_produto = db.Column(db.String(40), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    categorias = db.relationship(
        "Categoria",
        secondary=produto_categoria,
        backref=db.backref("produtos", lazy="select"),
        lazy="select",
    )
    lotes = db.relationship("Lote", back_populates="produto", lazy="select")

    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self, codigo_produto, nome, descricao, categorias):
        self.codigo_produto = codigo_produto
        self.nome = nome
        self.descricao = descricao
        self.categorias = categorias
        db.session.commit()
        return self

    def deletar(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def listar_todos(cls):
        return cls.query.order_by(cls.nome).all()

    @classmethod
    def buscar_por_id(cls, produto_id):
        return db.session.get(cls, produto_id)

    def to_dict(self):
        return {
            "id_produto": self.id_produto,
            "codigo_produto": self.codigo_produto,
            "nome": self.nome,
            "descricao": self.descricao,
            "categorias": [categoria.to_dict() for categoria in self.categorias],
            "quantidade_lotes": len(self.lotes),
        }
