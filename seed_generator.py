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
    robot = f2c.Robot(0.000000002, 0.6)
    robot.setMinTurningRadius(0.000000002)  # m
    robot.setMaxDiffCurv(0.1);  # 1/m^2
    path_planner = f2c.PP_PathPlanning()
    
    no_hl = cells
    bf = f2c.SG_BruteForce()
    swaths = bf.generateSwaths(angle_radians, robot.getCovWidth(), no_hl.getGeometry(0))
    snake_sorter = f2c.RP_Snake()
    swaths = snake_sorter.genSortedSwaths(swaths)
    dubins = f2c.PP_DubinsCurves()
    path_dubins = path_planner.planPath(robot, swaths, dubins);
    geojson_string = path_dubins.toLineString().exportToJson()
    seeds = json.loads(geojson_string)
    
    # Return dict for Flask to jsonify
    return seeds
   
