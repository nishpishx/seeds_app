from flask import Flask, request, jsonify
from seed_generator import generate_path_csv
import json
import os
from datetime import datetime
app = Flask(__name__)

# --------------------------
# Generate mission with plant spacing
# --------------------------
@app.route("/seeds.geojson", methods=["POST"])
def generate_mission():
    print("hello")
    data = request.get_json()
    print(data)
   
    angle = data.get('angle', 0)

    coords = data['polygon']['coordinates'][0]
    perimeter = [(x, y) for x, y in coords]
    print(perimeter)
   
    
    result = generate_path_csv(perimeter, angle)
    os.makedirs("missions", exist_ok=True)
    filename = f"missions/mission_{datetime.utcnow().isoformat()}.json"

    with open(filename, "w") as f:
        json.dump(result, f, indent=2)
    print("Result:", result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

