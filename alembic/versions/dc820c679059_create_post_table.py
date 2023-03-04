"""Create post table

Revision ID: dc820c679059
Revises: 
Create Date: 2023-03-04 12:21:59.191737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc820c679059'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", 
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
