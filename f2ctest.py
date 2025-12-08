import fields2cover as f2c

# Your perimeter (must be closed)
perimeter = [
    (0.0, 0.0),
    (32.78, 1.58),
    (29.57, 117.33),
    (-1.35, 116.65),
    (0.0, 0.0)
]

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
