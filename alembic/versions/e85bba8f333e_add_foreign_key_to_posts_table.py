"""Add foreign key to posts table

Revision ID: e85bba8f333e
Revises: af5a5c7a7a61
Create Date: 2023-03-04 16:15:10.994201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e85bba8f333e'
down_revision = 'af5a5c7a7a61'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", 
                          source_table="posts", 
                          referent_table="users", 
                          local_cols=["owner_id"], 
                          remote_cols=["id"], 
                          ondelete="CASCADE"
                          )
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
