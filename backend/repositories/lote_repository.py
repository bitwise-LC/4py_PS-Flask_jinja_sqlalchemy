from datetime import date, timedelta

from sqlalchemy import case, func

from backend.database import db
from backend.models.lote import Lote
from backend.models.produto import Produto


class LoteRepository:
    @staticmethod
    def buscar_por_numero(n_lote):
        return Lote.query.filter_by(n_lote=n_lote).first()

    @staticmethod
    def listar_com_filtros(status=None, produto_id=None, busca=None):
        hoje = date.today()
        consulta = Lote.query.join(Produto)
        if produto_id:
            consulta = consulta.filter(Lote.produto_id == produto_id)
        if busca:
            termo = f"%{busca.strip()}%"
            consulta = consulta.filter(
                Lote.n_lote.ilike(termo)
                | Produto.nome.ilike(termo)
                | Produto.codigo_produto.ilike(termo)
            )
        if status == "vencido":
            consulta = consulta.filter(Lote.validade < hoje)
        elif status == "critico":
            consulta = consulta.filter(Lote.validade.between(hoje, hoje + timedelta(days=7)))
        elif status == "atencao":
            consulta = consulta.filter(Lote.validade.between(hoje + timedelta(days=8), hoje + timedelta(days=30)))
        elif status == "valido":
            consulta = consulta.filter(Lote.validade > hoje + timedelta(days=30))
        return consulta.order_by(Lote.validade, Lote.n_lote).all()

    @staticmethod
    def listar_alertas_validade():
        hoje = date.today()
        limite_critico = hoje + timedelta(days=7)
        return (
            Lote.query
            .filter(Lote.validade <= limite_critico)
            .order_by(Lote.validade, Lote.n_lote)
            .all()
        )

    @staticmethod
    def gerar_resumo_validade():
        hoje = date.today()
        limite_critico = hoje + timedelta(days=7)
        limite_atencao = hoje + timedelta(days=30)
        resultado = db.session.query(
            func.count(Lote.id_lote).label("total_lotes"),
            func.coalesce(func.sum(Lote.quantidade_produtos), 0).label("total_unidades"),
            func.coalesce(func.sum(case((Lote.validade < hoje, 1), else_=0)), 0).label("vencidos"),
            func.coalesce(func.sum(case((Lote.validade.between(hoje, limite_critico), 1), else_=0)), 0).label("criticos"),
            func.coalesce(func.sum(case((Lote.validade.between(limite_critico + timedelta(days=1), limite_atencao), 1), else_=0)), 0).label("atencao"),
            func.coalesce(func.sum(case((Lote.validade > limite_atencao, 1), else_=0)), 0).label("validos"),
        ).one()
        total_lotes = int(resultado.total_lotes or 0)
        total_unidades = int(resultado.total_unidades or 0)
        vencidos = int(resultado.vencidos or 0)
        criticos = int(resultado.criticos or 0)
        atencao = int(resultado.atencao or 0)
        validos = int(resultado.validos or 0)
        percentual_validos = round((validos / total_lotes) * 100) if total_lotes else 0
        proximos = (
            Lote.query
            .filter(Lote.validade >= hoje)
            .order_by(Lote.validade)
            .limit(5)
            .all()
        )
        return {
            "total_lotes": total_lotes,
            "total_unidades": total_unidades,
            "vencidos": vencidos,
            "criticos": criticos,
            "atencao": atencao,
            "validos": validos,
            "percentual_validos": percentual_validos,
            "proximos_vencimentos": [lote.to_dict() for lote in proximos],
        }
