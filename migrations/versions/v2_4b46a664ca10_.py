"""empty message

Revision ID: 4b46a664ca10
Revises: c2d5cf332178
Create Date: 2024-08-08 19:07:42.137813

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4b46a664ca10"
down_revision: Union[str, None] = "c2d5cf332178"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user", sa.Column("hashed_password", sa.String(length=1024), nullable=False))
    op.add_column("user", sa.Column("is_active", sa.Boolean(), nullable=False))
    op.add_column("user", sa.Column("is_superuser", sa.Boolean(), nullable=False))
    op.add_column("user", sa.Column("is_verified", sa.Boolean(), nullable=False))
    op.alter_column("user", "email", existing_type=sa.VARCHAR(length=30), type_=sa.String(length=320),
                    existing_nullable=False)
    op.drop_constraint("user_email_key", "user", type_="unique")
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.drop_column("user", "password")


def downgrade() -> None:
    op.add_column("user", sa.Column("password", sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.create_unique_constraint("user_email_key", "user", ["email"])
    op.alter_column("user", "email", existing_type=sa.String(length=320), type_=sa.VARCHAR(length=30),
                    existing_nullable=False)
    op.drop_column("user", "is_verified")
    op.drop_column("user", "is_superuser")
    op.drop_column("user", "is_active")
    op.drop_column("user", "hashed_password")
