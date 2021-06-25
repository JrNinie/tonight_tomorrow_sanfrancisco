from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db


class User(db.Model):
    """Data model for user accounts

    Args:
        db (db): db object created in models/__init__.py
    """

    __tablename__ = "t_user"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    mail = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    is_activated = db.Column(db.Boolean, nullable=False)
    liked_movie_id = db.Column(db.ARRAY(UUID))

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
