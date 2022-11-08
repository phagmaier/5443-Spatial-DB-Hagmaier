from atexit import register
import json
import requests
from geojson import MultiPolygon, Point, MultiPoint
import psycopg2
import time

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

def convertLinestring(line):
    count = 0
    while line[count] != '(':
        count += 1
    count += 1
    cleaned = line[count:-1]
    cleaned = cleaned.split(' ')
    new = []
    for i in cleaned:
        if ',' in i:
            count = 0
            while i[count] != ',':
                count += 1
            new.append(float(i[:count]))
            new.append(float(i[count+1:]))

        else:
            new.append(float(i))
    final = []
    for i in range(0, len(new), 2):
        final.append((new[i], new[i+1], 0))
    if len(final) > 4:
        return final[:4]

    else:
        return final

#used to store previous missile information
MissileInfo = {}
#used to check if a missile has already been processed
IDsDone = []

#resets the game probably should use this only for testing but who knows
#requests.get("http://missilecommand.live:8080/RESET")

#lets the request finish
time.sleep(5)

#registers our team
register = requests.get("http://missilecommand.live:8080/REGISTER").json()

#checks to make sure register worked so there is enough geometries 
try:
    teamID = register["id"]
except:
    print("No available regions right now!")
    exit()

#stores the geometry as geojson
regionMultiPoly = MultiPolygon(register["region"]["features"][0]["geometry"]["coordinates"])

#prints out region really is just used for visualization testing
#print(regionMultiPoly)

cities = []

#stores the missiles
arsenal = register["arsenal"]

#places cities into an array
for city in register["cities"]["features"]:
    cities.append(Point(city["geometry"]["coordinates"]))

statement = """DROP TABLE IF EXISTS testCities"""
with DatabaseCursor() as cur:
    cur.execute(statement)

statement = 'CREATE TABLE testCities(id numeric NOT NULL PRIMARY KEY, city geometry(POINT, 4326))'
with DatabaseCursor() as cur:
    cur.execute(statement)

#loads cities into a postgres table
for i, city in enumerate(cities):
    statement = """INSERT INTO testCities (id, city) VALUES(%s, ST_SetSRID(ST_MakePoint(%s,%s), 4326))"""
    with DatabaseCursor() as cur:
        cur.execute(statement, (i, city["coordinates"][0], city["coordinates"][1]))

statement = """DROP TABLE IF EXISTS testArsenal"""
with DatabaseCursor() as cur:
    cur.execute(statement)

statement = 'CREATE TABLE testArsenal(id numeric NOT NULL PRIMARY KEY, name VARCHAR(50), supply numeric)'

with DatabaseCursor() as cur:
    cur.execute(statement)

#loads the arsenal into postgres table
for count, i in enumerate(arsenal):
    statement = """INSERT INTO testArsenal(id, name, supply) VALUES(%s,%s,%s) """
    with DatabaseCursor() as cur:
        cur.execute(statement, (count, i, arsenal[i]))

#Places the batteries on the extremes of the polygon
statement = "SELECT st_asText(ST_ExteriorRing(ST_Envelope(ST_GeomFromGeoJSON('" + str(regionMultiPoly) + "'))))"
with DatabaseCursor() as cur:
    cur.execute(statement)
    results = cur.fetchall()
    results = results[0][0]
cords = convertLinestring(results)
statement = """DROP TABLE IF EXISTS batteries"""
with DatabaseCursor() as cur:
    cur.execute(statement)
statement = 'CREATE TABLE batteries(id numeric, points geometry(POINT, 4326))'
with DatabaseCursor() as cur:
    cur.execute(statement)
statement = "INSERT INTO batteries(id, points) VALUES(%s, ST_ClosestPoint(ST_GeomFromGeoJSON('" + str(regionMultiPoly) + "'), ST_SetSRID(ST_MakePoint(%s,%s), 4326)))"
for i in range(len(cords)):
    with DatabaseCursor() as cur:
        cur.execute(statement, (i+1,cords[i][0],cords[i][1]))

#request to start the game
requests.get("http://missilecommand.live:8080/START/" + str(teamID))

#lets request finish
time.sleep(5)

