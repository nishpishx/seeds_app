"""
Script to insert a study site into the database
"""
import psycopg2
import json
import uuid
from datetime import datetime

DB_CONFIG = {
    "dbname": "pathdb",
    "user": "nisha",
    "password": "iamtheadmin",
    "host": "localhost",
    "port": 5432
}

def insert_study_site(site_name, longitude=None, latitude=None, description=None):
    """
    Insert a study site into the database
    
    Args:
        site_name: Name of the study site
        longitude: Longitude of the site location (optional)
        latitude: Latitude of the site location (optional)
        description: Description of the study site (optional)
    
    Returns:
        site_id: UUID of the inserted study site, or None if failed
    """
    
    print("Connecting to database...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    try:
        print(f"Inserting study site: {site_name}")
        if longitude is not None and latitude is not None:
            print(f"Location: ({longitude}, {latitude})")
        
        # Generate UUID for the site
        site_id = str(uuid.uuid4())
        
        if longitude is not None and latitude is not None:
            # Insert with Point geometry
            cur.execute("""
                INSERT INTO study_sites (id, name, location, description)
                VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s)
                RETURNING id, created_at;
            """, (
                site_id,
                site_name,
                longitude,
                latitude,
                description
            ))
        else:
            # Insert without location
            cur.execute("""
                INSERT INTO study_sites (id, name, description)
                VALUES (%s, %s, %s)
                RETURNING id, created_at;
            """, (
                site_id,
                site_name,
                description
            ))
        
        returned_id, created_at = cur.fetchone()
        conn.commit()
        
        print(f"✓ Success! Study site inserted with ID: {returned_id}")
        print(f"✓ Created at: {created_at}")
        
        # Verify by reading it back
        print("\nVerifying inserted data...")
        cur.execute("""
            SELECT 
                id, 
                name, 
                ST_AsGeoJSON(location) as geometry,
                description,
                created_at
            FROM study_sites 
            WHERE id = %s;
        """, (returned_id,))
        
        row = cur.fetchone()
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        if row[2]:
            print(f"Location: {json.dumps(json.loads(row[2]), indent=2)}")
        else:
            print(f"Location: None")
        print(f"Description: {row[3]}")
        print(f"Created: {row[4]}")
        
        return returned_id
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        cur.close()
        conn.close()
        print("\nDatabase connection closed.")

def test_insert_study_site():
    """Test inserting a study site with a location point"""
    
    site_name = "Maury River Study Site"
    longitude = -79.4428
    latitude = 37.7840
    description = "Primary research site on the Maury River"
    
    insert_study_site(site_name, longitude, latitude, description)

def test_insert_study_site_no_location():
    """Test inserting a study site without a location"""
    
    site_name = "Mobile Research Area"
    description = "Study site without fixed location"
    
    insert_study_site(site_name, None, None, description)

if __name__ == "__main__":
    print("=== Test 1: Insert study site with location ===")
    test_insert_study_site()
    
    print("\n" + "="*50)
    print("=== Test 2: Insert study site without location ===")
    test_insert_study_site_no_location()