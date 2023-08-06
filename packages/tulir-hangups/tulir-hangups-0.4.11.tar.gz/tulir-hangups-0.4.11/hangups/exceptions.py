"""Exceptions used by hangups."""

from typing import List, Dict


class HangupsError(Exception):
    """An ambiguous error occurred."""
    pass


class NetworkError(HangupsError):
    """A network error occurred."""
    pass


class HangoutsErrorPart(HangupsError):
    """Part of a Hangouts error response."""

    def __init__(self, message: str, **kwargs: str) -> None:
        super().__init__(message)
        self.data = kwargs
        self.data["message"] = message


class HangoutsError(HangupsError):
    """Hangouts returned an error response."""

    def __init__(self, message: str, code: int = None, status: str = None,
                 errors: List[Dict[str, str]] = None, **kwargs: str) -> None:
        super().__init__(message)
        self.code = code
        self.status = status
        self.message = message
        self.errors = [HangoutsErrorPart(**part) for part in errors] if errors else []
        self.extra_data = kwargs
