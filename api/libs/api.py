from __future__ import absolute_import
from flask import make_response, current_app
from flask_restful import Api
from flask_restful.utils import PY3
from json import dumps


def custom_output_json(data, code, headers=None):
    settings = current_app.config.get('RESTFUL_JSON', {})
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)
    _extra_data = headers.pop('_extra_data', None)
    if 200 <= code < 300:
        custom_data = {'data': data}
    else:
        custom_data = data
    if _extra_data:
        custom_data.update(_extra_data)
    if headers:
        custom_data.update(headers)

    print(custom_data, ' <------ this is return data')

    dumped = dumps(custom_data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


class CustomApi(Api):
    def __init__(self, *args, **kwargs):
        super(CustomApi, self).__init__(*args, **kwargs)
        self.representations = {
            'application/json': custom_output_json,
        }
