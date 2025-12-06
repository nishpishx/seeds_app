import fields2cover as f2c
from seed_generator import generate_seed_coords

# -------------------------
# Test rectangular field
# -------------------------
base_lat, base_lon = 48.3371, -122.55259
width, length = 10, 20
row_spacing = 2.0
plant_spacing = 1.0

# Generate rectangle mission
mission_rect = generate_seed_coords(base_lat, base_lon, width, length, row_spacing, plant_spacing)

# Extract F2C coordinates (meters) for visualization
coords_rect = [(pt['geometry']['coordinates'][0], pt['geometry']['coordinates'][1])
               for pt in mission_rect['features'][1:]]  # skip LineString
f2c_points_rect = [f2c.geometry.Point(x, y) for x, y in coords_rect]

# Visualize rectangle mission
f2c.visualizer.visualize_coverage_path(f2c_points_rect)


