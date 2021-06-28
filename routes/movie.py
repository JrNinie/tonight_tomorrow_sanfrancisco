from flask import Blueprint
from controllers.movie import find_movie_by_id

movie = Blueprint("movie", __name__, url_prefix="/movies")


@movie.route("/<movie_id>", methods=["GET"])
def get_movie_by_id(movie_id):
    """Find movie by id
    It allows to get all info about corresponding movie,
    its poster and trailer
    Args:
        movie_id (string): Movie id

    Returns:
        dict: Basic info & poster & trailer about the corresponding movie
    """
    return find_movie_by_id(movie_id)
