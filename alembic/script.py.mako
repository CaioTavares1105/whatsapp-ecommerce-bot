# ===========================================================
# alembic/script.py.mako - Template para novas migrations
# ===========================================================
# Este é o template usado quando rodamos:
# alembic revision -m "descrição"
#
# Mako é uma engine de templates Python.
# As variáveis ${variable} são substituídas pelo Alembic.
# ===========================================================
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """
    Aplica as mudanças no banco de dados.
    
    Este método é executado quando rodamos:
    alembic upgrade head
    """
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """
    Reverte as mudanças no banco de dados.
    
    Este método é executado quando rodamos:
    alembic downgrade -1
    """
    ${downgrades if downgrades else "pass"}
