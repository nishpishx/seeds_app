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
    print("hello")
    data = request.get_json()
    print(data)
    row_spacing = 2.0
    plant_spacing = 0.5


    
    width  = float(data.get("width", 10))
    length = float(data.get("length", 10))
    lat    = float(data.get("lat", 48.3371))
    lon    = float(data.get("lon", -122.55259))
    mission_geojson = generate_seed_coords(lat, lon, width, length, row_spacing, plant_spacing)
    print (mission_geojson)

    return jsonify(mission_geojson)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

