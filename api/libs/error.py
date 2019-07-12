from webargs.flaskparser import (parser, abort)

from api.libs.interface_tips import InterfaceTips


@parser.error_handler
def handler_request_parsing_error(e):
    if hasattr(e, 'kwargs') and e.kwargs.get('error_info'):
        error(e.kwargs.get('error_info'), errors=e.messages)
    error(errors=e.messages)


def error(error_info=InterfaceTips.INVALID_REQUEST, errors=None):
    http_code, error_code, error_msg = error_info.value
    params = {
        'message': error_msg,
        'errcode': error_code,
    }
    if errors:
        params['errors'] = errors

    abort(http_code, **params)
