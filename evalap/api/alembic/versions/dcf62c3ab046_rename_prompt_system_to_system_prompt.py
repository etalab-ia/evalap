"""rename prompt_system to system_prompt

Revision ID: dcf62c3ab046
Revises: 7c02444c083d
Create Date: 2025-05-03 16:40:53.318662

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dcf62c3ab046"
down_revision: Union[str, None] = "7c02444c083d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("models", "prompt_system", new_column_name="system_prompt")


def downgrade() -> None:
    op.alter_column("models", "prompt_system", new_column_name="system_prompt")
