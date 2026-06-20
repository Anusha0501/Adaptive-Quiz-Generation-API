"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-20
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "quizzes",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("topic", sa.String(255), nullable=False),
        sa.Column("difficulty", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_quizzes_topic", "quizzes", ["topic"])
    op.create_index("ix_quizzes_difficulty", "quizzes", ["difficulty"])
    op.create_table(
        "questions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("quiz_id", sa.Uuid(), sa.ForeignKey("quizzes.id"), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("bloom_level", sa.String(32), nullable=False),
        sa.Column("difficulty_score", sa.Float(), nullable=False),
        sa.Column("validation_score", sa.Float(), nullable=False),
    )
    op.create_index("ix_questions_quiz_id", "questions", ["quiz_id"])
    op.create_index("ix_questions_bloom_level", "questions", ["bloom_level"])
    op.create_table(
        "attempts",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("quiz_id", sa.Uuid(), sa.ForeignKey("quizzes.id"), nullable=False),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("answers", sa.JSON(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_attempts_quiz_id", "attempts", ["quiz_id"])
    op.create_table(
        "analytics",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("quiz_id", sa.Uuid(), sa.ForeignKey("quizzes.id"), unique=True, nullable=False),
        sa.Column("generation_ms", sa.Integer(), nullable=False),
        sa.Column("duplicate_regenerations", sa.Integer(), nullable=False),
        sa.Column("average_validation_score", sa.Float(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("analytics")
    op.drop_table("attempts")
    op.drop_table("questions")
    op.drop_table("quizzes")
    op.drop_table("users")
