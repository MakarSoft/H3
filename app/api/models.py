from pydantic import BaseModel
from typing import List, Tuple


class HexResponse(BaseModel):
    kmz_data: bytes  # Данные KMZ-файла


class BboxRequest(BaseModel):
    border: List[Tuple[float, float]]  # Границы в формате [[lon1,lat1], ...]


class AvgResponseItem(BaseModel):
    h3_index: str    # H3-индекс агрегированного гекса
    resolution: int  # Запрошенный уровень детализации
    cell_id: int     # Идентификатор ячейки
    median_level: float  # Медианное значение level
