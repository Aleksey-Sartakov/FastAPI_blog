"""Added complaint table

Revision ID: 3a1bdef0928f
Revises: f82839410c7f
Create Date: 2024-09-12 22:56:22.992942

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3a1bdef0928f"
down_revision: Union[str, None] = "f82839410c7f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "complaint",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "in_processing", "rejected", "confirmed", native_enum=False
            ),
            nullable=False,
        ),
        sa.Column("date_of_creation", sa.TIMESTAMP(), nullable=False),
        sa.Column("article_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["article_id"], ["article.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("complaint")
