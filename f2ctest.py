import math
import fields2cover as f2c

# ----------------------------
# 1. Create robot and field
# ----------------------------
rand = f2c.Random(42)             # Random field generator
robot = f2c.Robot(2.0, 6.0)       # Robot(width, coverage_width)
robot.setMinTurningRadius(2.0)    # meters
robot.setMaxDiffCurv(0.1)         # 1/m^2

# Generate a random field with 5 cells
field = rand.generateRandField(1e4, 5)
cells = field.getField()

# ----------------------------
# 2. Generate headlands
# ----------------------------
const_hl = f2c.HG_Const_gen()
no_hl = const_hl.generateHeadlands(cells, 3.0 * robot.getWidth())

# ----------------------------
# 3. Generate swaths
# ----------------------------
bf = f2c.SG_BruteForce()
swaths = bf.generateSwaths(math.pi, robot.getCovWidth(), no_hl.getGeometry(0))

# ----------------------------
# 4. Sort swaths (snake order)
# ----------------------------
snake_sorter = f2c.RP_Snake()
swaths_sorted = snake_sorter.genSortedSwaths(swaths)

# ----------------------------
# 5. Plan path using Dubins curves
# ----------------------------
path_planner = f2c.PP_PathPlanning()
dubins = f2c.PP_DubinsCurves()
path_dubins = path_planner.planPath(robot, swaths_sorted, dubins)

# ----------------------------
# 6. Visualize field and path
# ----------------------------
f2c.Visualizer.figure()
#f2c.Visualizer.plotField(field)
f2c.Visualizer.plot(path_dubins)
#f2c.Visualizer.show()
f2c.Visualizer.save("Tutorial_image.png")
