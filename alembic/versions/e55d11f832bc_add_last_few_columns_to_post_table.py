"""Add last few columns to post table

Revision ID: e55d11f832bc
Revises: e85bba8f333e
Create Date: 2023-03-04 16:27:41.529666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e55d11f832bc'
down_revision = 'e85bba8f333e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
