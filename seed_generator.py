import fields2cover as f2c
import math
import json
# Your perimeter (must be closed)

def generate_path_csv(perimeter,angle_degrees=0):
    # 1️⃣ Create LinearRing
    points = f2c.VectorPoint()
    for x, y in perimeter:
        points.push_back(f2c.Point(x, y))
    
    outer_ring = f2c.LinearRing(points)
    
    # 2️⃣ Create Cell
    try:
        cell = f2c.Cell(outer_ring)
        print("Cell created successfully!")
    except Exception as e:
        print("Error creating Cell:", e)
    
    # 3️⃣ Wrap into Cells
    try:
        cells = f2c.Cells(cell)
        print("Cells created successfully!")
    except Exception as e:
        print("Error creating Cells:", e)
    
    # 4️⃣ Optional checks
    print("Area:", cells.area())
    print("Is convex?", cells.isConvex())
    print("GeoJSON preview:", cells.exportToJson())

    angle_radians = math.radians(angle_degrees)
    rand = f2c.Random(42)
    robot = f2c.Robot(0.00002, 0.000012)
    robot.setMinTurningRadius(0.01)  # m
    robot.setMaxDiffCurv(99999999);   # 1/m^2
    path_planner = f2c.PP_PathPlanning()
    no_hl = cells
    bf = f2c.SG_BruteForce()
    swaths = bf.generateSwaths(angle_radians, robot.getCovWidth(), no_hl.getGeometry(0))
    boustrophedon_sorter = f2c.RP_Boustrophedon()
    swaths = boustrophedon_sorter.genSortedSwaths(swaths)
    dubins = f2c.PP_DubinsCurves()
    path_dubins = path_planner.planPath(robot, swaths, dubins);
    geojson_string = path_dubins.toLineString().exportToJson()
    geojson_data = json.loads(geojson_string)
    coords = geojson_data['coordinates']
    start_point = coords[0] if coords else None
    end_point = coords[-1] if coords else None
    
    return {
        "path": geojson_data,
        "start": {"lon": start_point[0], "lat": start_point[1]} if start_point else None,
        "end": {"lon": end_point[0], "lat": end_point[1]} if end_point else None
    }

