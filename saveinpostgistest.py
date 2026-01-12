#!/usr/bin/env python3
"""
Test script to insert a LineString into PostGIS paths table
"""

import psycopg2
import json
from datetime import datetime

DB_CONFIG = {
    "dbname": "pathdb",
    "user": "nisha",
    "password": "iamtheadmin",
    "host": "localhost",
    "port": 5432
}

def test_insert_path():
    """Test inserting a simple path into the database"""
    
    # Sample LineString GeoJSON
    sample_linestring = {
        "type": "LineString",
        "coordinates": [
            [-78.5, 37.2],
            [-78.51, 37.21],
            [-78.52, 37.22],
            [-78.53, 37.23],
            [-78.54, 37.24]
        ]
    }
    
    angle = 45.0
    sector_id = None  # or a valid UUID if you have one
    
    print("Connecting to database...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    try:
        print(f"Inserting path with angle: {angle}")
        print(f"LineString: {json.dumps(sample_linestring, indent=2)}")
        
        # Insert using ST_GeomFromGeoJSON into 'path' column
        cur.execute("""
            INSERT INTO paths (sector_id, angle_deg, path)
            VALUES (%s, %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326))
            RETURNING id, created_at;
        """, (
            sector_id,
            angle,
            json.dumps(sample_linestring)
        ))
        
        path_id, created_at = cur.fetchone()
        conn.commit()
        
        print(f"✓ Success! Path inserted with ID: {path_id}")
        print(f"✓ Created at: {created_at}")
        
        # Verify by reading it back
        print("\nVerifying inserted data...")
        cur.execute("""
            SELECT 
                id, 
                sector_id, 
                angle_deg, 
                ST_AsGeoJSON(path) as geometry,
                created_at
            FROM paths 
            WHERE id = %s;
        """, (path_id,))
        
        row = cur.fetchone()
        print(f"ID: {row[0]}")
        print(f"Sector ID: {row[1]}")
        print(f"Angle: {row[2]}")
        print(f"Geometry: {json.dumps(json.loads(row[3]), indent=2)}")
        print(f"Created: {row[4]}")
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()
        print("\nDatabase connection closed.")

if __name__ == "__main__":
    test_insert_path()