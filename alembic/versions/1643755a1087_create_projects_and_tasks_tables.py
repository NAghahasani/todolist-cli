from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "1643755a1087"
down_revision: Union[str, Sequence[str], None] = "f1a96e280114"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    status_enum = postgresql.ENUM("TODO", "IN_PROGRESS", "DONE", name="status")
    status_enum.create(op.get_bind(), checkfirst=True)

    op.rename_table("commands", "tasks")

    op.add_column("projects", sa.Column("description", sa.String(length=150), nullable=True))
    op.alter_column(
        "projects",
        "name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.create_index(op.f("ix_projects_id"), "projects", ["id"], unique=False)
    op.drop_column("projects", "created_at")

    op.add_column("tasks", sa.Column("deadline", sa.DateTime(timezone=True), nullable=True))
    op.alter_column(
        "tasks",
        "title",
        existing_type=sa.VARCHAR(length=150),
        type_=sa.String(length=50),
        existing_nullable=False,
    )
    op.alter_column(
        "tasks",
        "description",
        existing_type=sa.TEXT(),
        type_=sa.String(length=255),
        existing_nullable=True,
    )
    op.execute("ALTER TABLE tasks ALTER COLUMN status TYPE status USING status::text::status")
    op.alter_column(
        "tasks",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )
    op.create_index(op.f("ix_tasks_id"), "tasks", ["id"], unique=False)
    op.drop_column("tasks", "due_date")


def downgrade() -> None:
    op.add_column("commands", sa.Column("due_date", sa.DATE(), autoincrement=False, nullable=True))
    op.drop_index(op.f("ix_tasks_id"), table_name="commands")
    op.alter_column(
        "commands",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "commands",
        "status",
        existing_type=sa.Enum("TODO", "IN_PROGRESS", "DONE", name="status"),
        type_=sa.VARCHAR(length=20),
        existing_nullable=False,
    )
    op.alter_column(
        "commands",
        "description",
        existing_type=sa.String(length=255),
        type_=sa.TEXT(),
        existing_nullable=True,
    )
    op.alter_column(
        "commands",
        "title",
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=150),
        existing_nullable=False,
    )
    op.drop_column("commands", "deadline")
    op.add_column(
        "projects",
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_index(op.f("ix_projects_id"), table_name="projects")
    op.alter_column(
        "projects",
        "name",
        existing_type=sa.String(length=30),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.drop_column("projects", "description")

    op.rename_table("tasks", "commands")

    status_enum = postgresql.ENUM("TODO", "IN_PROGRESS", "DONE", name="status")
    status_enum.drop(op.get_bind(), checkfirst=True)