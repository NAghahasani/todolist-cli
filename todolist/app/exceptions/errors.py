class AppError(Exception):
    """Base class for application-specific errors."""
    pass


class ValidationError(AppError):
    """Raised when input validation fails."""

    NAME_MIN_LEN = 1
    NAME_MAX_LEN = 50
    DESC_MAX_LEN = 200

    @staticmethod
    def is_blank(value: str) -> bool:
        """Return True if the given string is empty or contains only whitespace."""
        return not value or not value.strip()
