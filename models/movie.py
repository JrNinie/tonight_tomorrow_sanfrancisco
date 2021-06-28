from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy import func, any_
import uuid
from . import db
from exceptions.errors import DatabaseError, NotFoundError, InputError
from log.my_logger import get_logger
from tools.common import is_valid_uuid

logger = get_logger()


class Movie(db.Model):
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

    def get_all_movies_contain(self, *keywords):
        """Find movies if they contain keyword in title

        Args:
            keyword (string): keywords input

        Raises:
            DatabaseError: Errors occured when find movies in db

        Returns:
            dict: key is "id" (string) and value "title"
        """
        keywords_list = [("%" + keyword + "%").upper() for keyword in keywords]

        movies_title_with_id_dict = {}
        try:
            # Find all movies ("id" & "title") which contains keyword in their "title"
            # result is a list of tuple : [(UUID('1a'), 'm1'), (UUID('1b'), 'm2')]
            movies_title_with_id = Movie.query.filter(
                func.upper(Movie.title).like(
                    any_(keywords_list))).with_entities(Movie.id,
                                                        Movie.title).all()

            # Convert "id" (UUID type) to string then to dict
            movies_title_with_id_dict = dict([
                (str(id), title) for id, title in movies_title_with_id
            ])
        except Exception as e:
            logger.error(f"Errors when find movies, details: {e}")
            raise DatabaseError(f"Errors when find movies, details: {e}")
        return movies_title_with_id_dict

    # TODO find a more efficient way to do it by avoiding retrieve all locations_funfacts
    def get_all_locations_contain(self, *keywords):
        """Find locations if they contain keyword

        Args:
            keyword (string): keywords input

        Returns:
            dict: key is "id" (string) and value "location"
        """

        # Find all location_funfacts with related movies id
        try:
            locations_funfacts_with_movieid = Movie.query.with_entities(
                Movie.id, Movie.location_funfact).all()
        except Exception as e:
            logger.error(f"Errors when find locations, details: {e}")
            raise DatabaseError(f"Errors when find locations, details: {e}")

        # Convert "id" (UUID type) to string then to dict
        locations_funfacts_with_movieid_dict = dict(
            (str(id), location_funfact)
            for id, location_funfact in locations_funfacts_with_movieid)

        result = {}
        for movie_id, location_funfact in locations_funfacts_with_movieid_dict.items(
        ):
            for location in location_funfact.keys():
                for keyword in keywords:
                    if keyword.upper() in location.upper():
                        result[movie_id] = location

        return result

    def get_movie_by_id(self, id):
        """Find movie by id

        Args:
            id (string): movie id

        Raises:
            DatabaseError: Errors when find movie in db
            NotFoundError: No corresponding movie in db
            InputError: Not valid UUID input

        Returns:
            dict: All info in db about the corresponding movie
        """
        # UUID validation
        if not is_valid_uuid(id):
            logger.error(f"{id} is not valid UUID")
            raise InputError(f"{id} is not valid UUID")

        # Find movie by id
        try:
            movie = Movie.query.filter_by(id=id).first()
        except Exception as e:
            logger.error(f"Errors when find movies, details: {e}")
            raise DatabaseError(f"Errors when find movies, details: {e}")

        if not movie:
            logger.error(f"Corresponding movie not found for '{id}'")
            raise NotFoundError(
                message=f"Corresponding movie not found for '{id}'.")

        return movie.to_dict()