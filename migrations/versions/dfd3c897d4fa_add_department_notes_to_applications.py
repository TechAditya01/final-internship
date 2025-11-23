"""Add department_notes to applications

Revision ID: dfd3c897d4fa
Revises: 
Create Date: 2025-11-23 23:11:32.532822
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'dfd3c897d4fa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('department_notes', sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.drop_column('department_notes')
