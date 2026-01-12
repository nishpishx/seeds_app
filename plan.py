from flask import Flask, request, jsonify
from seed_generator import generate_path_csv
import json
import os
from datetime import datetime
import psycopg2
from psycopg2.extras import Json
import uuid

app = Flask(__name__)


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


def save_path_to_db(angle, path_geojson, sector_id=None):
    """Save path to database"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    try:
        # Insert path into database using ST_GeomFromGeoJSON
        cur.execute("""
            INSERT INTO paths (sector_id, angle_deg, geom)
            VALUES (%s, %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326))
            RETURNING id;
        """, (
            sector_id,
            angle,
            json.dumps(path_geojson)
        ))
        
        
        conn.commit()
        
        return 00
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


# --------------------------
# Generate mission with plant spacing
# --------------------------
@app.route("/seeds.geojson", methods=["POST"])
def generate_mission():
    
    print("hello")
    data = request.get_json()
    print(data)
   
    angle = data.get('angle', 0)
    deploy = data.get('deploy', False)  # Get deploy boolean  # Optional sector_id

    coords = data['polygon']['coordinates'][0]
    perimeter = [(x, y) for x, y in coords]
    print(perimeter)
   
    
    result = generate_path_csv(perimeter, angle)
    print("Result:", result)
    
    try:
        db_result = db_test()
        print("DB connected, SELECT 1 returned:", db_result)
        
        # If deploy is true, save to database
        if deploy:
            path_id = save_path_to_db(angle, result.get('path'), 1)
            print(f"Path saved to database with ID: {path_id}")
            
            result['deployed'] = True

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)