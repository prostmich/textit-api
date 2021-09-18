class APIError(Exception):
    pass


class NetworkError(APIError):
    pass


class BadRequest(APIError):
    pass


class NotFound(APIError):
    pass


class Conflict(APIError):
    pass


class Unauthorized(APIError):
    pass


class ToLongText(ValueError):
    pass


class ALotOfWords(ValueError):
    pass


class NegativeNumber(ValueError):
    pass
