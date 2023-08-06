from .mappa_service import MAPPAService

from logging import getLogger

from mappa_api.models import Progressao, Especialidade, Login
from mappa_api.models.enums import Ramo
from typing import List


class KBService:

    LOG = getLogger(__name__)

    def __init__(self, mappa_service: MAPPAService):
        self._mappa = mappa_service
        self._http = mappa_service._http

    def get_progressoes(self, login: Login,
                        ramo: Ramo = Ramo.Todos) -> List[Progressao]:
        """ Retorna todas as progressões disponíveis """
        if not self._mappa._set_auth(login):
            return
        if ramo is Ramo.Alcateia:
            caminhos = [1, 2, 3]
        elif ramo is Ramo.TropaEscoteira:
            caminhos = [4, 5, 6]
        elif ramo is Ramo.TropaSenior:
            caminhos = [11, 12]
        elif ramo is Ramo.ClaPioneiro:
            caminhos = [15, 16]
        else:
            caminhos = [1, 2, 3, 4, 5, 6, 11, 12,
                        13, 14, 15, 16, 17, 18, 19, 20]
        filter = {"filter":
                  {"where": {
                      "numeroGrupo": None,
                      "codigoRegiao": None,
                      "codigoCaminho": {
                          "inq": caminhos}
                  }}}
        response = self._http.get(
            '/api/progressao-atividades', params=filter)
        progressoes = []
        if response.is_ok:
            try:
                for prg in response.content:
                    progressoes.append(Progressao(**prg))
            except Exception as exc:
                self.LOG.error('EXCEPTION PARSING PROGRESSOES %s : %s',
                               response.content, str(exc))

        return progressoes

    def get_especialidades(self, login: Login) -> List[Especialidade]:
        """ Retorna todas as especialidades disponíveis """
        if not self._mappa._set_auth(login):
            return
        filter = {
            "filter[include]": "itens"
        }
        response = self._http.get(
            '/api/especialidades', params=filter, description='Especialidades')
        especialidades = []
        if response.is_ok:
            try:
                for esp in response.content:
                    especialidades.append(Especialidade(**esp))
            except Exception as exc:
                self.LOG.error('EXCEPTION PARSING ESPECIALIDADES %s : %s',
                               response.content, str(exc))

        return especialidades
