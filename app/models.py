"""SQLAlchemy models."""
from datetime import datetime, timezone
from app import db


class Case(db.Model):
    """A criminal case loaded from app/cases/data.json."""
    __tablename__ = "cases"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    real_sentence = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(80), nullable=False, index=True)
    real_fine = db.Column(db.Float, nullable=False, default=0)
    real_jail = db.Column(db.Float, nullable=False, default=0)


class Vote(db.Model):
    """A user's estimate for a case."""
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey("cases.id"), nullable=False, index=True)
    fine_guess = db.Column(db.Float, nullable=False)
    jail_guess = db.Column(db.Float, nullable=False)
    timestamp = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    case = db.relationship("Case", backref=db.backref("votes", lazy=True))
