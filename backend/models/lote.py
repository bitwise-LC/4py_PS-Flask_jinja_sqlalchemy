from datetime import date

from backend.database import db


class Lote(db.Model):
    __tablename__ = "lotes"

    id_lote = db.Column(db.Integer, primary_key=True)
    n_lote = db.Column(db.String(50), unique=True, nullable=False, index=True)
    data_fabricacao = db.Column(db.Date, nullable=False)
    validade = db.Column(db.Date, nullable=False, index=True)
    quantidade_produtos = db.Column(db.Integer, nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id_produto"), nullable=False)
    produto = db.relationship("Produto", back_populates="lotes")

    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self, n_lote, data_fabricacao, validade, quantidade_produtos, produto):
        self.n_lote = n_lote
        self.data_fabricacao = data_fabricacao
        self.validade = validade
        self.quantidade_produtos = quantidade_produtos
        self.produto = produto
        db.session.commit()
        return self

    def deletar(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def listar_todos(cls):
        return cls.query.order_by(cls.validade, cls.n_lote).all()

    @classmethod
    def buscar_por_id(cls, lote_id):
        return db.session.get(cls, lote_id)

    @property
    def dias_para_vencer(self):
        return (self.validade - date.today()).days

    @property
    def status_validade(self):
        dias = self.dias_para_vencer
        if dias < 0:
            return "vencido"
        if dias <= 7:
            return "critico"
        if dias <= 30:
            return "atencao"
        return "valido"

    def to_dict(self):
        return {
            "id_lote": self.id_lote,
            "n_lote": self.n_lote,
            "data_fabricacao": self.data_fabricacao.isoformat(),
            "validade": self.validade.isoformat(),
            "quantidade_produtos": self.quantidade_produtos,
            "produto_id": self.produto_id,
            "produto": {
                "id_produto": self.produto.id_produto,
                "codigo_produto": self.produto.codigo_produto,
                "nome": self.produto.nome,
            },
            "dias_para_vencer": self.dias_para_vencer,
            "status_validade": self.status_validade,
        }
