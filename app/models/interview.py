from datetime import datetime

from ..extensions import db


class Interview(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    resume_id = db.Column(
        db.Integer,
        db.ForeignKey("resume.id"),
        nullable=True
    )

    questions_json = db.Column(
        db.Text,
        nullable=False,
        default="[]"
    )

    answers_json = db.Column(
        db.Text,
        nullable=False,
        default="[]"
    )

    score = db.Column(
        db.Float,
        default=0
    )

    feedback = db.Column(
        db.Text,
        default=""
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )