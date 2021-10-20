class ApiError(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code if status_code is not None else 400
        self.payload = payload

    def __str__(self):
        return f'Message: {self.message}. Status: {self.status_code}'


class MissingParameter(ApiError):
    def __init__(self, param_name):
        ApiError.__init__(self, 'Missing parameter: ' + param_name)


class InvalidParameter(ApiError):
    def __init__(self, param_name, message):
        ApiError.__init__(self, f'Invalid parameter: {param_name}: {message}')
