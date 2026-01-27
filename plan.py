from flask import Flask, request, jsonify
from seed_generator import generate_path_csv
import json
import os
from datetime import datetime
import psycopg2
from psycopg2.extras import Json
import uuid
from shapely.geometry import Polygon
from db_queries import get_study_sites_with_sectors
from db_inserts import insert_study_site, insert_sector

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

def calculate_anchor(perimeter):
    """Calculate lower-left corner (anchor point) from perimeter"""
    poly = Polygon(perimeter)
    minx, miny, maxx, maxy = poly.bounds
    
    anchor = {"lon": minx, "lat": miny}
    
    print(f"Anchor point (lower-left): ({minx}, {miny})")
    
    return anchor

def save_path_to_db(angle, path_geojson, anchor, start, end, sector_id=None):
    """Save path to database with anchor, start, and end points"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    try:
        # Strip Z coordinate if present (convert 3D to 2D)
        if 'coordinates' in path_geojson:
            path_geojson_2d = {
                'type': path_geojson['type'],
                'coordinates': [[coord[0], coord[1]] for coord in path_geojson['coordinates']]
            }
        else:
            path_geojson_2d = path_geojson
        
        print("Saving 2D path:", json.dumps(path_geojson_2d))
        
        # Create anchor point geometry
        anchor_point = {
            "type": "Point",
            "coordinates": [anchor["lon"], anchor["lat"]]
        }
        
        # Create start point geometry
        start_point = None
        if start:
            start_point = {
                "type": "Point",
                "coordinates": [start["lon"], start["lat"]]
            }
        
        # Create end point geometry
        end_point = None
        if end:
            end_point = {
                "type": "Point",
                "coordinates": [end["lon"], end["lat"]]
            }
        
        # Insert path into database
        cur.execute("""
            INSERT INTO test_paths (sector_id, angle_deg, path, anchor_point, start_point, end_point)
            VALUES (%s, %s, 
                    ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326),
                    ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326),
                    ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326),
                    ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326))
            RETURNING id, created_at;
        """, (
            sector_id,
            angle,
            json.dumps(path_geojson_2d),
            json.dumps(anchor_point),
            json.dumps(start_point) if start_point else None,
            json.dumps(end_point) if end_point else None
        ))
        
        path_id, created_at = cur.fetchone()
        conn.commit()
        
        return path_id
        
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
    deploy = data.get('deploy', False)
    sector_id = None
    coords = data['polygon']['coordinates'][0]
    perimeter = [(x, y) for x, y in coords]
    print(perimeter)
    
    # Calculate anchor point (lower-left corner)
    anchor = calculate_anchor(perimeter)
    
    result = generate_path_csv(perimeter, angle)
    print("Result:", result)
    
    # Add anchor to result
    result['anchor'] = anchor
    
    try:
        db_result = db_test()
        print("DB connected, SELECT 1 returned:", db_result)
        
        # If deploy is true, save to database
        if deploy:
            print("deploy is true")
            
            # Validate path_data before saving
            path_data = result.get('path')
            if not path_data:
                raise ValueError("No path data in result")
            
            # Get start and end points from result
            start = result.get('start')
            end = result.get('end')
            
            path_id = save_path_to_db(angle, path_data, anchor, start, end, sector_id)
            print(f"Path saved to database with ID: {path_id}")
            result['path_id'] = str(path_id)
            result['deployed'] = True

    except Exception as e:
        print("ERROR:", str(e))
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    return jsonify(result)

@app.route("/study-sites-with-sectors", methods=["GET", "POST"])
def api_study_sites_with_sectors():
    """Get all study sites with sectors (GET) or create new site/sector (POST)"""

    if request.method == "GET":
        try:
            data = get_study_sites_with_sectors()
            return jsonify(data)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    elif request.method == "POST":
        try:
            data = request.get_json()

            # ---------- INSERT SECTOR ----------
            if 'site_id' in data and 'boundary' in data:
                site_id = data.get('site_id')
                name = data.get('name')
                boundary = data.get('boundary')  # GeoJSON geometry

                if not site_id or not name or not boundary:
                    return jsonify({
                        "status": "error",
                        "message": "site_id, name, and boundary are required for sector"
                    }), 400

                sector_id = insert_sector(
                    site_id=site_id,
                    sector_name=name,
                    boundary=boundary
                )

                if sector_id:
                    return jsonify({
                        "status": "success",
                        "sector_id": str(sector_id),
                        "name": name
                    })
                else:
                    return jsonify({
                        "status": "error",
                        "message": "Failed to create sector"
                    }), 500

            # ---------- INSERT SITE ----------
            site_name = data.get('name')
            longitude = data.get('longitude')
            latitude = data.get('latitude')
            description = data.get('description', '')

            if not site_name:
                return jsonify({
                    "status": "error",
                    "message": "Site name is required"
                }), 400

            site_id = insert_study_site(
                site_name,
                longitude,
                latitude,
                description
            )

            if site_id:
                return jsonify({
                    "status": "success",
                    "site_id": str(site_id),
                    "name": site_name
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "Failed to create site"
                }), 500

        except Exception as e:
            print(f"Error creating site/sector: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)