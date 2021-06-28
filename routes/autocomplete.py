from flask import Blueprint
from controllers.autocomplete import search_movie_or_location_by_keyword

autocomplete = Blueprint("autocomplete", __name__, url_prefix="/autocomplete")


@autocomplete.route("/<resource>/<keywords>", methods=["GET"])
def autocomplete_resource(resource, keywords):
    """Find all corresponding movies or locations by keywords

    Args:
        resource (string): must be "movie" or "location"
        keywords (string): if multipl keywords that must be seperated by "_" (ex: "ab_c_d")

    Returns:
        dict: response structure is different according to resource
            ex:
                {
                    "movies": {
                        "1be9b31c-32c8-4e60-a1ad-a561d7860b24": "GirlBoss",
                        "1f211831-7b93-4fc7-b691-b90c37ef4623": "The Diary of a Teenage Girl"
                    }
                }
            ex:
                {
                    "locations": {
                        "Bay Bridge": [
                            "22e86742-7750-46be-86a5-7661601f377f",
                            "2682d36a-6054-413c-9133-8cbb6cfb240b"
                        ],
                        "Golden Gate Bridge": [
                            "18f7bc16-614f-4003-ae27-87df4495f030",
                            "1a55790b-447c-4e93-a354-3d6d845d08c0"
                        ]
                    }
                }
    """

    return search_movie_or_location_by_keyword(resource, keywords)