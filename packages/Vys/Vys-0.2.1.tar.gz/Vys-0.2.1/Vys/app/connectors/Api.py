#! python3
import requests

from Vys.app.core import *

from Vys.app.errors import *


class CustomApi(Connect):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.endpoint = Url()
        self.endpoints = []

    def get(self, url, headers=None, params=None, data=None):
        r = self._construct(url=url, method='GET', headers=headers, params=params, data=data)
        return r

    def post(self, url, headers=None, params=None, data=None):
        r = self._construct(url=url, method='POST', headers=headers, params=params, data=data)
        return r

    def patch(self, url, headers=None, params=None, data=None):
        r = self._construct(url=url, method='PATCH', headers=headers, params=params, data=data)
        return r

    def delete(self, url, headers=None, params=None, data=None):
        r = self._construct(url=url, method='DELETE', headers=headers, params=params, data=data)
        return r

    def _construct(self, url, method, headers=None, params=None, data=None):
        self.endpoints.append(url)

        def wrapper(func):
            def inner(*a, **k):
                r = self._request(
                    method=method,
                    url=self._base_url + url,
                    headers=self._o_headers(headers),
                    params=self._o_params(params),
                    data=self._o_data(data)
                )
                func(r)
            return inner
        return wrapper

    def _request(self, method, url, headers, params, data):
        r = requests.request(method, url, headers=headers, params=params, data=data)
        return r

    def set_headers(self, k, v):
        self._headers[k] = v

    def set_params(self, k, v):
        self._params[k] = v

    def set_data(self, k, v):
        self._headers[k] = v

    def set_auth_type(self, auth_type=None, body=None, params=None, headers=None):
        if auth_type == 'token':
            self._auth_body = body

    def _o_headers(self, header):
        if header:
            new_header = self._headers
            for i in header:
                new_header[i] = header[i]
            return new_header
        return self._headers

    def _o_params(self, params):
        if params:
            new_params = self._params
            for i in params:
                new_params[i] = params[i]
            return new_params
        return self._params

    def _o_data(self, data):
        if data:
            new_data = self._data
            for i in data:
                new_data[i] = data[i]
            return new_data
        return self._data


class Url:
    pass  # TODO Fill this out or delete.
