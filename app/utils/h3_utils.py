import h3
import h3.api.basic_str as h3_api
import io
import logging
import math
import numpy as np
import simplekml
import shutil
import zipfile

from typing import Tuple, List, Dict

from .exceptions import InvalidH3IndexError, InvalidPolygonError

from app.core.types import (
    Coord, HexagonData, HexagonList,
    Resolution, Coord, BboxRequest, AvgResult
)

from app.utils.intersection import(
    filter_hexagons_with_set,
    filter_hexagons_with_dict,
    filter_hexagons_with_numpy,
    filter_hexagons_parallel
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# ==========================================================
# radius_to_rings
# ==========================================================
def radius_to_rings(
    radius: int,    # Радиус в километрах
    resolution: Resolution
):
    """
    Переводит радиус в метрах в количество колец гексагонов.

    :param radius_km: Радиус в километрах.
    :param resolution: Разрешение гексагональной сетки (0-15).
    :return: Количество колец (целое число).
    """

    # Проверка корректности разрешения
    if not isinstance(resolution, int) or resolution not in range(0, 16):
        raise ValueError("Разрешение должно быть целым числом от 0 до 15.")

    # Получаем размер гексагона для заданного разрешения (в километрах)
    hex_edge_length = h3.average_hexagon_edge_length(resolution)

    # Вычисляем количество колец
    rings = math.ceil(radius / hex_edge_length)
        
    return rings


# ==========================================================
# generate_hexagons
# ==========================================================
def generate_hexagons(
    center: Coord,
    radius: int,
    resolution: Resolution
) -> HexagonList:
    """
    Генерирует массив гексагонов для заданной области.

    :param center: Координаты центра (широта, долгота).
    :param radius: Радиус области в километрах.
    :param resolution: Уровень детализации H3.
    :return: Список гексагонов с данными [h3_index, level, cell_id].
    """
    
    # Преобразуем координаты центра в H3 индекс
    center_hex = h3.latlng_to_cell(
        center.lat,
        center.lng,
        resolution
    )
    
    # преобразуем радиус в кол-во колец
    rings = radius_to_rings(radius, resolution)
    
    # Получаем гексагоны в радиусе
    hexagons = h3.grid_disk(center_hex, rings)
    
    # Создаем датасет с случайными level и cell_id
    hex_data: HexagonList = []

    for hex_id in hexagons:
        level = np.random.randint(-120, -47)
        cell_id = np.random.randint(1, 101)
        hex_data.append(
            HexagonData(hex_id, level, cell_id)
        )
    
    logger.info(f"Generated {len(hex_data)} hexagons")

    return hex_data


# ==========================================================
# included_hexagons
# ==========================================================
def included_hexagons(
    parent_hex: str,
    hex_dataset: HexagonList
):

    logger.info(f"Requested hexagons for parent_hex: {parent_hex}")
    
    # Проверяем, что parent_hex — это валидный H3 индекс
    if not h3.is_valid_cell(parent_hex):
        raise InvalidH3IndexError("Invalid H3 index")
    
    # Фильтруем гексагоны, входящие в parent_hex
    parent_resolution = h3_api.get_resolution(parent_hex)
    
    # filtered = [
    #     hexagon for hexagon in hex_dataset
    #     if h3.cell_to_parent(hexagon.h3_index, parent_resolution) == parent_hex
    # ]
    # # Генерируем KML
    # kml = simplekml.Kml()
    # for hexagon in filtered:
    #     polygon = h3.cell_to_boundary(hexagon.h3_index)
    #     kml.newpolygon(outerboundaryis=polygon)
    
    # Создаём KMZ-файл
    kml = simplekml.Kml()
    for hexagon in hex_dataset:
        if h3.cell_to_parent(hexagon.h3_index, parent_resolution) == parent_hex:
            logger.info(
                f"Гексагон {hexagon.h3_index} "
                f"входит в родительский гексагон {parent_hex}"
            )
            logger.info(
                f"Adding hexagon: {hexagon.h3_index}"
            )
            polygon = h3.cell_to_boundary(hexagon.h3_index)
            kml.newpolygon(name=hexagon.h3_index, outerboundaryis=polygon)
            
    kmz_data = kml.kml()
    
    logger.info(f"Generated KMZ data for parent_hex: {parent_hex}")

    return {"kmz_data": kmz_data}


# ==========================================================
# save_to_kmz
# ==========================================================
def save_to_kmz(
    kmz_data: bytes,
    kmz_filepath: str = "interview.kmz",
    zip_filename: str = "interview.kml"
) -> None:
    
    # упаковываем в KMZ
    kmz_buffer = io.BytesIO()
    with zipfile.ZipFile(kmz_buffer, 'w') as zip_file:
        zip_file.writestr(zip_filename, kmz_data)
    
    # Сохраняем буфер на диск
    kmz_buffer.seek(0)
    with open(kmz_filepath, 'wb') as f:
        shutil.copyfileobj(kmz_buffer, f)  # Копируем данные из памяти в файл
    
    # x = kmz_buffer.getvalue()
    

# ==========================================================
# save_hexagons_to_zip
# для отладки оч. медленно (много файлов)...
# ==========================================================
def save_hexagons_to_zip(
    hex_dataset: HexagonList,
    zip_path: str = "hex_dataset.zip"
) -> None:
    
    logger.info(f"Saving hexagons to zip file: {zip_path}")
    with zipfile.ZipFile(zip_path, "w") as zip_file:
        for hexagon in hex_dataset:
            hexagon_data = f"{hexagon.h3_index},{hexagon.level},{hexagon.cell_id}\n"
            zip_file.writestr(
                f"{hexagon.h3_index}.txt",
                hexagon_data.encode('utf-8')
            )
    logger.info(f"Saved hexagons to zip file: {zip_path}")


# ==========================================================
# write_hexagons_to_zip
# для отладки - в один файл...
# ==========================================================
def write_hexagons_to_zip(
    hex_dataset: HexagonList,
    zip_path: str = 'hex_dataset.zip',
    file_name='hex_dataset.txt'
):
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        text_content = '\n'.join(
            [
                f"{hexagon.h3_index},{hexagon.level},{hexagon.cell_id}"
                for hexagon in hex_dataset
            ]
        )
        # Записываем в ZIP как байты (encode в UTF-8)
        zip_file.writestr(file_name, text_content.encode('utf-8'))


# ==========================================================
# included_hexagons_in_bbox
# ==========================================================

def included_hexagons_in_box(
    points: List[Coord],
    hex_dataset: HexagonList
) -> HexagonList:
    
    try:
        # Преобразуем границы в многоугольник и находим гексагоны
        polygon = [
            (point.lat, point.lng)
            for point in points
        ]
        h3_shape = h3.LatLngPoly(polygon)
        hexagons = h3.polygon_to_cells(h3_shape, 12)

        # Множество обеспечивает поиск элемента за среднее время O(1),
        # что быстрее, чем линейный поиск в списке (O(n))
        included_hexagons = filter_hexagons_with_set(hexagons, hex_dataset)
        return included_hexagons
    
        # included_hexagons = []
        # for hexagon in hex_dataset:
        #     if hexagon.h3_index in hexagons:
        #         included_hexagons.append(hexagon)
        # return included_hexagons 

    except InvalidPolygonError as e:
        logger.error(f"Error in included_hexagons_in_box: {e}")
        return []


# ==========================================================
# ==========================================================
def make_point_list( 
    input_string: str # Строка с координатами границ ("lng1,lat1,lng2,lat2, ....")
) -> List[Coord]:
    
    items = list(map(float, input_string.split(',')))
    if len(items) % 2 != 0:
        items = items[:-1]
    
    return [Coord(*items[i:i+2]) for i in range(0, len(items), 2)]


# ==========================================================
# avg_result
# ==========================================================
def avg_result(
    resolution: int,
    hex_dataset: HexagonList
) -> AvgResult:
    
    grouped_data: Dict[int, List[int]] = {}
    for hexagon in hex_dataset:
        if h3.get_resolution(hexagon.h3_index) == resolution:
            if hexagon.cell_id not in grouped_data:
                grouped_data[hexagon.cell_id] = []
            grouped_data[hexagon.cell_id].append(hexagon.level)

    result: AvgResult = []
    for cell_id, levels in grouped_data.items():
        median_level = float(np.median(levels))
        result.append((cell_id, median_level))

    return result
