import fields2cover as f2c
import math
import json
# Your perimeter (must be closed)

def generate_path_csv(perimeter, csv_filename="path.csv"):
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

    
    rand = f2c.Random(42)
    robot = f2c.Robot(2.0, 6.0)
    const_hl = f2c.HG_Const_gen()
    robot.setMinTurningRadius(2)  # m
    robot.setMaxDiffCurv(0.1);  # 1/m^2
    path_planner = f2c.PP_PathPlanning()
    no_hl = const_hl.generateHeadlands(cells, 3.0 * robot.getWidth())
    bf = f2c.SG_BruteForce()
    swaths = bf.generateSwaths(math.pi, robot.getCovWidth(), no_hl.getGeometry(0))
    snake_sorter = f2c.RP_Snake()
    swaths = snake_sorter.genSortedSwaths(swaths)
    dubins = f2c.PP_DubinsCurves()
    path_dubins = path_planner.planPath(robot, swaths, dubins);
    geojson_path = path_dubins.toLineString();
    with open(geojson_filename, "w") as f:
    f.write(str(geojson_path))

    f2c.Visualizer.figure();
    f2c.Visualizer.plot(cells);
    f2c.Visualizer.plot(no_hl);
    f2c.Visualizer.plot(path_dubins);
    f2c.Visualizer.plot(swaths);
    f2c.Visualizer.save("Tutorial_image.png");
