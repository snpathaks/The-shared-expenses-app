from enum import StrEnum
from typing import TypeVar


EnumType = TypeVar("EnumType", bound=StrEnum)


def enum_values(enum_cls: type[EnumType]) -> list[str]:
    return [member.value for member in enum_cls]


class MembershipRole(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class ExpenseStatus(StrEnum):
    ACTIVE = "active"
    VOIDED = "voided"


class SettlementStatus(StrEnum):
    ACTIVE = "active"
    VOIDED = "voided"


class SplitType(StrEnum):
    EQUAL = "equal"
    EXACT = "exact"
    PERCENTAGE = "percentage"
    SHARES = "shares"


class ImportStatus(StrEnum):
    STAGED = "staged"
    REVIEW_REQUIRED = "review_required"
    APPROVED = "approved"
    PARTIALLY_APPROVED = "partially_approved"
    REJECTED = "rejected"
    FAILED = "failed"


class ImportRowParseStatus(StrEnum):
    PARSED = "parsed"
    PARSE_ERROR = "parse_error"


class ImportRowDecision(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPROVED_WITH_RESOLUTION = "approved_with_resolution"


class AnomalySeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AnomalyStatus(StrEnum):
    OPEN = "open"
    APPROVED = "approved"
    REJECTED = "rejected"
    RESOLVED = "resolved"
    IGNORED = "ignored"
