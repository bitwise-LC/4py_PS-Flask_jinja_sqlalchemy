from datetime import date

from backend.services.exceptions import RegraNegocioError


def texto_obrigatorio(dados, campo, minimo=1):
    valor = str(dados.get(campo, "")).strip()
    if len(valor) < minimo:
        raise RegraNegocioError(f"{campo.replace('_', ' ').capitalize()} deve possuir pelo menos {minimo} caracteres")
    return valor


def inteiro_positivo(dados, campo):
    try:
        valor = int(dados.get(campo))
    except (TypeError, ValueError):
        raise RegraNegocioError(f"{campo.replace('_', ' ').capitalize()} deve ser um número inteiro")
    if valor <= 0:
        raise RegraNegocioError(f"{campo.replace('_', ' ').capitalize()} deve ser maior que zero")
    return valor


def data_iso_obrigatoria(dados, campo):
    try:
        return date.fromisoformat(str(dados.get(campo, "")))
    except ValueError:
        raise RegraNegocioError(f"{campo.replace('_', ' ').capitalize()} deve estar no formato AAAA-MM-DD")
