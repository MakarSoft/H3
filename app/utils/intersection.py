from concurrent.futures import ThreadPoolExecutor
import numpy as np
from typing import List

from app.core import HexagonData, HexagonList

# Эксперементы с разными способами нахождения пересечения
# двух коллекций из за проблем с производительностью....


# ==========================================================
# filter_hexagons_with_set
# ==========================================================
def filter_hexagons_with_set(
    hexagons: List[str],
    hex_dataset: HexagonList
) -> HexagonList:
    """
    Фильтрует hex_dataset с использованием множества для быстрого поиска.
    """
    
    hexagons_set = set(hexagons)
    included_hexagons = [
        hexagon for hexagon in hex_dataset
        if hexagon.h3_index in hexagons_set
    ]

    return included_hexagons


# ==========================================================
# filter_hexagons_with_dict
# ==========================================================
def filter_hexagons_with_dict(
    hexagons: List[str],
    hex_dataset: HexagonList
) -> HexagonList:
    """
    Фильтрует hex_dataset с использованием словаря для быстрого доступа.
    """
    # Создаем словарь для быстрого доступа к hex_dataset
    hex_dataset_dict = {hexagon.h3_index: hexagon for hexagon in hex_dataset}

    # Преобразуем hexagons в множество
    hexagons_set = set(hexagons)

    # Фильтруем hex_dataset
    included_hexagons = [
        hex_dataset_dict[h3_index] for h3_index in hexagons_set
        if h3_index in hex_dataset_dict
    ]
    
    return included_hexagons

# ==========================================================
# filter_hexagons_with_numpy
# ==========================================================
def filter_hexagons_with_numpy(
    hexagons: List[str],
    hex_dataset: HexagonList
) -> HexagonList:
    """
    Фильтрует hex_dataset с использованием NumPy для векторизации.
    """
    
    # Преобразуем hexagons в массив NumPy
    hexagons_array = np.array(hexagons)

    # Преобразуем hex_dataset в массив NumPy
    hex_dataset_array = np.array([hexagon.h3_index for hexagon in hex_dataset])

    # Находим пересечение
    included_indices = np.isin(hex_dataset_array, hexagons_array)

    # Фильтруем hex_dataset
    included_hexagons = [
        hex_dataset[i] for i, include in enumerate(included_indices)
        if include
    ]
    
    return included_hexagons

# ==========================================================
# filter_hexagons_parallel
# ==========================================================
def filter_hexagons_parallel(
    hexagons: List[str],
    hex_dataset: HexagonList,
    num_threads: int = 8
) -> HexagonList:
    """
    Фильтрует hex_dataset с использованием параллельной обработки.
    """
    
    # Преобразуем hexagons в множество
    hexagons_set = set(hexagons)

    # Функция для обработки части данных
    def process_chunk(chunk):
        return [
            hexagon for hexagon in chunk
            if hexagon.h3_index in hexagons_set
        ]

    # Разделяем hex_dataset на части
    chunk_size = len(hex_dataset) // num_threads
    chunks = [
        hex_dataset[i:i + chunk_size]
        for i in range(0, len(hex_dataset), chunk_size)
    ]

    # Обрабатываем части параллельно
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = executor.map(process_chunk, chunks)

    # Объединяем результаты
    included_hexagons = [
        hexagon
        for chunk_result in results
        for hexagon in chunk_result
    ]
    
    return included_hexagons
