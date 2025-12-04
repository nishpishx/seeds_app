import fields2cover as f2c
from shapely.geometry import Polygon, mapping, LineString, Point
import math

def generate_seed_coords(base_lat, base_lon, width, length, row_spacing=2.0, plant_spacing=0.5):
    """
    Generate coverage path in lat/lon with plant waypoints.

    Returns GeoJSON with LineString path and waypoints for each plant.
    """
    # 1. Local rectangular polygon
    coords = [(0,0), (width,0), (width,length), (0,length), (0,0)]
    poly = Polygon(coords)

    # 2. Fields2Cover polygon & coverage path
    points = [f2c.geometry.Point(x, y) for x,y in poly.exterior.coords]
    f2c_poly = f2c.geometry.Polygon(points)
    farm = f2c.fields.Farm(f2c_poly)
    field = farm.fields[0]

    swaths = f2c.swaths.generate_swaths(field, row_spacing)
    path = f2c.paths.generate_coverage_path(swaths)
    coords_path = [(p.x, p.y) for p in path.get_points()]

    # 3. Convert local meters → lat/lon
    lat_origin = base_lat
    lon_origin = base_lon
    path_latlon = []
    for x, y in coords_path:
        delta_lat = y / 111320
        delta_lon = x / (40075000 * math.cos(math.radians(lat_origin)) / 360)
        path_latlon.append((lon_origin + delta_lon, lat_origin + delta_lat))

    # 4. Create LineString
    line = LineString(path_latlon)

    # 5. Generate waypoints along path
    total_length = line.length
    num_plants = max(1, math.floor(total_length / plant_spacing))
    waypoints = []

    for i in range(num_plants):
        fraction = i / max(1, num_plants - 1)  # evenly spaced
        point = line.interpolate(fraction * total_length)
        prop = {"label": ""}
        if i == 0:
            prop["label"] = "START"
        elif i == num_plants - 1:
            prop["label"] = "END"
        waypoints.append({
            "type": "Feature",
            "geometry": mapping(point),
            "properties": prop
        })

    # 6. Return GeoJSON FeatureCollection
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
        ] + waypoints  # add all plant points
    }
    return mission_geojson


