# db_queries.py
import psycopg2
import json

DB_CONFIG = {
    "dbname": "pathdb",
    "user": "nisha",
    "password": "iamtheadmin",
    "host": "localhost",
    "port": 5432
}

def get_study_sites_with_sectors():
    """Return all study sites with nested sectors"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    try:
        # Get all study sites
        cur.execute("""
            SELECT id, name, 
                   ST_X(location) AS lon, 
                   ST_Y(location) AS lat,
                   description
            FROM study_sites
            ORDER BY created_at DESC
        """)
        sites = cur.fetchall()
        
        # Build list of sites
        result = []
        site_map = {}
        
        for site in sites:
            site_id, name, lon, lat, description = site
            site_data = {
                "id": str(site_id),
                "name": name,
                "lon": lon,
                "lat": lat,
                "description": description,
                "sectors": []
            }
            result.append(site_data)
            site_map[str(site_id)] = site_data
        
        # Get all sectors
        cur.execute("""
            SELECT id, site_id, name, description, ST_AsGeoJSON(boundary) AS boundary
            FROM sectors
            ORDER BY created_at DESC
        """)
        sectors = cur.fetchall()
        
        # Map sectors to study sites
        for sector in sectors:
            sec_id, site_id, name, description, boundary = sector
            site_id_str = str(site_id)
            
            if site_id_str in site_map:
                boundary_dict = json.loads(boundary) if boundary else None
                coordinates = boundary_dict.get("coordinates") if boundary_dict else None
                print(coordinates)
                site_map[site_id_str]["sectors"].append({
                    "id": str(sec_id),
                    "name": name,
                    "description": description,
                    "boundary": boundary
                })
        
        return result
        
    except Exception as e:
        print(f"Error in get_study_sites_with_sectors: {e}")
        import traceback
        traceback.print_exc()
        raise e
    finally:
        cur.close()
        conn.close()