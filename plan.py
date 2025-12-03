from flask import Flask, jsonify, request
import math

app = Flask(__name__)

# ---- GENERATE MISSION SEEDS ----
def generate_mission_seeds(width, length, seeds, lon, lat):
    m_to_deg_lat = 1 / 111320
    m_to_deg_lon = 1 / (111320 * math.cos(math.radians(lat)))

    rows = int(math.sqrt(seeds))
    cols = int(math.ceil(seeds / rows))
    spacing_x = width / max(cols - 1, 1)
    spacing_y = length / max(rows - 1, 1)

    features = []
    for r in range(rows):
        for c in range(cols):
            if len(features) >= seeds:
                break
            seed_lat = lat + r * spacing_y * m_to_deg_lat
            seed_lon = lon + c * spacing_x * m_to_deg_lon
            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [seed_lon, seed_lat]},
                "properties": {}
            })
    return features

# ---- ROUTE: SEEDS.GEOJSON ----
@app.route("/seeds.geojson")
def seeds_geojson():
    # Get mission parameters from query string
    width  = request.args.get("width", type=float, default=10)
    length = request.args.get("length", type=float, default=10)
    seeds  = request.args.get("seeds", type=int, default=25)
    lon    = request.args.get("lon", type=float, default=-122.55259)
    lat    = request.args.get("lat", type=float, default=48.3371)

    features = generate_mission_seeds(width, length, seeds, lon, lat)

    return jsonify({
        "type": "FeatureCollection",
        "features": features
    })

# ---- RUN SERVER ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)




