"""Add user table

Revision ID: af5a5c7a7a61
Revises: d9f28b7698eb
Create Date: 2023-03-04 12:35:20.337368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af5a5c7a7a61'
down_revision = 'd9f28b7698eb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                     sa.Column ("id", sa.Integer(), nullable = False), 
                     sa.Column("email", sa.String(), nullable = False), 
                     sa.Column ("password", sa.String(), nullable = False), 
                     sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default = sa.text("now()"), nullable = False),
                     sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("email")
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
