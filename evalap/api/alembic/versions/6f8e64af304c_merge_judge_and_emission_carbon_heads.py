"""merge judge and emission_carbon heads

Revision ID: 6f8e64af304c
Revises: 0f62332b614f, e2e82a623408
Create Date: 2025-08-04 15:17:06.343797

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "6f8e64af304c"
down_revision: Union[str, None] = ("0f62332b614f", "e2e82a623408")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
