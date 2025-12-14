"""Initial migration: create user and task tables

Revision ID: 001
Revises: None
Create Date: 2025-12-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Create user and task tables with indexes."""
    # Create user table
    op.create_table(
        "user",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    # Create index on email for quick lookups
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)

    # Create task table
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("priority", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # Create indexes on task table
    op.create_index(op.f("ix_task_user_id"), "task", ["user_id"])
    op.create_index(op.f("ix_task_title"), "task", ["title"])
    op.create_index(op.f("ix_task_status"), "task", ["status"])
    op.create_index(op.f("ix_task_created_at"), "task", ["created_at"])
    # Create composite index for efficient user task filtering
    op.create_index("ix_task_user_status", "task", ["user_id", "status"])


def downgrade() -> None:
    """Downgrade schema - Drop task and user tables."""
    # Drop composite index
    op.drop_index("ix_task_user_status", table_name="task")
    # Drop task indexes
    op.drop_index(op.f("ix_task_created_at"), table_name="task")
    op.drop_index(op.f("ix_task_status"), table_name="task")
    op.drop_index(op.f("ix_task_title"), table_name="task")
    op.drop_index(op.f("ix_task_user_id"), table_name="task")
    # Drop task table
    op.drop_table("task")
    # Drop user indexes
    op.drop_index(op.f("ix_user_email"), table_name="user")
    # Drop user table
    op.drop_table("user")
