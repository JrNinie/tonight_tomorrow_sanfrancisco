from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
from . import db


class User(db.Model):
    """Data model for movies & locations

    Args:
        db (db): db object created in models/__init__.py
    """

    __tablename__ = "t_movie"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    title = db.Column(db.String(50), unique=True)
    release_year = db.Column(db.Integer)
    production_company = db.Column(db.String(255))
    distributor = db.Column(db.String(50))
    director = db.Column(db.String(255))
    writer = db.Column(db.String(255))
    actor_1 = db.Column(db.String(50))
    actor_2 = db.Column(db.String(50))
    actor_3 = db.Column(db.String(50))
    location_funfact = db.Column(JSON, nullable=False)
    movie_like_counter = db.Column(db.Integer)
    location_like_counter = db.Column(db.Integer)

    def to_dict(self, *columns_to_ignore):
        """Convert to dict
        This method allows to convert schema to dict and ignore unwanted info.

        Returns:
            dict: dict of schema's wanted info
        """
        dict_ = {}
        for key in self.__mapper__.c.keys():
            if key in columns_to_ignore:
                continue
            dict_[key] = getattr(self, key)
        return dict_
