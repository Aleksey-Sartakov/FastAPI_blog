"""empty message

Revision ID: f82839410c7f
Revises: 4b46a664ca10
Create Date: 2024-08-09 16:29:19.789373

"""

from typing import Sequence, Union
from pwdlib import PasswordHash

from alembic import op
import sqlalchemy as sa


from src.auth.auth_models import RoleDbModel, UserDbModel

# revision identifiers, used by Alembic.
revision: str = "f82839410c7f"
down_revision: Union[str, None] = "4b46a664ca10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	conn = op.get_bind()
	session = sa.orm.Session(bind=conn)
	admin_role = RoleDbModel(
		name="admin",
		permissions=["admin", "base"]
	)
	user_role = RoleDbModel(
		name="user",
		permissions=["base"]
	)

	session.add_all([admin_role, user_role])
	session.flush()

	password_hash = PasswordHash.recommended()
	admin_user = UserDbModel(
		first_name="admin",
		last_name="admin",
		email="root",
		role_id=admin_role.id,
		hashed_password=password_hash.hash("root"),
		is_superuser=True
	)
	session.add(admin_user)
	session.commit()


def downgrade() -> None:
	pass
