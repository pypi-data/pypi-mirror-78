import json
from datetime import timedelta
from logging import getLogger

from cache_gs import CacheGS

from mappa_api.models import Login

from .http_service import HTTPService


class MAPPAService:

    LOG = getLogger(__name__)
    CACHE_SECTION = 'mappa'

    def __init__(self, cache_string_connection: str = 'path://.cache',
                 http_service=None):
        if isinstance(cache_string_connection, CacheGS):
            self._cache = cache_string_connection
        else:
            self._cache = CacheGS(cache_string_connection)
        self._http = http_service or HTTPService(self._cache)
        self._login: Login = None

    def login(self, username, password) -> Login:
        login = self._get_login_from_cache(username, password)
        if not login:
            login = self._get_login_from_mappa(username, password)

        if login:
            self._login = login
            return login

    def _get_login_from_cache(self, username, password) -> Login:
        cache_login = self._cache.get_value(
            self.CACHE_SECTION, 'login_'+username, None)
        if not cache_login:
            return None
        if isinstance(cache_login, str):
            try:
                cache_login = json.loads(cache_login)
            except Exception as exc:
                self.LOG.warning('BAD VALUE FOR CACHE: %s - %s',
                                 cache_login, str(exc))
                self._cache.delete_value(self.CACHE_SECTION, 'login_'+username)
                return None

        try:
            cache_login = Login(**cache_login)
            if cache_login.is_valid:
                self.LOG.info('LOGIN FROM CACHE: %s %s',
                              cache_login.user_id, cache_login.id)
                return cache_login
            self.LOG.info('EXPIRED LOGIN FROM CACHE: %s %s',
                          cache_login.user_id, cache_login.id)
            self._cache.delete_value(self.CACHE_SECTION, 'login_'+username)
        except Exception as exc:
            self.LOG.warning('ERROR GETTING LOGIN FROM CACHE: %s', str(exc))

    def _get_login_from_mappa(self, username, password) -> Login:
        response = self._http.post(url='/api/escotistas/login',
                                   params={"type": "LOGIN_REQUEST",
                                           "username": username,
                                           "password": password})

        if not response.is_ok:
            self.LOG.warning('login user (%s) failed', username)
            return None
        try:
            login = Login(**response.content)

            self._cache.set_value(section=self.CACHE_SECTION,
                                  key='login_'+username,
                                  value=response.content,
                                  ttl=login.ttl)
            self.LOG.info('login from mappa (%s) valid until (%s)',
                          username,
                          login.created+timedelta(seconds=login.ttl))
            return login
        except Exception as exc:
            self.LOG.error('exception on mappa login: %s', str(exc))

    def _set_auth(self, login: Login):
        if login and login.is_valid:
            self._http.set_authorization(login)
            return True
        self.LOG.warning('SETTING INVALID AUTH: %s', login)
