"""Create projects and tasks tables

Revision ID: e60cda54f31a
Revises: 1643755a1087
Create Date: 2025-12-01 00:47:52.672376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e60cda54f31a'
down_revision: Union[str, Sequence[str], None] = '1643755a1087'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass