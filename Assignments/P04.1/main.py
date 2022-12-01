import psycopg2
import json
import random
from geojson import Polygon, Point, MultiPoint

#class to do database queries
class DatabaseCursor(object):
    def __enter__(self):
        with open("login.json") as f:
            data = json.load(f)
            self.conn = psycopg2.connect(host = data["host"], database = data["dbname"], user = data["user"], password = data["password"])
            self.cur = self.cur = self.conn.cursor()
            return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

#runs the sql file to create the ships table
with DatabaseCursor() as cur:
    cur.execute(open("./SQL/MakeShipsTable.psql", "r").read())

#holds the number of boats total
boats = 0

with open("ships.json", "r") as shipsFile:
    ships = json.load(shipsFile)

    insert = "INSERT INTO public.ships(id, category, shipclass, length, width, torpedolaunchers, armament, hullarmor, deckarmor, speed, turnradius, location, bearing) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    for ship in ships:
        row = []
        row.append(ship["id"])
        row.append(ship["category"])
        row.append(ship["shipClass"])
        row.append(ship["length"])
        row.append(ship["width"])
        row.append(ship["torpedoLaunchers"]) if ship["torpedoLaunchers"] == None else row.append(json.dumps(ship["torpedoLaunchers"]))
        row.append(json.dumps(ship["armament"]))
        row.append(ship["armor"]["hull"])
        row.append(ship["armor"]["deck"])
        row.append(ship["speed"])
        row.append(ship["turn_radius"])
        row.append(ship["location"])
        row.append(0.0)

        #loads in the row of data
        with DatabaseCursor() as cur:
            cur.execute(insert, row)

        boats += 1

#gets a random degree between 0->360
degrees = random.uniform(0, 360)

#holds the cardinal direction information
cardinalList = ["N","NNE","NE","ENE","E","ESE","SE","SSE", "S","SSW","SW","WSW","W","WNW","NW","NNW"]
cardinalDegree = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
cardinalMax = [348.75, 11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75, 281.25, 303.75, 326.25]
cardinalMin = [11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75, 281.25, 303.75, 326.25, 348.75]

degrees = int(float(degrees))
index = int((degrees + 11.25) / 22.5)

#gets the direction of area I am using
direction = cardinalList[index % 16]
#used to place boats facing opposite direction to the edge of the map
opposite = cardinalList[(index + 8) % 16]
oppositeBearing = cardinalDegree[(index + 8) % 16]

#left and rightmost of area
left = cardinalMax[index % 16]
right = cardinalMin[index % 16]

#gets the bounding box for the map
bbox = "SELECT ST_AsGeoJson(ST_MakeEnvelope(-10.31324002, 48.74631646, -8.06068579, 50.17116998, 4326))"
with DatabaseCursor() as cur:
    cur.execute(bbox)
    bbox = Polygon(json.loads(cur.fetchall()[0][0])["coordinates"])

#gets the center point of the map
Center = "SELECT ST_AsGeoJson(ST_Centroid(ST_GeomFromGeoJSON('" + str(bbox) + "')))"
with DatabaseCursor() as cur:
    cur.execute(Center)
    Center = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

#gets the extremes of my region
p1 = "SELECT ST_AsGeoJSON(ST_Intersection(ST_Project(ST_GeomFromGeoJSON('" + str(Center) + "'), 80000, radians(" + str(left) + ")), ST_GeomFromGeoJSON('" + str(bbox) + "')))"
with DatabaseCursor() as cur:
    cur.execute(p1)
    p1 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

p2 = "SELECT ST_AsGeoJSON(ST_Intersection(ST_Project(ST_GeomFromGeoJSON('" + str(Center) + "'), 80000, radians(" + str(right) + ")), ST_GeomFromGeoJSON('" + str(bbox) + "')))"
with DatabaseCursor() as cur:
    cur.execute(p2)
    p2 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

