class RegraNegocioError(Exception):
    status_code = 400


class RecursoNaoEncontradoError(RegraNegocioError):
    status_code = 404


class ConflitoError(RegraNegocioError):
    status_code = 409
