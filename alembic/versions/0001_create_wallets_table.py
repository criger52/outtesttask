from alembic import op
import sqlalchemy as sa


revision = "0001_create_wallets_table"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "wallets",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("balance", sa.BigInteger, nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_table("wallets")

