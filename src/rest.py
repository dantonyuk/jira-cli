import requests
import logging
from urllib.parse import urljoin

from propdict import PropDict


def enable_debug():
    import http.client as http_client

    http_client.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


class RestClient(object):

    def __init__(self, endpoint, auth):
        self.endpoint = endpoint
        self.auth = auth

    def get(self, req, **kwargs):
        return self._act('get', req, **kwargs)

    def put(self, req, **kwargs):
        return self._act('put', req, **kwargs)

    def post(self, req, **kwargs):
        return self._act('post', req, **kwargs)

    def delete(self, req, **kwargs):
        return self._act('delete', req, **kwargs)

    def _act(self, method, req, **kwargs):
        url = urljoin(self.endpoint, req)
        call = getattr(requests, method)
        return RestResponse(call(url, auth=self.auth, **kwargs))


class RestResponse(object):
    def __init__(self, response):
        self.response = response

    result = property(lambda self: PropDict(self.response.json()))
    status = property(lambda self: ResponseStatus(self.response.status_code, self.response.reason))


class ResponseStatus(object):
    def __init__(self, code, reason):
        self.code = code
        self.reason = reason
