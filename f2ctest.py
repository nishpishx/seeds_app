# seed_generator.py
from fields2cover import types as f2c_types
from fields2cover import sg as f2c_sg
from fields2cover import visualizer as f2c_vis
from shapely.geometry import LineString, mapping
import math

def generate_seed_coords(base_lat, base_lon, width, length, row_spacing=2.0, plant_spacing=0.5):
    """
    Generate coverage path for a rectangular field using Fields2Cover.
    Returns GeoJSON with path and waypoints.
    """
    # 1. Define rectangle in local meters
    coords = [(0,0), (width,0), (width,length), (0,length)]
    pts = [f2c_types.Point(x, y) for x, y in coords]

    # 2. Create Field
    field = f2c_types.Field(pts)

    # 3. Generate swaths (coverage lines)
    coverage = f2c_sg.FieldCoverage(field, row_spacing=row_spacing)
    swaths = coverage.generate_swaths()

    # 4. Plan coverage path
    path_obj = f2c_sg.SwathGeneratorBase().generate_coverage_path(swaths)
    path_coords = [(p.x, p.y) for p in path_obj.get_points()]

    # 5. Convert local meters → lat/lon
    path_latlon = []
    for x, y in path_coords:
        delta_lat = y / 111320
        delta_lon = x / (40075000 * math.cos(math.radians(base_lat)) / 360)
        path_latlon.append((base_lon + delta_lon, base_lat + delta_lat))

    # 6. LineString
    line = LineString(path_latlon)

    # 7. Generate plant waypoints along path
    total_length = line.length
    num_plants = max(1, math.floor(total_length / plant_spacing))
    waypoints = []

    for i in range(num_plants):
        fraction = i / max(1, num_plants - 1)
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

    # 8. Return GeoJSON FeatureCollection
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
        ] + waypoints
    }
    return mission_geojson

# -----------------------------
# Polygon version
# -----------------------------
def generate_seed_coords_polygon(base_lat, base_lon, polygon_coords, row_spacing=2.0, plant_spacing=0.5):
    """
    Generate coverage path for an arbitrary polygon (list of [x,y] in meters).
    Returns GeoJSON with path and waypoints.
    """
    pts = [f2c_types.Point(x, y) for x, y in polygon_coords]
    field = f2c_types.Field(pts)

    coverage = f2c_sg.FieldCoverage(field, row_spacing=row_spacing)
    swaths = coverage.generate_swaths()

    path_obj = f2c_sg.SwathGeneratorBase().generate_coverage_path(swaths)
    path_coords = [(p.x, p.y) for p in path_obj.get_points()]

    path_latlon = []
    for x, y in path_coords:
        delta_lat = y / 111320
        delta_lon = x / (40075000 * math.cos(math.radians(base_lat)) / 360)
        path_latlon.append((base_lon + delta_lon, base_lat + delta_lat))

    line = LineString(path_latlon)
    total_length = line.length
    num_plants = max(1, math.floor(total_length / plant_spacing))
    waypoints = []

    for i in range(num_plants):
        fraction = i / max(1, num_plants - 1)
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
        ] + waypoints
    }
    return mission_geojson

# -----------------------------
# Optional: Visualizer test
# -----------------------------
if __name__ == "__main__":
    # Rectangle test
    mission = generate_seed_coords(48.3371, -122.55259, 10, 20)
    print("Generated rectangle mission GeoJSON with", len(mission['features']), "features")

    # Polygon test
    polygon = [(0,0),(15,0),(12,10),(0,10)]
    mission_poly = generate_seed_coords_polygon(48.3371, -122.55259, polygon)
    print("Generated polygon mission GeoJSON with", len(mission_poly['features']), "features")

    # Visualize last mission (optional)
    field_pts = [f2c_types.Point(x, y) for x, y in polygon]
    field_obj = f2c_types.Field(field_pts)
    coverage = f2c_sg.FieldCoverage(field_obj, row_spacing=2.0)
    swaths = coverage.generate_swaths()
    path_obj = f2c_sg.SwathGeneratorBase().generate_coverage_path(swaths)
    f2c_vis.Visualizer.plot_path(path_obj)
