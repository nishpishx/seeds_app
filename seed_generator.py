

import math

def generate_seed_coords(width_m, length_m, num_seeds, base_lon, base_lat):
    """
    Generate evenly spaced seed coordinates inside a rectangular area.

    width_m  = rectangle width in meters   (east-west)
    length_m = rectangle height in meters  (north-south)
    num_seeds = total seeds to generate
    base_lon, base_lat = bottom-left corner in degrees
    """

    # Convert meters → degrees
    deg_per_m_lat = 1 / 111320                                  # meters per degree latitude
    deg_per_m_lon = 1 / (111320 * math.cos(math.radians(base_lat)))

    # Rectangle dimensions in degrees
    delta_lat = length_m * deg_per_m_lat
    delta_lon = width_m  * deg_per_m_lon

    coords = []

    # Make a square-ish grid
    rows = int(math.sqrt(num_seeds))
    cols = math.ceil(num_seeds / rows)

    # Step sizes in degrees
    step_lat = delta_lat / (rows - 1) if rows > 1 else 0
    step_lon = delta_lon / (cols - 1) if cols > 1 else 0

    count = 0
    for r in range(rows):
        for c in range(cols):
            if count >= num_seeds:
                break

            lat = base_lat + r * step_lat
            lon = base_lon + c * step_lon

            coords.append((lon, lat))
            count += 1

    return coords


