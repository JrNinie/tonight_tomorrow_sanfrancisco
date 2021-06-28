from exceptions.errors import InputError
from models.movie import Movie


def search_movie_or_location_by_keyword(resource, keywords):
    # Transfrom keywords
    # ex: from "boy_blue" to ["boy","blue"]
    keywords = keywords.split("_")

    if resource.upper() == "MOVIE":
        # Get all corresponding movies' title with id
        movies_title_with_id = Movie().get_all_movies_contain(*keywords)
        return {"movies": movies_title_with_id}

    elif resource.upper() == "LOCATION":
        # Get all corresponding locations with related movie's id
        locations_with_id = Movie().get_all_locations_contain(*keywords)
        # Group id by location
        result = {}
        for id, location in sorted(locations_with_id.items()):
            result.setdefault(location, []).append(id)
        return {"locations": result}

    else:
        raise InputError(f"Search about '{resource}' not allowed,\
 you can only search 'movie' or 'location'")
