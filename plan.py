from flask import Flask, request, jsonify
from seed_generator import generate_seed_coords

app = Flask(__name__)

# --------------------------
# Generate mission with plant spacing
# --------------------------
@app.route("/seeds.geojson", methods=["POST"])
def generate_mission():
    data = request.get_json()
    width = data.get("width", 50)
    length = data.get("length", 50)
    row_spacing = data.get("row_spacing", 2.0)
    plant_spacing = data.get("plant_spacing", 0.5)

    mission_geojson = generate_seed_coords(width, length, row_spacing, plant_spacing)
    return jsonify(mission_geojson)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

