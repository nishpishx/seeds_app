# seed_generator.py
import fields2cover as f2c
from shapely.geometry import Polygon, mapping, LineString
import math

def generate_seed_coords(width, length, row_spacing=2.0, plant_spacing=0.5):
    """
    Generate coverage path and planting plan.

    Args:
        width (float): field width (meters)
        length (float): field length (meters)
        row_spacing (float): distance between coverage rows (meters)
        plant_spacing (float): distance between plants along a row (meters)

    Returns:
        dict: GeoJSON FeatureCollection with LineString path and planting properties
    """
    # 1. Rectangle polygon
    coords = [(0, 0), (width, 0), (width, length), (0, length), (0, 0)]
    poly = Polygon(coords)

    # 2. Fields2Cover polygon and farm
    points = [f2c.geometry.Point(x, y) for x, y in poly.exterior.coords]
    f2c_poly = f2c.geometry.Polygon(points)
    farm = f2c.fields.Farm(f2c_poly)
    field = farm.fields[0]

    # 3. Generate swaths and coverage path
    swaths = f2c.swaths.generate_swaths(field, row_spacing)
    path = f2c.paths.generate_coverage_path(swaths)

    # 4. Convert path to LineString
    coords_path = [(p.x, p.y) for p in path.get_points()]
    line = LineString(coords_path)

    # 5. Calculate number of plants
    total_length = line.length
    num_plants = max(1, math.floor(total_length / plant_spacing))

    # 6. Return GeoJSON with planting info
    mission_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": mapping(line),
                "properties": {
                    "row_spacing": row_spacing,
                    "plant_spacing": plant_spacing,
                    "num_plants": num_plants
                }
            }
        ]
    }
    return mission_geojson


