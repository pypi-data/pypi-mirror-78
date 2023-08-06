from logging import getLogger
from typing import List

from mappa_api.models import (Associado, Conquistas, Escotista, Grupo, Imagem,
                              Login, Marcacoes, Secao, Subsecao, UserInfo)

from .mappa_service import MAPPAService


class EscotistaService:

    LOG = getLogger(__name__)

    def __init__(self, mappa_service: MAPPAService):
        self._mappa = mappa_service
        self._http = mappa_service._http

    def get_escotista(self, login: Login) -> Escotista:
        if not self._mappa._set_auth(login):
            return
        response = self._http.get(
            f'/api/escotistas/{login.userId}', 'Escotista')
        if response.is_ok:
            try:
                escotista = Escotista(**response.content)
                return escotista
            except Exception as exc:
                self.LOG.error(
                    'ERROR PARSING ESCOTISTA MODEL: %s - %s',
                    response.content, str(exc))

    def get_associado(self, login: Login, cod_associado: int) -> Associado:
        if not self._mappa._set_auth(login):
            return
        response = self._http.get(
            f"/api/associados/{cod_associado}", 'Associado')

        if response.is_ok:
            try:
                associado = Associado(**response.content)
                return associado
            except Exception as exc:
                self.LOG.error('ERROR PARSING ASSOCIADO MODEL: %s - %s',
                               response.content, str(exc))

    def get_grupo(self, login: Login,
                  cod_grupo: int, cod_regiao: str) -> Grupo:
        if not self._mappa._set_auth(login):
            return
        filter = {"filter": {
            "where": {
                "codigo": cod_grupo,
                "codigoRegiao": cod_regiao
            }
        }}
        response = self._http.get('/api/grupos',
                                  params=filter,
                                  description='Grupo')
        grupo = None
        if response.is_ok:
            try:
                for item_grupo in response.content:
                    grupo = Grupo(**item_grupo)
                    return grupo
            except Exception as exc:
                self.LOG.error('ERROR PARSING GRUPO MODEL: %s - %s',
                               response.content, str(exc))

    def get_user_info(self, login: Login) -> UserInfo:
        if not self._mappa._set_auth(login):
            return
        escotista = self.get_escotista(login)
        if not escotista:
            return None

        associado = self.get_associado(login, escotista.codigoAssociado)
        if not associado:
            return None

        grupo = self.get_grupo(
            login, escotista.codigoGrupo, escotista.codigoRegiao)
        if not grupo:
            return None

        user_info = {
            "id": escotista.codigo,
            "username": escotista.username,
            "codigoAssociado": escotista.codigoAssociado,
            "numeroDigito": associado.numeroDigito,
            "nomeCompleto": escotista.nomeCompleto,
            "nomeAbreviado": associado.nomeAbreviado,
            "dataNascimento": associado.dataNascimento,
            "sexo": associado.sexo,
            "ativo": escotista.ativo == 'S',
            "dataValidade": associado.dataValidade,
            "codigoGrupo": escotista.codigoGrupo,
            "codigoRegiao": escotista.codigoRegiao,
            "nomeGrupo": grupo.nome,
            "codigoModalidade": grupo.codigoModalidade,
            "autorizacao": login.id,
            "autorizacaoValidade": login.created.timestamp() + login.ttl
        }
        try:
            return UserInfo(**user_info)
        except Exception as exc:
            self.LOG.error("ERROR CREATING USER_INFO: %s - %s",
                           user_info, str(exc))

    def get_secoes(self, login: Login) -> List[Secao]:
        if not self._mappa._set_auth(login):
            return
        response = self._http.get(f'/api/escotistas/{login.userId}/secoes')

        secoes = []
        if response.is_ok:
            try:
                for secao in response.content:
                    secoes.append(Secao(**secao))
            except Exception as exc:
                self.LOG.error('ERROR PARSING SECOES %s - %s',
                               response.content, str(exc))

        return secoes

    def get_equipe(self, login: Login, cod_secao: int) -> List[Subsecao]:
        if not self._mappa._set_auth(login):
            return
        filter = {"filter": {"include": "associados"}}
        response = self._http.get('/api/escotistas/{0}/secoes/{1}/equipes'.
                                  format(login.userId, cod_secao),
                                  params=filter)
        equipe = []
        if response.is_ok:
            try:
                for ss in response.content:
                    equipe.append(Subsecao(**ss))
            except Exception as exc:
                self.LOG.error('ERROR PARSING EQUIPE %s - %s',
                               response.content, str(exc))

        return equipe

    def get_marcacoes(self, login: Login, cod_secao: int) -> Marcacoes:
        url = '/api/marcacoes/v2/updates?dataHoraUltimaAtualizacao='\
            '{0}&codigoSecao={1}'.format(
                "1970-01-01T00:00:00.000Z",
                cod_secao)

        response = self._http.get(
            url, description="Marcações", max_age=86400)

        if response.is_ok:
            try:
                marcacoes = Marcacoes(**response.content)
                return marcacoes
            except Exception as exc:
                self.LOG.error('ERROR PARSING MARCACOES %s - %s',
                               response.content, str(exc))

    def get_conquistas(self, login: Login, cod_secao: int) -> Conquistas:
        escotista = self.get_escotista(login)
        if not escotista:
            return None
        url = '/api/associado-conquistas/v2/updates?dataHoraUltimaAtualizacao='\
            '{0}&codigoSecao={1}&codigoEscotista={2}'.format(
                '2000-09-05T15:04:59-00:00',
                cod_secao,
                escotista.codigo)

        response = self._http.get(
            url, description="Conquistas", max_age=86400)

        if response.is_ok:
            try:
                conquistas = Conquistas(**response.content)
                return conquistas
            except Exception as exc:
                self.LOG.error('ERROR PARSING CONQUISTAS %s - %s',
                               response.content, str(exc))

    def get_imagem(self, login: Login, cod_imagem: int) -> Imagem:
        url = '/api/imagens/{0}'.format(cod_imagem)
        response = self._http.get(
            url, description="Imagem")

        if response.is_ok:
            try:
                imagem = Imagem(**response.content)
                return imagem
            except Exception as exc:
                self.LOG.error('ERROR PARSING IMAGE %s - %s',
                               response.content, str(exc))
