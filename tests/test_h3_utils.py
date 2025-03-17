# TODO....

from app.const import CENTER_LAT, CENTER_LON, H3_LEVEL, RADIUS_KM
from app.utils import generate_hexagons
from typing import Tuple


CENTER: Tuple[float, float] = (CENTER_LAT, CENTER_LON)


def test_generate_hexagons():
    hexagons = generate_hexagons(CENTRE, RADIUS_KM, H3_LEVEL)
    assert len(hexagons) > 0
    assert h3.h3_get_resolution(hexagons[0][0])
    assert h3.h3_get_resolution(hexagons[0][0]) == H3_LEVEL
    assert h3.h3_to_geo(hexagons[0][0])[0] == CENTER_LAT    
    assert h3.h3_to_geo(hexagons[0][0])[1]  
    assert h3.h3_to_geo(hexagons[0][0])[2]  
    assert h3.h3_get_resolution(hexagons[0][0]) 
    
