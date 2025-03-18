import h3
import numpy as np
import simplekml
import logging

import io
import zipfile

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import Response

from typing import Dict, List, Tuple

from app.const import CENTER, RADIUS, H3_LEVEL
from app.utils import (
    generate_hexagons, included_hexagons, save_to_kmz,
    make_point_list, included_hexagons_in_box, avg_result,
    InvalidH3IndexError, InvalidPolygonError
)

from app.core import (
    Coord, HexagonData, HexagonList,
    AvgResult, Resolution, HexResponse,
    BboxRequest
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Генерация исходного массива гексагонов
hex_dataset: HexagonList = generate_hexagons(CENTER, RADIUS, H3_LEVEL)


router = APIRouter()

# ==========================================================
# /
# ==========================================================
@router.get("/")
async def hello():
    return {
        "message": "Hello H3"
}

# ==========================================================
# Эндпоинт /hex
# ==========================================================
@router.get("/hex")
async def get_hex(
    parent_hex: str = Header(..., alias="parent_hex")
) -> Response:
    """
    Возвращает KMZ-файл с гексагонами, входящими в заданный родительский гексагон.

    :param parent_hex: H3 индекс родительского гексагона ("8b11aa648360fff").
    :return: KMZ-файл.
    """

    logger.info(f"Received parent_hex: {parent_hex}")

    try:
        kmz_data = included_hexagons(parent_hex, hex_dataset)
        save_to_kmz(kmz_data["kmz_data"])
        print(kmz_data["kmz_data"])

        response = Response(
            content=kmz_data["kmz_data"],
            media_type="application/vnd.google-earth.kmz"
        )
    except InvalidH3IndexError as e:
        logger.error(f"Error in get_hex: {e}")
        raise HTTPException(status_code=400, detail="Invalid H3 index")

    return response


# ==========================================================
# Эндпоинт /bbox
# ==========================================================
@router.get("/bbox")
async def get_bbox(border: str = Header(...)) -> HexagonList:
    """
    Возвращает гексагоны, входящие в заданные границы.

    :param border: Строка с координатами границ (lng1,lat1,lng2,lat2).
    :return: Список гексагонов.
    """

    points = make_point_list(border)
    try:
        hex_list = included_hexagons_in_box(
            points = points,
            hex_dataset=hex_dataset
        )
    except InvalidPolygonError as e:
        logger.error(f"Error in get_bbox: {e}")
        raise HTTPException(status_code=400, detail="Invalid polygon")

    return hex_list

# ==========================================================
# Эндпоинт /avg
# ==========================================================
@router.get("/avg")
async def get_avg(resolution: int = Header(...)) -> AvgResult:
    """
    Возвращает медианные значения level для гексагонов заданного разрешения.

    :param resolution: Уровень детализации H3.
    :return: Список с медианными значениями level, сгруппированными по cell_id.
    """
    result = avg_result(resolution, hex_dataset)

    return result
