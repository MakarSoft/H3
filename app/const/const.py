from typing import Final
from app.core.types import Coord, Resolution

# Константы для генерации H3-гексагонов
CENTER_LAT: Final[float] = 56.0    # Широта центра области
CENTER_LNG: Final[float] = 38.0    # Долгота центра области
CENTER: Final[Coord] = Coord(CENTER_LAT, CENTER_LNG)

RADIUS: Final[int] = 7             # Радиус области в километрах
H3_LEVEL: Final[Resolution] = 12   # Уровень детализации H3

# Константы для генерации данных
LEVEL_MIN: Final[int] = -120       # Минимальное значение level
LEVEL_MAX: Final[int] = -47        # Максимальное значение level
CELL_ID_MIN: Final[int] = 1        # Минимальное значение cell_id
CELL_ID_MAX: Final[int] = 100      # Максимальное значение cell_id
