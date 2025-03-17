import h3
import h3.api.basic_str as h3_api_str
import h3.api.basic_int as h3_api_int

from app.core.types import (
    Coord, HexagonData, HexagonList,
    Resolution, BboxRequest
)

from app.utils.h3_utils import (
    generate_hexagons, included_hexagons,
    save_to_kmz, save_hexagons_to_zip,
    write_hexagons_to_zip, included_hexagons_in_box, make_point_list
)

hex_dataset = generate_hexagons(
    center = Coord(56.0,38.0),
    radius = 7,
    resolution = 12
)

# write_hexagons_to_zip(hex_dataset)

hex_coords = h3.cell_to_latlng("8c11aa6483607ff")
hex_coords = Coord(*hex_coords)


points = make_point_list(
    "55.999, 37.999,55.999, 38.001,56.001, 38.001,56.001, 37.999,55.999, 37.999"
)
hex_list = included_hexagons_in_box(
        points = points,
        hex_dataset=hex_dataset
)

child_hex = "8c11aa6483607ff"
resolution = h3_api_str.get_resolution(child_hex)
print(resolution)  # Выведет 12

resolution = int(child_hex[1], 16)  # Для индекса вида '8cX...'
print(resolution)  # 12

parent_hex = h3_api_str.cell_to_parent(child_hex)
print(parent_hex)  # "8b11aa648360fff"

kml_data = included_hexagons(parent_hex, hex_dataset)
print(kml_data)

save_to_kmz(kml_data["kmz_data"])
