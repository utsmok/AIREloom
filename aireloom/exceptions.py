"""Custom exception classes for the aireloom library."""


class AireloomError(Exception):
    """Base exception class for all aireloom errors."""
    pass


class AuthenticationError(AireloomError):
    """Raised when authentication fails (e.g., invalid credentials, token expired)."""
    pass


class ApiError(AireloomError):
    """Raised for non-success API responses (e.g., 4xx, 5xx status codes)."""

    def __init__(self, status_code: int, message: str = "API request failed"):
        self.status_code = status_code
        self.message = f"{message} (Status code: {status_code})"
        super().__init__(self.message)


class RateLimitError(ApiError):
    """Raised specifically for 429 Too Many Requests errors."""

    def __init__(self, message: str = "API rate limit exceeded", retry_after: int | None = None):
        super().__init__(status_code=429, message=message)
        self.retry_after = retry_after  # Optional: seconds to wait before retry


class ValidationError(AireloomError):
    """Raised for invalid input parameters or failed Pydantic validation."""
    pass