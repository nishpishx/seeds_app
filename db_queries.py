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
    
    # Get all study sites
    cur.execute("""
        SELECT id, name, ST_X(location) AS lon, ST_Y(location) AS lat
        FROM study_sites
        ORDER BY created_at DESC
    """)
    sites = cur.fetchall()
    
    # Build dict of sites
    result = []
    for site in sites:
        site_id, name, lon, lat = site
        result.append({
            "id": str(site_id),
            "name": name,
            "lon": lon,
            "lat": lat,
            "sectors": []
        })
    
    # Get all sectors
    cur.execute("""
        SELECT id, study_site_id, name, ST_AsGeoJSON(polygon) AS polygon
        FROM sectors
        ORDER BY created_at DESC
    """)
    sectors = cur.fetchall()
    
    # Map sectors to study sites
    site_map = {s["id"]: s for s in result}
    for sector in sectors:
        sec_id, site_id, name, polygon = sector
        site_map[str(site_id)]["sectors"].append({
            "id": str(sec_id),
            "name": name,
            "polygon": json.loads(polygon)
        })
    
    cur.close()
    conn.close()
    
    return result


