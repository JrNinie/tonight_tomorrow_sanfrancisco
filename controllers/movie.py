from models.movie import Movie


def find_movie_by_id(movie_id):
    # Get basic info from db
    movie_info = Movie().get_movie_by_id(movie_id)

    # TODO get post & trailer from another api or scraping
    movie_info["poster"] = "https://movie_url"
    movie_info["trailer"] = "https://trailer_url"

    return movie_info
