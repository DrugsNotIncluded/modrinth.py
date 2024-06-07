class LabrinthAPIException(Exception):
    """Base for all Labrinth API Exceptions"""

    def __init__(self, error: str) -> None:
        self.error = error

class DeprecatedAPI(LabrinthAPIException):
    """API has been deprecated and is no longer usable."""

class InvalidScope(LabrinthAPIException):
    """Invalid scope for provided token."""

class NotFound(LabrinthAPIException):
    """Not Found"""

def StatusResolver(func):
    async def result(*args, **kwargs):
        status, body = await func(*args, **kwargs)
        match status:
            case 200:
                return body
            case 204:
                return True
            case 410:
                raise DeprecatedAPI(body)
            case 404:
                raise NotFound(body)
    return result