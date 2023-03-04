"""Add content column to the posts table

Revision ID: d9f28b7698eb
Revises: dc820c679059
Create Date: 2023-03-04 12:30:26.885802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9f28b7698eb'
down_revision = 'dc820c679059'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
