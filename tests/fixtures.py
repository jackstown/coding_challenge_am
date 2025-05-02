import json
from importlib.abc import Traversable
from importlib.resources import as_file
from unittest import TestCase

import respx
from httpx import codes


class TestFixture(TestCase):
    @classmethod
    def create_ok_route(cls, method='GET', headers=None, _json=None, text=None, **kwargs):
        return cls.create_route(
            method=method,
            response_status_code=codes.OK,
            response_headers=headers,
            response_json=_json,
            response_text=text,
            **kwargs
        )

    @classmethod
    def create_route(
        cls,
        response_status_code,
        method='GET',
        response_headers=None,
        response_json=None,
        response_text=None,
        **kwargs
    ):
        return respx.route(
            method=method,
            **kwargs
        ).mock(
            return_value=Response(
                headers=response_headers,
                status_code=response_status_code,
                json=response_json,
                text=response_text,
            )
        )

    @classmethod
    def create_bad_request_route(cls, **kwargs):
        return cls.create_route(response_status_code=codes.BAD_REQUEST, **kwargs)

    @classmethod
    def get_resource_json(cls, *descendants: str, path: Traversable):
        source = path.joinpath(*descendants)
        with as_file(source) as file_text:
            return json.loads(file_text.read_text(encoding='utf-8'))
