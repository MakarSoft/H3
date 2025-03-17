from pydantic import BaseModel
from typing import List, NamedTuple, Literal, Tuple


Resolution = Literal[
    0, 1, 2, 3, 4,
    5, 6, 7, 8, 9,
    10, 11, 12,
    13, 14, 15
]


# координата (широта, долгота)
class Coord(NamedTuple):
    lat: float
    lng: float

# Тип для данных одного гексагона
class HexagonData(NamedTuple):
    h3_index: str
    level: int
    cell_id: int


class HexResponse(BaseModel):
    kmz_data: bytes


class BboxRequest(BaseModel):
    border: List[Coord]  # [(lng1,lat1), (lng2,lat2), ... (lngN,latN)]


# Тип для списка гексагонов
HexagonList = List[HexagonData]


# Тип для результата эндпоинта /avg
AvgResult = List[Tuple[int, float]]

