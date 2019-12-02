from requests import Session, HTTPError

from .stacks import Stacks
from .config import BASE_URL


def check_for_errors(resp, *args, **kwargs):
    """Raises stored :class:`HTTPError`, if one occurred."""

    http_error_msg = {}
    if isinstance(resp.reason, bytes):
        # We attempt to decode utf-8 first because some servers
        # choose to localize their reason strings. If the string
        # isn't utf-8, we fall back to iso-8859-1 for all other
        # encodings. (See PR #3538)
        try:
            reason = resp.reason.decode('utf-8')
        except UnicodeDecodeError:
            reason = resp.reason.decode('iso-8859-1')
    else:
        reason = resp.reason

    try:
        response_obj = resp.json()
    except Exception:
        response_obj = {"text": resp.text}

    if 400 <= resp.status_code < 600:
        http_error_msg = {
            "status_code": resp.status_code,
            "url": resp.url,
            "reason": reason,
            "content": response_obj
        }

    if http_error_msg:
        raise HTTPError(http_error_msg, response=resp)


class OAuth2Session(Session):
    def __init__(self, clientid, apisecret, custom_hooks: list = [check_for_errors]):
        self._clientid = clientid
        self._apisecret = apisecret
        self._custom_hooks = custom_hooks
        self._token = ""

        super(OAuth2Session, self).__init__()

    def _refresh_token(self):
        response = super(OAuth2Session, self).post(
            "/identity/v1/oauth2/token",
            json={
                "grant_type": "client_credentials",
                "client_id": self._clientid,
                "client_secret": self._apisecret
            }
        )

        self._token = response.json()["access_token"]

    def _add_auth(self, kwargs):
        if not "headers" in kwargs:
            kwargs["headers"] = dict()
        kwargs["headers"]["Authorization"] = "Bearer %s" % self._token
        return kwargs

    def _add_hooks(self, kwargs):
        if not "headers" in kwargs:
            kwargs["headers"] = dict()
        if not "hooks" in kwargs["headers"]:
            kwargs["headers"]["hooks"] = dict()
        if not "response" in kwargs["headers"]["hooks"]:
            kwargs["headers"]["hooks"]["response"] = list()

        kwargs["headers"]["hooks"]["response"].append(self._custom_hooks)

        return kwargs

    def request(self, method, url, **kwargs):
        kwargs = self._add_auth(kwargs)
        kwargs = self._add_hooks(kwargs)
        response = super(OAuth2Session, self).request(method, BASE_URL + url, **kwargs)
        if response.status_code == 401:
            self._refresh_token()
            kwargs = self._add_auth(kwargs)
            kwargs = self._add_hooks(kwargs)
            response = super(OAuth2Session, self).request(method, BASE_URL + url, **kwargs)
        return response


class Stackpath(object):
    _clientid = ""
    _apisecret = ""

    client = None

    def __init__(self, clientid, apisecret, custom_hooks: list = [check_for_errors]):
        self._clientid = clientid
        self._apisecret = apisecret
        self._init_client(custom_hooks)

    def _init_client(self, custom_hooks):
        self.client = OAuth2Session(self._clientid, self._apisecret, custom_hooks=custom_hooks)

    def stacks(self):
        return Stacks(self.client)
