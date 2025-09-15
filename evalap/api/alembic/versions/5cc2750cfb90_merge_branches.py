"""Merge branches

Revision ID: 5cc2750cfb90
Revises: a8816ddd6dfd, eee3dc59f461
Create Date: 2024-12-11 20:02:55.960060

"""

from typing import Sequence, Union



# revision identifiers, used by Alembic.
revision: str = "5cc2750cfb90"
down_revision: Union[str, None] = ("a8816ddd6dfd", "eee3dc59f461")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
