from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# ---- FUNCTION TO GENERATE MISSION SEEDS ----
def generate_mission_seeds(width, length, seeds, lon, lat):
    print(width, length, seeds, lon, lat)
    # Convert meters to degrees
    m_to_deg_lat = 1 / 111320
    m_to_deg_lon = 1 / (111320 * math.cos(math.radians(lat)))

    # Determine rows and columns for roughly square grid
    rows = int(math.sqrt(seeds))
    cols = int(math.ceil(seeds / rows))
    spacing_x = width / max(cols - 1, 1)
    spacing_y = length / max(rows - 1, 1)

    mission_seeds = []
    for r in range(rows):
        for c in range(cols):
            if len(mission_seeds) >= seeds:
                break
            seed_lat = lat + r * spacing_y * m_to_deg_lat
            seed_lon = lon + c * spacing_x * m_to_deg_lon
            mission_seeds.append({
                "lat": seed_lat,
                "lon": seed_lon
            })
    return mission_seeds

# ---- ROUTE: /seeds.geojson ----
@app.route("/seeds.geojson", methods=["POST"])
def seeds_geojson():
    data = request.get_json()
    width  = float(data.get("width", 10))
    length = float(data.get("length", 10))
    seeds  = int(data.get("seeds", 25))
    lon    = float(data.get("lon", -122.55259))
    lat    = float(data.get("lat", 48.3371))

    mission_seeds = generate_mission_seeds(width, length, seeds, lon, lat)

    return jsonify({
        "num_seeds": len(mission_seeds),
        "seeds": mission_seeds
    })

# ---- RUN SERVER ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
