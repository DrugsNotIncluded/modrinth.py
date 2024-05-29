class LabrinthAPIException(Exception):
    """Base for all Labrinth API Exceptions"""

    def __init__(self, error: str) -> None:
        self.error = error

class DeprecatedAPI(LabrinthAPIException):
    """API has been deprecated and is no longer usable."""

class InvalidScope(LabrinthAPIException):
    """Invalid scope for provided token."""