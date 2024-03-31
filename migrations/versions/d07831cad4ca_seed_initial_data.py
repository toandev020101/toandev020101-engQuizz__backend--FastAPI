"""Seed initial data

Revision ID: d07831cad4ca
Revises: 86038a232d0e
Create Date: 2024-03-31 16:59:02.477859

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from app.core import get_settings
from app.utils import hash_password, to_date

settings = get_settings()

# revision identifiers, used by Alembic.
revision: str = 'd07831cad4ca'
down_revision: Union[str, None] = '86038a232d0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute(
        sa.text(
            "INSERT INTO users (fullname, email, password, birth_day, is_verified, is_admin) VALUES "
            "(:fullname, :email, :password, :birth_day, :is_verified, :is_admin)"
        ).bindparams(
            fullname=settings.ADMIN_FULLNAME,
            email=settings.ADMIN_EMAIL,
            password=hash_password(settings.ADMIN_PASSWORD),
            birth_day=to_date("2002-01-02"),
            is_verified=True,
            is_admin=True
        )
    )


def downgrade() -> None:
    pass
