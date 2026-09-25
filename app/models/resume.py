from datetime import datetime

from ..extensions import db


class Resume(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    extracted_text = db.Column(
        db.Text,
        nullable=False
    )

    analysis_json = db.Column(
        db.Text,
        nullable=False,
        default="{}"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )