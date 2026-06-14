"""Initial shared expenses schema.

Revision ID: 20260614_0001
Revises:
Create Date: 2026-06-14
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260614_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


membership_role = sa.Enum("owner", "admin", "member", name="membership_role")
expense_status = sa.Enum("active", "voided", name="expense_status")
settlement_status = sa.Enum("active", "voided", name="settlement_status")
split_type = sa.Enum("equal", "exact", "percentage", "shares", name="split_type")
import_status = sa.Enum(
    "staged",
    "review_required",
    "approved",
    "partially_approved",
    "rejected",
    "failed",
    name="import_status",
)
import_row_parse_status = sa.Enum("parsed", "parse_error", name="import_row_parse_status")
import_row_decision = sa.Enum(
    "pending",
    "approved",
    "rejected",
    "approved_with_resolution",
    name="import_row_decision",
)
anomaly_severity = sa.Enum("info", "warning", "critical", name="anomaly_severity")
anomaly_status = sa.Enum(
    "open",
    "approved",
    "rejected",
    "resolved",
    "ignored",
    name="anomaly_status",
)


def upgrade() -> None:
    bind = op.get_bind()
    for enum_type in (
        membership_role,
        expense_status,
        settlement_status,
        split_type,
        import_status,
        import_row_parse_status,
        import_row_decision,
        anomaly_severity,
        anomaly_status,
    ):
        enum_type.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("full_name", sa.String(length=160), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("preferred_currency", sa.String(length=3), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("char_length(preferred_currency) = 3", name="ck_users_preferred_currency_len"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)

    op.create_table(
        "exchange_rates",
        sa.Column("from_currency", sa.String(length=3), nullable=False),
        sa.Column("to_currency", sa.String(length=3), nullable=False),
        sa.Column("rate", sa.Numeric(18, 8), nullable=False),
        sa.Column("effective_date", sa.Date(), nullable=False),
        sa.Column("source", sa.String(length=80), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("char_length(from_currency) = 3", name="ck_exchange_rates_from_currency_len"),
        sa.CheckConstraint("char_length(to_currency) = 3", name="ck_exchange_rates_to_currency_len"),
        sa.CheckConstraint("from_currency <> to_currency", name="ck_exchange_rates_distinct_currency"),
        sa.CheckConstraint("rate > 0", name="ck_exchange_rates_rate_positive"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "from_currency",
            "to_currency",
            "effective_date",
            "source",
            name="uq_exchange_rates_pair_date_source",
        ),
    )

    op.create_table(
        "groups",
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("base_currency", sa.String(length=3), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("char_length(base_currency) = 3", name="ck_groups_base_currency_len"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "group_memberships",
        sa.Column("group_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("role", membership_role, nullable=False),
        sa.Column("joined_at", sa.Date(), nullable=False),
        sa.Column("left_at", sa.Date(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("left_at IS NULL OR left_at > joined_at", name="ck_membership_valid_interval"),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("group_id", "user_id", "joined_at", name="uq_membership_group_user_joined"),
    )
    op.create_index(
        "ix_memberships_group_user_dates",
        "group_memberships",
        ["group_id", "user_id", "joined_at", "left_at"],
        unique=False,
    )

    op.create_table(
        "imports",
        sa.Column("group_id", sa.Uuid(), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_hash", sa.String(length=128), nullable=False),
        sa.Column("status", import_status, nullable=False),
        sa.Column("uploaded_by", sa.Uuid(), nullable=False),
        sa.Column("report", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"]),
        sa.ForeignKeyConstraint(["uploaded_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("group_id", "file_hash", name="uq_imports_group_file_hash"),
    )
    op.create_index("ix_imports_group_status", "imports", ["group_id", "status"], unique=False)

    op.create_table(
        "expenses",
        sa.Column("group_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("expense_date", sa.Date(), nullable=False),
        sa.Column("original_amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("original_currency", sa.String(length=3), nullable=False),
        sa.Column("base_amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("base_currency", sa.String(length=3), nullable=False),
        sa.Column("exchange_rate", sa.Numeric(18, 8), nullable=False),
        sa.Column("split_type", split_type, nullable=False),
        sa.Column("status", expense_status, nullable=False),
        sa.Column("import_batch_id", sa.Uuid(), nullable=True),
        sa.Column("source_row_id", sa.Uuid(), nullable=True),
        sa.Column("created_by", sa.Uuid(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("base_amount >= 0", name="ck_expenses_base_amount_non_negative"),
        sa.CheckConstraint("char_length(base_currency) = 3", name="ck_expenses_base_currency_len"),
        sa.CheckConstraint("char_length(original_currency) = 3", name="ck_expenses_original_currency_len"),
        sa.CheckConstraint("exchange_rate > 0", name="ck_expenses_exchange_rate_positive"),
        sa.CheckConstraint("original_amount >= 0", name="ck_expenses_original_amount_non_negative"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"]),
        sa.ForeignKeyConstraint(["import_batch_id"], ["imports.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_expenses_group_date", "expenses", ["group_id", "expense_date"], unique=False)
    op.create_index("ix_expenses_import_source", "expenses", ["import_batch_id", "source_row_id"], unique=False)

    op.create_table(
        "settlements",
        sa.Column("group_id", sa.Uuid(), nullable=False),
        sa.Column("paid_by", sa.Uuid(), nullable=False),
        sa.Column("paid_to", sa.Uuid(), nullable=False),
        sa.Column("settlement_date", sa.Date(), nullable=False),
        sa.Column("original_amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("original_currency", sa.String(length=3), nullable=False),
        sa.Column("base_amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("base_currency", sa.String(length=3), nullable=False),
        sa.Column("exchange_rate", sa.Numeric(18, 8), nullable=False),
        sa.Column("status", settlement_status, nullable=False),
        sa.Column("import_batch_id", sa.Uuid(), nullable=True),
        sa.Column("source_row_id", sa.Uuid(), nullable=True),
        sa.Column("created_by", sa.Uuid(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("base_amount > 0", name="ck_settlements_base_amount_positive"),
        sa.CheckConstraint("char_length(base_currency) = 3", name="ck_settlements_base_currency_len"),
        sa.CheckConstraint("char_length(original_currency) = 3", name="ck_settlements_original_currency_len"),
        sa.CheckConstraint("exchange_rate > 0", name="ck_settlements_exchange_rate_positive"),
        sa.CheckConstraint("original_amount > 0", name="ck_settlements_original_amount_positive"),
        sa.CheckConstraint("paid_by <> paid_to", name="ck_settlements_distinct_users"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"]),
        sa.ForeignKeyConstraint(["import_batch_id"], ["imports.id"]),
        sa.ForeignKeyConstraint(["paid_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["paid_to"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_settlements_group_date", "settlements", ["group_id", "settlement_date"], unique=False)
    op.create_index("ix_settlements_import_source", "settlements", ["import_batch_id", "source_row_id"], unique=False)

    op.create_table(
        "expense_payers",
        sa.Column("expense_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("base_amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.CheckConstraint("amount >= 0", name="ck_expense_payers_amount_non_negative"),
        sa.CheckConstraint("base_amount >= 0", name="ck_expense_payers_base_amount_non_negative"),
        sa.CheckConstraint("char_length(currency) = 3", name="ck_expense_payers_currency_len"),
        sa.ForeignKeyConstraint(["expense_id"], ["expenses.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_expense_payers_expense_user", "expense_payers", ["expense_id", "user_id"], unique=False)

    op.create_table(
        "expense_splits",
        sa.Column("expense_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("split_amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("base_amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("percentage", sa.Numeric(9, 6), nullable=True),
        sa.Column("shares", sa.Numeric(18, 4), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("base_amount >= 0", name="ck_expense_splits_base_amount_non_negative"),
        sa.CheckConstraint("char_length(currency) = 3", name="ck_expense_splits_currency_len"),
        sa.CheckConstraint("percentage IS NULL OR percentage >= 0", name="ck_expense_splits_percentage_non_negative"),
        sa.CheckConstraint("shares IS NULL OR shares >= 0", name="ck_expense_splits_shares_non_negative"),
        sa.CheckConstraint("split_amount >= 0", name="ck_expense_splits_amount_non_negative"),
        sa.ForeignKeyConstraint(["expense_id"], ["expenses.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_expense_splits_expense_user", "expense_splits", ["expense_id", "user_id"], unique=False)

    op.create_table(
        "import_rows",
        sa.Column("import_id", sa.Uuid(), nullable=False),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("raw_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("row_hash", sa.String(length=128), nullable=False),
        sa.Column("parse_status", import_row_parse_status, nullable=False),
        sa.Column("parse_errors", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("normalized_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_expense_id", sa.Uuid(), nullable=True),
        sa.Column("created_settlement_id", sa.Uuid(), nullable=True),
        sa.Column("decision", import_row_decision, nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["created_expense_id"], ["expenses.id"]),
        sa.ForeignKeyConstraint(["created_settlement_id"], ["settlements.id"]),
        sa.ForeignKeyConstraint(["import_id"], ["imports.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("import_id", "row_number", name="uq_import_rows_import_row_number"),
    )
    op.create_index("ix_import_rows_import_decision", "import_rows", ["import_id", "decision"], unique=False)
    op.create_index("ix_import_rows_row_hash", "import_rows", ["row_hash"], unique=False)

    op.create_foreign_key(
        "fk_expenses_source_row_id_import_rows",
        "expenses",
        "import_rows",
        ["source_row_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_settlements_source_row_id_import_rows",
        "settlements",
        "import_rows",
        ["source_row_id"],
        ["id"],
    )

    op.create_table(
        "anomalies",
        sa.Column("import_id", sa.Uuid(), nullable=True),
        sa.Column("import_row_id", sa.Uuid(), nullable=True),
        sa.Column("entity_type", sa.String(length=80), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=True),
        sa.Column("rule_code", sa.String(length=80), nullable=False),
        sa.Column("severity", anomaly_severity, nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("details", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("status", anomaly_status, nullable=False),
        sa.Column("requires_approval", sa.Boolean(), nullable=False),
        sa.Column("resolved_by", sa.Uuid(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["import_id"], ["imports.id"]),
        sa.ForeignKeyConstraint(["import_row_id"], ["import_rows.id"]),
        sa.ForeignKeyConstraint(["resolved_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_anomalies_import_status", "anomalies", ["import_id", "status"], unique=False)
    op.create_index("ix_anomalies_rule_severity", "anomalies", ["rule_code", "severity"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("actor_user_id", sa.Uuid(), nullable=True),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=True),
        sa.Column("before_state", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("after_state", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_audit_logs_actor_created", "audit_logs", ["actor_user_id", "created_at"], unique=False)
    op.create_index("ix_audit_logs_entity", "audit_logs", ["entity_type", "entity_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_audit_logs_entity", table_name="audit_logs")
    op.drop_index("ix_audit_logs_actor_created", table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index("ix_anomalies_rule_severity", table_name="anomalies")
    op.drop_index("ix_anomalies_import_status", table_name="anomalies")
    op.drop_table("anomalies")
    op.drop_constraint("fk_settlements_source_row_id_import_rows", "settlements", type_="foreignkey")
    op.drop_constraint("fk_expenses_source_row_id_import_rows", "expenses", type_="foreignkey")
    op.drop_index("ix_import_rows_row_hash", table_name="import_rows")
    op.drop_index("ix_import_rows_import_decision", table_name="import_rows")
    op.drop_table("import_rows")
    op.drop_index("ix_expense_splits_expense_user", table_name="expense_splits")
    op.drop_table("expense_splits")
    op.drop_index("ix_expense_payers_expense_user", table_name="expense_payers")
    op.drop_table("expense_payers")
    op.drop_index("ix_settlements_import_source", table_name="settlements")
    op.drop_index("ix_settlements_group_date", table_name="settlements")
    op.drop_table("settlements")
    op.drop_index("ix_expenses_import_source", table_name="expenses")
    op.drop_index("ix_expenses_group_date", table_name="expenses")
    op.drop_table("expenses")
    op.drop_index("ix_imports_group_status", table_name="imports")
    op.drop_table("imports")
    op.drop_index("ix_memberships_group_user_dates", table_name="group_memberships")
    op.drop_table("group_memberships")
    op.drop_table("groups")
    op.drop_table("exchange_rates")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    for enum_type in (
        anomaly_status,
        anomaly_severity,
        import_row_decision,
        import_row_parse_status,
        import_status,
        split_type,
        settlement_status,
        expense_status,
        membership_role,
    ):
        enum_type.drop(bind, checkfirst=True)

