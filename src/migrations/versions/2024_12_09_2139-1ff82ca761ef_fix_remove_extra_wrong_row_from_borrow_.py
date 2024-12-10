"""fix: remove extra(wrong) row from borrow table

Revision ID: 1ff82ca761ef
Revises: b6d68f616d88
Create Date: 2024-12-09 21:39:18.751133

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1ff82ca761ef"
down_revision: Union[str, None] = "b6d68f616d88"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("borrows", "return_date", existing_type=sa.DATE(), nullable=True)
    op.drop_column("borrows", "available_copies")


def downgrade() -> None:
    op.add_column(
        "borrows",
        sa.Column(
            "available_copies", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.alter_column("borrows", "return_date", existing_type=sa.DATE(), nullable=False)
