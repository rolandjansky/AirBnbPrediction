from dataclasses import dataclass

import pandas as pd
from math import sin, cos, sqrt, atan2, radians

from property import Property


@dataclass
class Location:
    latitude: float
    longitude: float
    tolerance: float = 0.0


PRICE_TOLERANCE = 0.1
LOCATION_TOLERANCE = 1.0
GRID_GRANULARITY = 10


def get_dist_between_coordinates(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    r = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return r * c


def filter_by_dist(row: pd.Series, lat2: float, lon2: float, max_dist: float) -> bool:
    if (
        get_dist_between_coordinates(row["latitude"], row["longitude"], lat2, lon2)
        < max_dist
    ):
        return True
    else:
        return False


def df_of_properties_in_proximity(
    df: pd.DataFrame, location: Location, inverse_selection: bool = False
) -> pd.DataFrame:
    if inverse_selection:
        filtered_df = df[
            ~df.apply(
                filter_by_dist,
                args=(location.latitude, location.longitude, location.tolerance),
                axis=1,
            )
        ]
    else:
        filtered_df = df[
            df.apply(
                filter_by_dist,
                args=(location.latitude, location.longitude, location.tolerance),
                axis=1,
            )
        ]
    return filtered_df


def df_matching_properties(
    df: pd.DataFrame, property: Property, price_tolerance: float
) -> pd.DataFrame:
    filtered_df = df[
        (df.price <= property.price * (1.0 + price_tolerance))
        & (df.price >= property.price * (1.0 - price_tolerance))
        & (df.room_type == property.room_type)
        & (df.accommodates == property.accommodates)
        & (df.bedrooms == property.bedrooms)
    ]
    return filtered_df


def score_for_coordinates(location: Location, df: pd.DataFrame) -> float:
    num_properties_in_proximity = len(df_of_properties_in_proximity(df, location))
    num_properties_outside_proximity = len(
        df_of_properties_in_proximity(df, location, inverse_selection=True)
    )
    return num_properties_in_proximity / (
        num_properties_outside_proximity + num_properties_in_proximity
    )


def get_most_likely_location(
    df: pd.DataFrame, property: Property
) -> ((float, float), float):
    df_filtered_by_properties = df_matching_properties(
        df, property, price_tolerance=PRICE_TOLERANCE
    )
    print(
        "Considering properties exactly matching room_type, accommodates, and bedrooms."
    )
    print(
        "Price of the property can be within "
        + str(PRICE_TOLERANCE * 100)
        + "% of the given price."
    )

    max_lon = df_filtered_by_properties.longitude.max()
    min_lon = df_filtered_by_properties.longitude.min()
    diff_lon = max_lon - min_lon
    max_lat = df_filtered_by_properties.latitude.max()
    min_lat = df_filtered_by_properties.latitude.min()
    diff_lat = max_lat - min_lat
    steps = GRID_GRANULARITY
    print(
        "Scanning locations with a longitude in the range of "
        + str(min_lon)
        + "-"
        + str(max_lon)
        + " and with "
        + str(steps)
        + " steps of size "
        + str(diff_lon / steps)
    )
    print(
        "Scanning locations with a latitude in the range of "
        + str(min_lat)
        + "-"
        + str(max_lat)
        + " and with "
        + str(steps)
        + " steps of size "
        + str(diff_lat / steps)
    )

    coordinates_to_scan = {}
    for step_lon in range(0, steps + 1):
        this_lon = min_lon + step_lon * diff_lon / steps
        for step_lat in range(0, steps + 1):
            this_lat = min_lat + step_lat * diff_lat / steps
            this_loc = Location(
                longitude=this_lon, latitude=this_lat, tolerance=LOCATION_TOLERANCE
            )
            coordinates_to_scan[
                (this_loc.latitude, this_loc.longitude)
            ] = score_for_coordinates(this_loc, df_filtered_by_properties)
    max_key = max(coordinates_to_scan, key=coordinates_to_scan.get)
    return max_key, coordinates_to_scan[max_key]
