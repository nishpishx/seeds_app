from flask import Flask, jsonify
import math
import json

app = Flask(__name__)

# ---- GEOJSON GENERATION FUNCTION ----
def generate_geojson():
    subpolygons = [
        {"name": "polygon_1", "lat_base": 48.3371},
    ]

    lon_base = -122.55259
    delta_lat = 0.000045
    delta_lon = 0.000135
    clusters_per_row = 70
    clusters_per_col = 4

    seed_grid_size = 5
    seed_spacing = 1  # meters
    m_to_deg_lat = 1 / 111320
    m_to_deg_lon = 1 / (111320 * math.cos(math.radians(34.702696)))

    features = []

    # ---- SEED POINTS ----
    for subpoly in subpolygons:
        lat_start = subpoly["lat_base"]
        cluster_id = 1

        for i in range(clusters_per_col):
            lat_center = lat_start + i * delta_lat

            for j in range(clusters_per_row):
                lon_center = lon_base + j * delta_lon

                offset = (seed_grid_size - 1) / 2 * seed_spacing

                for row in range(seed_grid_size):
                    for col in range(seed_grid_size):

                        dlat = (row * seed_spacing - offset) * m_to_deg_lat
                        dlon = (col * seed_spacing - offset) * m_to_deg_lon

                        seed_lat = lat_center + dlat
                        seed_lon = lon_center + dlon

                        seed_id = row * seed_grid_size + col + 1

                        features.append({
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [seed_lon, seed_lat]
                            },
                            "properties": {
                                "cluster_id": cluster_id,
                                "seed_id": seed_id
                            }
                        })

                cluster_id += 1

    # ---- GRID BOUNDARY POLYGON ----
    total_width = delta_lon * clusters_per_row
    total_height = delta_lat * len(subpolygons)

    lat_min = subpolygons[0]["lat_base"]
    lon_min = lon_base
    lat_max = lat_min + total_height
    lon_max = lon_min + total_width

    rectangle_coords = [
        [lon_min, lat_min],
        [lon_min, lat_max],
        [lon_max, lat_max],
        [lon_max, lat_min],
        [lon_min, lat_min],
    ]

    features.append({
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [rectangle_coords]
        },
        "properties": {"name": "Grid Boundary"}
    })

    return {
        "type": "FeatureCollection",
        "features": features
    }


# ---- FLASK ROUTE ----
@app.route("/seeds.geojson")
def seeds_geojson():
    return jsonify(generate_geojson())


# ---- RUN ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




