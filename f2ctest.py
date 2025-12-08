import fields2cover as f2c


perimeter = [(0.0, 0.0),
                    (32.78050114008247, 1.5825016090575466),
                    (29.57253273552087, 117.33027361366625),
                    (-1.356751555428749, 116.6520692813985),
                    (0.0, 0.0)]


obstacle_1 = [(4.747806702833676, 5.651789908962271),
                  (6.273475800086682, 5.651789908962271),
                  (4.453250327517964, 109.70047130564375),
                  (3.0803003438120697, 109.64395422172686),
                  (4.747806702833676, 5.651789908962271)]

obstacle_2 = [(11.630852129420637, 6.44304015055372),
                  (12.987603683127588, 6.44304015055372),
                  (11.473218260136703, 110.20912503561279),
                  (9.997544584299696, 110.20912503561279),
                  (11.630852129420637, 6.44304015055372)]



robot_c = f2c.Robot(1.8, 2.0)
robot_c.setMinTurningRadius(0.5)


points = f2c.VectorPoint()
for (lon, lat) in perimeter:
	points.push_back(f2c.Point(lon, lat))
outer_ring = f2c.LinearRing(points)

points = f2c.VectorPoint()
for (lon, lat) in obstacle_1:
	points.push_back(f2c.Point(lon, lat))
obstacle_1_ring = f2c.LinearRing(points)

points = f2c.VectorPoint()
for (lon, lat) in obstacle_2:
	points.push_back(f2c.Point(lon, lat))
obstacle_2_ring = f2c.LinearRing(points)

cells_c = f2c.Cells(f2c.Cell(outer_ring))
cells_c.addRing(0, obstacle_1_ring)
cells_c.addRing(0, obstacle_2_ring)

const_hl = f2c.HG_Const_gen();
mid_hl_c = const_hl.generateHeadlands(cells_c, 0.0)
no_hl_c = const_hl.generateHeadlands(cells_c, 1.0)

swath_length = f2c.OBJ_SwathLength()
swaths_c = f2c.SG_BruteForce().generateBestSwaths(swath_length,  robot_c.getCovWidth(), no_hl_c)


route_planner = f2c.RP_RoutePlannerBase()
route = route_planner.genRoute(mid_hl_c, swaths_c)

path_planner = f2c.PP_PathPlanning()
dubins = f2c.PP_DubinsCurvesCC()
path = path_planner.planPath(robot_c, route, dubins)


f2c.Visualizer.figure();
f2c.Visualizer.plot(cells_c);
f2c.Visualizer.plot(mid_hl_c)
f2c.Visualizer.plot(no_hl_c);
f2c.Visualizer.plot(path)
f2c.Visualizer.save("test_route.png")
