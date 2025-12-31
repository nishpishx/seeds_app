from seed_generator import generate_path_csv

import json



perimeter = [

    (-122.4881720747436, 37.86431319225779),

    (-122.488235658491, 37.86423935838986),

    (-122.4881382666009, 37.86419005972356),

    (-122.488076302597, 37.86426307188792),

    (-122.4881720747436, 37.86431319225779)

]



result = generate_path_csv(perimeter, 304)



# -------- Save to file --------

with open("mission_304deg.json", "w") as f:

    json.dump(result, f, indent=2)



print("Saved mission_304deg.json")



print(result["start"])

print(result["end"])

print(result["path"]["type"])       # LineString

print(len(result["path"]["coordinates"]))

