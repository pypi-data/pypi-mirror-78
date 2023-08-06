from logging import getLogger

from mappa_api.models.mappa import Login

from .mappa_service import MAPPAService
from .test_escotista_service import EscotistaService


class ExportService:

    def __init__(self, mappa_service: MAPPAService):
        self._svc: EscotistaService = EscotistaService(mappa_service)
        self._log = getLogger(__name__)

    def get_progressoes_equipe(self, login: Login, cod_secao: int):
        self._svc.get_marcacoes(login, cod_secao)
