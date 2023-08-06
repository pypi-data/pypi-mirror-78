import json
import requests
from endpoints.exceptions import HttpMethodIsNotSupported
from endpoints.methods import (
        GET,
        POST,
        PUT,
        PATCH,
        DELETE,
    )


class Endpoint(object):

    domain = None
    path = None
    headers = None
    query_params = None
    methods = []

    def __init__(self, credential=None, *args, **kwargs):
        self.credential = credential
        self.path_params = kwargs or {}

    def get_path(self):
        self.path = self.path.format(**self.path_params)

    def get_url(self):
        if self.domain[-1] == '/' and self.path[0] == '/':
            domain = self.domain[:-1]
        elif self.domain[-1] != '/' and self.path[0] != '/':
            domain = self.domain + '/'
        else:
            domain = self.domain
        return f'{domain}{self.path}'

    def get_headers(self, extra=None):
        ret = {}
        if self.credential:
            ret.update(self.credential.get_headers())
        ret.update(self.headers or {})
        ret.update(extra or {})
        return ret

    def get_query_params(self, extra=None):
        ret = {}
        if self.credential:
            ret.update(self.credential.get_query_params())
        ret.update(self.query_params or {})
        ret.update(extra or {})
        return ret

    def request(self, method, headers=None, query_params=None, data=None,
                json_data=None):
        if method not in self.methods:
            raise HttpMethodIsNotSupported(method, self.methods)

        headers = self.get_headers(headers)
        params = self.get_query_params(query_params)
        url = self.get_url()
        if not data and json_data:
            data = json.dumps(json_data)

        fn = getattr(requests, method)
        if data:
            resp = fn(url=url, headers=headers, params=params, data=data)
        else:
            resp = fn(url=url, headers=headers, params=params)

        return resp

    def get(self, headers=None, query_params=None, data=None, json_data=None):
        return self.request(GET, headers, query_params, data, json_data)

    def post(self, headers=None, query_params=None, data=None, json_data=None):
        return self.request(POST, headers, query_params, data, json_data)

    def put(self, headers=None, query_params=None, data=None, json_data=None):
        return self.request(PUT, headers, query_params, data, json_data)

    def patch(self, headers=None, query_params=None, data=None, json_data=None):
        return self.request(PATCH, headers, query_params, data, json_data)

    def delete(
            self, headers=None, query_params=None, data=None, json_data=None):
        return self.request(DELETE, headers, query_params, data, json_data)
