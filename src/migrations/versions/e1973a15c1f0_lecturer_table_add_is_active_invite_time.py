"""lecturer table add is_active, invite time

Revision ID: e1973a15c1f0
Revises: 42903e4eaac7
Create Date: 2023-06-19 19:50:08.199063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e1973a15c1f0"
down_revision = "42903e4eaac7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("lecturer", sa.Column("is_active", sa.Boolean(), nullable=True))
    op.add_column(
        "lecturer", sa.Column("last_invitation_at", sa.DateTime(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("lecturer", "last_invitation_at")
    op.drop_column("lecturer", "is_active")
    # ### end Alembic commands ###
