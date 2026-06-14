class ServiceError(ValueError):
    """Base class for user-safe service errors."""


class ValidationError(ServiceError):
    """Raised when a business rule fails."""


class ApprovalRequiredError(ServiceError):
    """Raised when an operation would mutate reviewed finance data without approval."""

