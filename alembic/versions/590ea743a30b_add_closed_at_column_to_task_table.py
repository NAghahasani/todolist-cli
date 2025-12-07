from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql # Keep this import if it was auto-generated

# revision identifiers, used by Alembic.
revision: str = '590ea743a30b'
down_revision: Union[str, Sequence[str], None] = '2aebc6b696dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Adds closed_at column to tasks table."""
    op.add_column('tasks', sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Downgrade schema: Drops closed_at column from tasks table."""
    op.drop_column('tasks', 'closed_at')