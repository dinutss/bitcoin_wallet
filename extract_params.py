from exceptions import ApiError, InvalidParameter, MissingParameter
from flask import request


def get_string_param(name, method=None):
    value = None
    if (method is None or method == 'POST') and request.method == 'POST':
        if name in request.json:
            value = request.json[name]
    elif (method is None or method == 'GET') and request.method == 'GET':
        if name in request.args:
            value = request.args[name]
    elif method is None:
        raise ApiError('Unsupported request method')
    else:
        raise ApiError('Invalid method parameter', 500)
    if value is None:
        raise MissingParameter(name)
    return str(value)


def param_exists(name, method=None):
    if (method is None or method == 'POST') and request.method == 'POST':
        if name in request.json:
            return True
    elif (method is None or method == 'GET') and request.method == 'GET':
        if name in request.args:
            return True
    return False


def get_int_param(name):
    value = get_string_param(name)
    try:
        return int(value)
    except Exception as e:
        raise InvalidParameter(name, e)


def get_float_param(name):
    value = get_string_param(name)
    try:
        return float(value)
    except Exception as e:
        raise InvalidParameter(name, e)