#makes the points of the center and extremes into a polygon to query
region = "SELECT ST_AsGeoJSON(ST_MakePolygon(ST_MakeLine((ARRAY[ST_GeomFromGeoJSON('" + str(Center) + "'), ST_GeomFromGeoJSON('" + str(p1) + "'), ST_GeomFromGeoJSON('" + str(p2) + "'), ST_GeomFromGeoJSON('" + str(Center) + "')]))))"
with DatabaseCursor() as cur:
    cur.execute(region)
    region = Polygon(json.loads(cur.fetchall()[0][0])["coordinates"])

#gets the center of the area and places boats around there
BackBoat = "SELECT ST_AsGeoJSON(ST_Centroid(ST_GeomFromGeoJSON('" + str(region) + "')))"
with DatabaseCursor() as cur:
    cur.execute(BackBoat)
    BackBoat = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

update = "UPDATE ships SET location = ST_GeomFromGeoJSON(%s), bearing = " + str(oppositeBearing) + " WHERE id = %s"

r0 = "SELECT ST_AsGeoJSON(ST_Project(ST_Project(ST_GeomFromGeoJSON('" + str(BackBoat) + "'), 111, radians(270)), 111, radians(0)))"
r1 = BackBoat
r2 = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON('" + str(BackBoat) + "'), 111, radians(180)))"

#places the first 4 boats due to its 4 row pattern
with DatabaseCursor() as cur:
    cur.execute(r0)
    r0 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

with DatabaseCursor() as cur:
    cur.execute(r2)
    r2 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

r3 = "SELECT ST_AsGeoJSON(ST_Project(ST_Project(ST_GeomFromGeoJSON('" + str(r2) + "'), 111, radians(270)), 111, radians(180)))"

with DatabaseCursor() as cur:
    cur.execute(r3)
    r3 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

with DatabaseCursor() as cur:
    cur.execute(update, (json.dumps(r1), 0))

with DatabaseCursor() as cur:
    cur.execute(update, (json.dumps(r2), 1))

with DatabaseCursor() as cur:
    cur.execute(update, (json.dumps(r3), 2))

with DatabaseCursor() as cur:
    cur.execute(update, (json.dumps(r0), 3))

next = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON(%s), 111, radians(270)))"

#moves ships along the row in an ordered fashion
for i in range(4, boats):
    if i % 4 == 0:
        next = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON('" + str(r1) + "'), 222, radians(270)))"
        with DatabaseCursor() as cur:
            cur.execute(next)
            r1 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

        with DatabaseCursor() as cur:
            cur.execute(update, (json.dumps(r1), i))
    elif i % 4 == 1:
        next = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON('" + str(r2) + "'), 222, radians(270)))"
        with DatabaseCursor() as cur:
            cur.execute(next)
            r2 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

        with DatabaseCursor() as cur:
            cur.execute(update, (json.dumps(r2), i))
    elif i % 4 == 2:
        next = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON('" + str(r3) + "'), 222, radians(270)))"
        with DatabaseCursor() as cur:
            cur.execute(next)
            r3 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

        with DatabaseCursor() as cur:
            cur.execute(update, (json.dumps(r3), i))
    else:
        next = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON('" + str(r0) + "'), 222, radians(270)))"
        with DatabaseCursor() as cur:
            cur.execute(next)
            r0 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

        with DatabaseCursor() as cur:
            cur.execute(update, (json.dumps(r0), i))

#used to output answer
answer = {
    "fleet_id": random.randint(1,30),
    "ship_status": []
}

#gets all necessary things from the ships table for 
select = "SELECT id, bearing, ST_asGeoJSON(location) FROM ships ORDER BY id ASC"
with DatabaseCursor() as cur:
    cur.execute(select)
    res = cur.fetchall()

for result in res:
    answer["ship_status"].append({"ship_id": result[0], "bearing": result[1], "location": {"lon": json.loads(result[2])["coordinates"][0], "lat":json.loads(result[2])["coordinates"][1]}})

#writes output readably in JSON format
with open("final_product.json", "w") as out:
    json.dump(answer, out, indent=4)
