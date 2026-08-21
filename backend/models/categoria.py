from backend.database import db


class Categoria(db.Model):
    __tablename__ = "categorias"

    id_categoria = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(255), nullable=False)

    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
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
    def buscar_por_id(cls, categoria_id):
        return db.session.get(cls, categoria_id)

    @classmethod
    def buscar_por_nome(cls, nome):
        return cls.query.filter(db.func.lower(cls.nome) == nome.lower()).first()

    def to_dict(self):
        return {
            "id_categoria": self.id_categoria,
            "nome": self.nome,
            "descricao": self.descricao,
            "quantidade_produtos": len(self.produtos),
        }
