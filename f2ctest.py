"""
Self-contained test for Fields2Cover coverage path generation and visualization.
"""

from fields2cover import Point, Polygon, Farm
from fields2cover.swaths import generate_swaths
from fields2cover.paths import generate_coverage_path
from fields2cover.visualizer import visualize_coverage_path
from shapely.geometry import LineString, mapping
import math

# ------------------------
# Helper: generate rectangle path
# ------------------------
def generate_seed_coords(base_lat, base_lon, width, length, row_spacing=2.0, plant_spacing=0.5):
    # 1. Local rectangle polygon
    coords = [(0,0), (width,0), (width,length), (0,length), (0,0)]
    poly = Polygon([Point(x, y) for x, y in coords])

    # 2. Fields2Cover coverage path
    farm = Farm(poly)
    field = farm.fields[0]
    swaths = generate_swaths(field, row_spacing)
    path = generate_coverage_path(swaths)
    coords_path = [(p.x, p.y) for p in path.get_points()]

    # 3. Convert local meters -> lat/lon
    path_latlon = []
    for x, y in coords_path:
        delta_lat = y / 111320
        delta_lon = x / (40075000 * math.cos(math.radians(base_lat)) / 360)
        path_latlon.append((base_lon + delta_lon, base_lat + delta_lat))

    # 4. LineString
    line = LineString(path_latlon)

    # 5. Waypoints along path
    total_length = line.length
    num_plants = max(1, math.floor(total_length / plant_spacing))
    waypoints = []
    for i in range(num_plants):
        fraction = i / max(1, num_plants - 1)
        point = line.interpolate(fraction * total_length)
        label = "START" if i==0 else "END" if i==num_plants-1 else ""
        waypoints.append({
            "type": "Feature",
            "geometry": mapping(point),
            "properties": {"label": label}
        })

    mission_geojson = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "geometry": mapping(line),
             "properties": {"row_spacing": row_spacing, "plant_spacing": plant_spacing, "num_plants": num_plants}}
        ] + waypoints
    }

    return coords_path, mission_geojson

# ------------------------
# Helper: generate polygon path
# ------------------------
def generate_seed_coords_polygon(latlon_list, num_plants=20):
    # Convert GPS to local meters (simple approximation)
    base_lat = latlon_list[0][0]
    base_lon = latlon_list[0][1]
    coords_m = []
    for lat, lon in latlon_list:
        x = (lon - base_lon) * (40075000 * math.cos(math.radians(base_lat)) / 360)
        y = (lat - base_lat) * 111320
        coords_m.append((x, y))

    poly = Polygon([Point(x, y) for x, y in coords_m])
    farm = Farm(poly)
    field = farm.fields[0]
    swaths = generate_swaths(field, 2.0)
    path = generate_coverage_path(swaths)
    coords_path = [(p.x, p.y) for p in path.get_points()]

    # LineString in meters (can visualize directly)
    line = LineString(coords_path)

    # Waypoints along path
    total_length = line.length
    waypoints = []
    for i in range(num_plants):
        fraction = i / max(1, num_plants-1)
        point = line.interpolate(fraction * total_length)
        label = "START" if i==0 else "END" if i==num_plants-1 else ""
        waypoints.append((point.x, point.y, label))

    return coords_path, waypoints

# ------------------------
# Main test
# ------------------------
if __name__ == "__main__":
    # Rectangular field
    print("Testing rectangular field...")
    coords_rect, mission_geojson = generate_seed_coords(48.3371, -122.55259, width=10, length=20)
    print(f"Number of waypoints: {len(mission_geojson['features'])-1}")
    visualize_coverage_path([Point(x, y) for x, y in coords_rect])

    # Polygon field
    print("Testing polygon field...")
    polygon_latlon = [
        (48.3371, -122.55259),
        (48.3371, -122.55159),
        (48.3361, -122.55179),
        (48.3365, -122.5528)
    ]
    coords_poly, waypoints_poly = generate_seed_coords_polygon(polygon_latlon)
    print(f"Number of polygon waypoints: {len(waypoints_poly)}")
    visualize_coverage_path([Point(x, y) for x, y, _ in waypoints_poly])



