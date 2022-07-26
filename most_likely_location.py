import pandas as pd
import glob

from location import get_most_likely_location
from property import Property

FILE_LOCATION = "berlin"
CURRENT_DATE = "2017-04-01"
PRICE = 136
ROOM_TYPE = "Entire home/apt"
ACCOMMODATES = 5.0
BEDROOMS = 1.0
PROPERTY = Property(
    price=PRICE, room_type=ROOM_TYPE, accommodates=ACCOMMODATES, bedrooms=BEDROOMS
)


def read_files(location: str) -> pd.DataFrame:
    all_files = glob.glob(location + "/*.csv")
    return pd.concat((pd.read_csv(f) for f in all_files), axis=0, ignore_index=True)


def filter_relevant_data(df: pd.DataFrame, current_date: str) -> pd.DataFrame:
    df["last_modified"] = pd.to_datetime(df["last_modified"])
    df_before_datetime = df[df.last_modified <= current_date]
    df_of_latest_entries = (
        df_before_datetime.sort_values("last_modified").groupby("room_id").tail(1)
    )
    return df_of_latest_entries


if __name__ == "__main__":
    df = read_files(FILE_LOCATION)
    relevant_df = filter_relevant_data(df, CURRENT_DATE)
    coordinates, probability = get_most_likely_location(df, PROPERTY)
    print(
        "Bob is staying at "
        + str(coordinates)
        + " with a probability of "
        + str(probability)
        + "."
    )
