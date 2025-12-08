import fields2cover as f2c

# ----------------------------
# 1️⃣ Define field perimeter only
# ----------------------------
perimeter = [
    (0.0, 0.0),
    (32.78050114008247, 1.5825016090575466),
    (29.57253273552087, 117.33027361366625),
    (-1.356751555428749, 116.6520692813985),
    (0.0, 0.0)
]

# ----------------------------
# 2️⃣ Create robot
# ----------------------------
robot_c = f2c.Robot(1.8, 2.0)
robot_c.setMinTurningRadius(0.5)

# ----------------------------
# 3️⃣ Create outer ring & cell
# ----------------------------
points = f2c.VectorPoint()
for lon, lat in perimeter:
    points.push_back(f2c.Point(lon, lat))

outer_ring = f2c.LinearRing(points)
cell_c = f2c.Cell(outer_ring)

# ----------------------------
# 4️⃣ Wrap cell into Cells
# ----------------------------
cells_c = f2c.Cells(cell_c)  # only one polygon, no obstacles

# ----------------------------
# 5️⃣ Generate headlands
# ----------------------------
const_hl = f2c.HG_Const_gen()
mid_hl_c = const_hl.generateHeadlands(cells_c, 0.0)
no_hl_c = const_hl.generateHeadlands(cells_c, 1.0)

# ----------------------------
# 6️⃣ Generate swaths
# ----------------------------
swath_length = f2c.OBJ_SwathLength()
swaths_c = f2c.SG_BruteForce().generateBestSwaths(swath_length, robot_c.getCovWidth(), no_hl_c)

# ----------------------------
# 7️⃣ Generate route and path
# ----------------------------
route_planner = f2c.RP_RoutePlannerBase()
route = route_planner.genRoute(mid_hl_c, swaths_c)

path_planner = f2c.PP_PathPlanning()
dubins = f2c.PP_DubinsCurvesCC()
path = path_planner.planPath(robot_c, route, dubins)

# ----------------------------
# 8️⃣ Visualize
# ----------------------------
f2c.Visualizer.figure()
f2c.Visualizer.plot(cells_c)      # field boundary
f2c.Visualizer.plot(mid_hl_c)      # mid headlands
f2c.Visualizer.plot(no_hl_c)       # outer headlands
f2c.Visualizer.plot(path)          # planned path
f2c.Visualizer.save("test_route_no_obstacles.png")
