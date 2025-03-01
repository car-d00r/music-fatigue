"""init

Revision ID: a5b17d8d705d
Revises: 
Create Date: 2025-02-27 23:19:00.948548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5b17d8d705d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:

    op.execute("""
    CREATE TABLE users (
        user_id VARCHAR NOT NULL,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP NOT NULL,
        PRIMARY KEY (user_id)
    );
    """)

    op.execute("""
    CREATE TABLE user_tournaments (
        user_id VARCHAR NOT NULL,
        tournament_id VARCHAR NOT NULL,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP NOT NULL,
        PRIMARY KEY (user_id, tournament_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    op.execute("""
    CREATE TABLE tournaments (
        tournament_id VARCHAR,
        round_id INTEGER NOT NULL,
        tournament_type VARCHAR NOT NULL,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP NOT NULL,
        PRIMARY KEY (tournament_id, round_id),
        FOREIGN KEY (tournament_id) REFERENCES users(user_id)
    );
    """)

    op.execute("""
    CREATE TABLE round_submissions (
        tournament_id VARCHAR NOT NULL,
        round_id INTEGER NOT NULL,
        user_id VARCHAR NOT NULL,
        submission VARCHAR NOT NULL,
        created_at TIMESTAMP NOT NULL,
        PRIMARY KEY (tournament_id, round_id, user_id, submission),
        FOREIGN KEY (tournament_id, round_id) REFERENCES tournaments(tournament_id, round_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    op.execute("""
    CREATE TABLE round_votes_updown (
        tournament_id VARCHAR NOT NULL,
        round_id INTEGER NOT NULL,
        user_id VARCHAR NOT NULL,
        submission VARCHAR NOT NULL,
        vote INTEGER NOT NULL,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP NOT NULL,
        PRIMARY KEY (tournament_id, round_id, user_id, submission),
        FOREIGN KEY (tournament_id, round_id, user_id, submission) REFERENCES round_submissions(tournament_id, round_id, user_id, submission)
    );
    """)

    op.execute("""
    CREATE TABLE round_votes_ranked (
        tournament_id VARCHAR NOT NULL,
        round_id INTEGER NOT NULL,
        user_id VARCHAR NOT NULL,
        submission VARCHAR NOT NULL,
        rank INTEGER NOT NULL,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP NOT NULL,
        PRIMARY KEY (tournament_id, round_id, user_id, submission),
        FOREIGN KEY (tournament_id, round_id, user_id, submission) REFERENCES round_submissions(tournament_id, round_id, user_id, submission)
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE round_votes_ranked;")
    op.execute("DROP TABLE round_votes_updown;")
    op.execute("DROP TABLE round_submissions;")
    op.execute("DROP TABLE tournaments;")
    op.execute("DROP TABLE user_tournaments;")
    op.execute("DROP TABLE users;")