#probably will need to change this but meh
while(True):
    #preforms radar sweep and breaks if there are no missiles
    try:
        sweep = requests.get("http://missilecommand.live:8080/RADAR_SWEEP").json()
        sweep["features"]
    except:
        print("NO ACTIVE MISSILES!!!")
        requests.get("http://missilecommand.live:8080/QUIT" + str(teamID))
        exit()

    #goes through each missile in the sweep
    for feature in sweep["features"]:
        #if there is already information about that missile uses the algorithm to make its path
        if feature["id"] in MissileInfo.keys():

            #uses postgis to get the change in time
            TimeChange = "SELECT EXTRACT (EPOCH FROM (SELECT time '" + feature["properties"]["current_time"] + "' - time '" + MissileInfo[feature["id"]]["current_time"] + "'))"
            with DatabaseCursor() as cur:
                cur.execute(TimeChange)
                TimeChange = int(cur.fetchall()[0][0])
            
            #drop rate = change in alt / change in time
            DropRate =  (MissileInfo[feature["id"]]["altitude"] - feature["properties"]["altitude"]) / TimeChange
            
            #how many seconds until alt = 0 -> alt / drop rate
            HowManySeconds = MissileInfo[feature["id"]]["altitude"] / DropRate

            #uses postgis to get the missile speed
            MissileSpeed = "SELECT ms FROM missile_speed WHERE category = (SELECT \"speedCat\" FROM missile where name = '" + feature["properties"]["missile_type"] + "') "
            with DatabaseCursor() as cur:
                cur.execute(MissileSpeed)
                MissileSpeed = int(cur.fetchall()[0][0])

            #uses postgis project to get the exact location that the missile will reach alt = 0
            HitPoint = "SELECT ST_AsGeoJSON(ST_Project('POINT(" + str(MissileInfo[feature["id"]]["geometry"][0]) + " " + str(MissileInfo[feature["id"]]["geometry"][1]) + ")'::geography, " + str(MissileSpeed * HowManySeconds) + "," + str(MissileInfo[feature["id"]]["bearing"]) + "));"
            with DatabaseCursor() as cur:
                cur.execute(HitPoint)
                HitPoint = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

            #uses postgis contains to check if the hit point is in the polygon
            InPoly = "SELECT ST_Contains(ST_GeomFromGeoJSON('" + str(regionMultiPoly) + "'), ST_GeomFromGeoJSON('" + str(HitPoint) + "'))"
            with DatabaseCursor() as cur:
                cur.execute(InPoly)
                InPoly = bool(cur.fetchall()[0][0])

            #makes it so that perceived hit point is actually the city it is most likely targeting
            MovePoint = "SELECT ST_AsGeoJSON(city), ST_Distance(city, ST_GeomFromGeoJSON('"+ str(HitPoint) +"')) as dist FROM testcities ORDER BY dist ASC LIMIT 1"
            with DatabaseCursor() as cur:
                cur.execute(MovePoint)
                HitPoint = Point(json.loads(cur.fetchall()[0][0])["coordinates"])

            #if the hit point is in the polygon then the do the algo
            if InPoly:

                #uses postgis to get a set of (100) points along the line with the missile for interception
                MissileLineWithPoints = "SELECT ST_AsGeoJSON(ST_LineInterpolatePoints(ST_MakeLine(ST_MakePoint(" + str(MissileInfo[feature["id"]]["geometry"][0]) + "," + str(MissileInfo[feature["id"]]["geometry"][1]) +"," + str(MissileInfo[feature["id"]]["altitude"]) + "), ST_MakePoint("+ str(HitPoint["coordinates"][0]) + "," + str(HitPoint["coordinates"][1]) + ",0)), .01));"
                with DatabaseCursor() as cur:
                    cur.execute(MissileLineWithPoints)
                    MissileLineWithPoints = MultiPoint(json.loads(cur.fetchall()[0][0])["coordinates"])

                #used to print the missiles path for visualization purposes not needed!!!
                #print('{"type": "Feature", "properties": {}, "geometry":' + str(MissileLineWithPoints) + "},")

                #the point we want to try and intercept (halfway point)
                target = MissileLineWithPoints["coordinates"][(len(MissileLineWithPoints["coordinates"]) - 1) // 2]
            
                #gets the closest battery to where we want to intercept
                battery = "SELECT ST_AsGeoJSON(points), ST_Distance(points, ST_Point("+ str(target[0]) + "," + str(target[1]) + ",4326)) as dist FROM batteries ORDER BY dist ASC LIMIT 1"
                with DatabaseCursor() as cur:
                    cur.execute(battery)
                    battery = Point(json.loads(cur.fetchall()[0][0])["coordinates"])
                    #makes 3d point at alt 0
                    battery["coordinates"].append(0)

                #use drop rate and altitude of at target location to get time at target location
                HitTime = target[2] / DropRate

                #gets the distance from the battery to the missile in meters
                DistanceToMissile = "SELECT ST_3DDistance(ST_Transform(ST_GeomFromGeoJSON('" + str(battery) + "'), 2163), ST_Transform(ST_PointZ("+ str(target[0]) + "," + str(target[1]) + "," + str(target[2]) +",4326),2163))"
                with DatabaseCursor() as cur:
                    cur.execute(DistanceToMissile)
                    DistanceToMissile = float(cur.fetchall()[0][0])

                #the minimum speed of a missile to reach the target
                MinimumSpeed = DistanceToMissile / HitTime
                
                #gets the info of the missile to shoot
                MissileToSend = 'SELECT ms, missile."name", supply FROM missile_speed JOIN missile on missile_speed.category = missile."speedCat" JOIN testarsenal on missile.id = testarsenal.id WHERE ms >= ' + str(MinimumSpeed) + ' AND supply > 0 ORDER BY supply DESC LIMIT 1'
                try:
                    with DatabaseCursor() as cur:
                        cur.execute(MissileToSend)
                        MissileToSend = cur.fetchall()[0]

                    #decrements the missile used
                    UseMissile = 'UPDATE testarsenal SET supply = supply - 1 WHERE testarsenal."name" = \'' + MissileToSend[1] + '\';'
                    with DatabaseCursor() as cur:
                        cur.execute(UseMissile)
                    
                    # #gets the amount of seconds needed to reach target with given missile
                    TimeNeededToHit = DistanceToMissile / float(MissileToSend[0])

                    #gets when we need to fire from battery
                    WhenFire = HitTime - TimeNeededToHit

                    #gets the timestamp we need to fire from battery
                    FireTime = "SELECT current_date + time '" + MissileInfo[feature["id"]]["current_time"] + "' + interval '" + str(WhenFire) + " seconds' as until"
                    with DatabaseCursor() as cur:
                        cur.execute(FireTime)
                        FireTime = str(cur.fetchall()[0][0])

                    #gets hit time in required way
                    ExpectedHitTime = "SELECT current_date + time '" + MissileInfo[feature["id"]]["current_time"] + "' + interval '" + str(HitTime) + " seconds' as until"
                    with DatabaseCursor() as cur:
                        cur.execute(ExpectedHitTime)
                        HitTime = str(cur.fetchall()[0][0])

                    solution = {
                        "team_id" : teamID,
                        "target_missile_id": feature["id"],
                        "missile_type": MissileToSend[1],
                        "fired_time": FireTime,
                        "firedfrom_lat": battery["coordinates"][1],
                        "firedfrom_lon": battery["coordinates"][0],
                        "aim_lat": target[1],
                        "aim_lon": target[0],
                        "expected_hit_time": HitTime,
                        "target_alt": target[2]
                    }

                    print(solution)
                    print()
                    response = requests.post("http://missilecommand.live:8080/FIRE_SOLUTION", json = solution)
                    print(response.text)
                    print()
                except:
                    print("No missiles left with a minimum speed of: " + str(MinimumSpeed))
                    print()

            #removes proceeded missiles
            IDsDone.append(feature["id"])
            MissileInfo.pop(feature["id"])
        #else if it has not been registered store it
        elif feature["id"] not in IDsDone:
            MissileInfo.update({feature["id"]: {
                "geometry": feature["geometry"]["coordinates"],
                "bearing": feature["properties"]["bearing"],
                "altitude": feature["properties"]["altitude"],
                "current_time": feature["properties"]["current_time"],
                "missile_type": feature["properties"]["missile_type"]
            }})
    #allows the API to recover
    time.sleep(1)
