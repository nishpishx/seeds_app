import psycopg2

def generate_seed_coords(width, length, num_seeds, base_lon, base_lat):
    # your logic here
    coords = []

    # Example placeholder:
    for i in range(num_seeds):
        lon = base_lon + 0.00001 * i
        lat = base_lat + 0.00001 * i
        coords.append((lon, lat))

    return coords


def batch_insert_seeds(seed_coords):
    conn = psycopg2.connect(
        host="localhost",
        database="geoapp",
        user="geoapp",
        password="your_secure_password"
    )

    cur = conn.cursor()

    # batch insert (fastest)
    cur.executemany(
        "INSERT INTO seeds (geom) VALUES (ST_SetSRID(ST_MakePoint(%s, %s), 4326));",
        seed_coords
    )

    conn.commit()
    cur.close()
    conn.close()
