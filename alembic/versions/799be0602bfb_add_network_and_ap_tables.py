"""add_network_and_AP_tables

Revision ID: 799be0602bfb
Revises: 71c3f5e5c075
Create Date: 2024-06-11 15:15:32.307450

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "799be0602bfb"
down_revision: Union[str, None] = "71c3f5e5c075"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "access_points",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("device_id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "networks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("ssid", sa.String(), nullable=True),
        sa.Column("country_code", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "ap_network_connectors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("acess_point_id", sa.Integer(), nullable=False),
        sa.Column("network_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["acess_point_id"],
            ["access_points.id"],
        ),
        sa.ForeignKeyConstraint(
            ["network_id"],
            ["networks.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ap_network_connectors")
    op.drop_table("networks")
    op.drop_table("access_points")
    # ### end Alembic commands ###
