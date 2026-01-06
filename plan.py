from flask import Flask, request, jsonify
from seed_generator import generate_path_csv
import json
import os
from datetime import datetime
import psycopg2

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
    print("Result:", result)
    
    try:
        db_result = db_test()
        print("DB connected, SELECT 1 returned:", db_result)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


DB_CONFIG = {
    "dbname": "pathdb",
    "user": "nisha",
    "password": "iamtheadmin",
    "host": "localhost",
    "port": 5432
    }


def db_test():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0]
