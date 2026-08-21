from backend.models.associations import produto_categoria
from backend.models.produto import Produto


class ProdutoRepository:
    @staticmethod
    def buscar_por_codigo(codigo_produto):
        return Produto.query.filter_by(codigo_produto=codigo_produto).first()

    @staticmethod
    def listar_com_filtros(busca=None, categoria_id=None):
        consulta = Produto.query
        if busca:
            termo = f"%{busca.strip()}%"
            consulta = consulta.filter(
                Produto.nome.ilike(termo) | Produto.codigo_produto.ilike(termo)
            )
        if categoria_id:
            consulta = consulta.join(
                produto_categoria,
                Produto.id_produto == produto_categoria.c.produto_id,
            ).filter(produto_categoria.c.categoria_id == categoria_id)
        return consulta.order_by(Produto.nome).all()
