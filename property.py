from dataclasses import dataclass


@dataclass
class Property:
    price: float
    room_type: str
    accommodates: float
    bedrooms: float
