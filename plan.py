from flask_cors import CORS
from flask import Flask, request, jsonify
from seed_generator import generate_path_csv

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
   


    coords = data['polygon']['coordinates'][0]
    perimeter = [(x, y) for x, y in coords]
    print(perimeter)
   
    
    result = generate_path_csv(perimeter, csv_filename="path.csv")
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

