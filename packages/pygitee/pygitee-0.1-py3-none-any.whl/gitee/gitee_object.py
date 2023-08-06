import typing
from dataclasses import dataclass
from gitee.consts import *

import requests


@dataclass
class Response(object):
    ok: bool
    code: int
    data: typing.Any
    message: str


class GiteeObject(object):
    def __init__(self, access_token='', base_url=DEFAULT_BASE_URL, per_page=DEFAULT_PER_PAGE):
        self.access_token = access_token
        self.base_url = base_url
        self.per_page = per_page

    def get_url(self, url):
        return self.base_url + url

    def do_get(self, url, params: dict = None):
        if self.access_token:
            if not params:
                params = {}
            params.setdefault('access_token', self.access_token)

        resp = requests.get(self.get_url(url), params=params)
        if resp.ok:
            return Response(True, resp.status_code, resp.json(), '')
        return Response(False, resp.status_code, None, resp.text)

    def do_post(self, url, params: dict = None):
        if self.access_token:
            if not params:
                params = {}
            params.setdefault('access_token', self.access_token)

        resp = requests.post(self.get_url(url), data=params)
        if resp.ok:
            return Response(True, resp.status_code, resp.json(), '')
        return Response(False, resp.status_code, None, resp.text)

    def do_patch(self, url, params: dict = None):
        if self.access_token:
            if not params:
                params = {}
            params.setdefault('access_token', self.access_token)

        resp = requests.patch(self.get_url(url), data=params)
        if resp.ok:
            return Response(True, resp.status_code, resp.json(), '')
        return Response(False, resp.status_code, None, resp.text)

    def do_delete(self, url, params: dict = None):
        if self.access_token:
            if not params:
                params = {}
            params.setdefault('access_token', self.access_token)

        resp = requests.delete(self.get_url(url), params=params)
        if resp.ok:
            return Response(True, resp.status_code, resp.json(), '')
        return Response(False, resp.status_code, None, resp.text)
