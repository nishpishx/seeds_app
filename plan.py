from flask_cors import CORS
from flask import Flask, request, jsonify
from seed_generator import generate_seed_coords

app = Flask(__name__)
CORS(app)
# --------------------------
# Generate mission with plant spacing
# --------------------------
@app.route("/seeds.geojson", methods=["POST"])
def generate_mission():
    data = request.get_json()
    
    row_spacing = float(data.get("row_spacing", 2.0))
    plant_spacing = float(data.get("plant_spacing", 0.5))

    # Check if polygon exists
    polygon = data.get("polygon", None)

    if polygon:
        # polygon is a GeoJSON FeatureCollection
        # extract coordinates
        features = polygon.get("features", [])
        if not features:
            return jsonify({"error": "Polygon missing"}), 400
        
        coords = features[0]["geometry"]["coordinates"][0]  # outer ring
        mission_geojson = generate_seed_coords_polygon(coords, row_spacing, plant_spacing)
    else:
        # fallback: rectangle-based
        width  = float(data.get("width", 10))
        length = float(data.get("length", 10))
        lat    = float(data.get("lat", 48.3371))
        lon    = float(data.get("lon", -122.55259))
        mission_geojson = generate_seed_coords(lat, lon, width, length, row_spacing, plant_spacing)

    return jsonify(mission_geojson)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

