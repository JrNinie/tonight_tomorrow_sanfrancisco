import pandas as pd
import json


def convert_tow_columns_to_json(row):
    """Convert "locations" & "fun_facts" to one row in json

    Args:
        row: one row of a dataframe

    Returns:
        json: combination of "locations" & "fun_facts" in json format
    """
    temp_dict = dict(zip(row["locations"], row["fun_facts"]))
    return json.dumps(temp_dict)


def prepare_movie_data(filepath):
    """Data preparation
    It allows to transform raw data to desired format, steps:
        - Data preparation (delete empty row, rename colums' name etc.)
        - Delete lines where 'location' is empty
        - Modify in order that every movie takes only 1 line and /
        its related 'location'and 'fun fact' become an dict keeped /
        in a new column 'location_funfact'
        - Add columns 'movie_like_counter'

    Args:
        filepath (string): file path for raw data
    """
    # Read raw data
    dataframe = pd.read_csv(
        filepath,
        encoding="utf-8",
        keep_default_na=False,
    )

    # Reform colums' name
    dataframe.columns = dataframe.columns.str.replace(" ", "_").str.lower()

    # Delete empty lines
    dataframe = dataframe.dropna(axis=0, how="all")
    # Delete lines where "locations" is empty
    dataframe = dataframe[dataframe.locations.ne("")]
    # Reset index
    dataframe = dataframe.reset_index(drop=True)

    # Create column "location_funfact" in dict/json
    df_locations = (
        dataframe.groupby("title")["locations"]
        .apply(list)
        .reset_index(name="locations")
    )
    df_funfacts = (
        dataframe.groupby("title")["fun_facts"]
        .apply(list)
        .reset_index(name="fun_facts")
    )
    df_temp = pd.merge(df_locations, df_funfacts, on="title")
    df_temp["location_funfact"] = df_temp.apply(
        lambda row: convert_tow_columns_to_json(row), axis=1
    )
    df_temp.drop(["locations", "fun_facts"], axis=1, inplace=True)

    # Delete colums "locations" and "fun_facts" and duplicate rows
    dataframe.drop(["locations", "fun_facts"], axis=1, inplace=True)
    dataframe = dataframe.drop_duplicates(subset="title")
    dataframe = dataframe.reset_index(drop=True)

    # Merge "location_funfact" to dataframe
    new_dataframe = pd.merge(dataframe, df_temp, on="title")
    # Add "movie_like_counter"
    new_dataframe["movie_like_counter"] = 0

    new_dataframe.to_csv("./movies.csv", index=False)


def main():
    prepare_movie_data("./Film_Locations_in_San_Francisco.csv")


if __name__ == "__main__":
    main()
