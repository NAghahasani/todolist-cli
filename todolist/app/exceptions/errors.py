class AppError(Exception):
    """Base exception for all application-specific errors."""
    pass


class ValidationError(AppError):
    """Raised when input validation fails."""

    @staticmethod
    def is_blank(value: str) -> bool:
        """Return True if the given string is empty or contains only whitespace."""
        return not value or not value.strip()


class ProjectNotFoundError(AppError):
    """Raised when a requested project ID is not found."""
    pass


class TaskNotFoundError(AppError):
    """Raised when a requested task ID is not found."""
    pass


class DuplicateNameError(AppError):
    """Raised when attempting to create an entity (Project) with a name that already exists."""
    pass


class MaxLimitExceededError(AppError):
    """Raised when the maximum allowed number of entities (Project/Task) is exceeded."""
    pass