import psycopg2
import json

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

with DatabaseCursor() as cur:
    cur.execute(open("./SQL/MakeTables/cartridge.psql", "r").read())

with DatabaseCursor() as cur:
    cur.execute(open("./SQL/MakeTables/gun.psql", "r").read())

with DatabaseCursor() as cur:
    cur.execute(open("./SQL/MakeTables/GunState.psql", "r").read())

with DatabaseCursor() as cur:
    cur.execute(open("./SQL/MakeTables/projectile.psql", "r").read())

with DatabaseCursor() as cur:
    cur.execute(open("./SQL/MakeTables/GunState.psql", "r").read())

with DatabaseCursor() as cur:
    cur.execute(open("./SQL/MakeTables/ship_guns.psql", "r").read())

with DatabaseCursor() as cur:
    cur.execute(open("./SQL/MakeTables/ShipState.psql", "r").read())

with DatabaseCursor() as cur:
    cur.execute(open("./SQL/MakeTables/torpedo.psql", "r").read())

with DatabaseCursor() as cur:
    cur.execute(open("./SQL/MakeTables/torpedo_state.psql", "r").read())

#gets info to load into other tables
ships = "SELECT * FROM ships"
with DatabaseCursor() as cur:
    cur.execute(ships)
    ships = cur.fetchall()

insertShipState = "INSERT INTO public.ship_state(ship_id, bearing, speed, location) VALUES (%s, %s, %s, %s);"
insertShipGun = "INSERT INTO public.ships_guns(ship_id, gun_id, type, pos) VALUES (%s, %s, %s, %s);"
insertGunState = "INSERT INTO public.gun_state(ship_id, gun_id, bearing, elevation, ammo) VALUES (%s, %s, %s, %s, %s);"
insertTorpedoState = "INSERT INTO public.torpedo_state(ship_id, t_id, location, side, facing) VALUES (%s, %s, %s, %s, %s);"

for ship in ships:
    with DatabaseCursor() as cur:
        cur.execute(insertShipState, (ship[0], ship[12], ship[9], ship[11]))

    for arm in ship[6]:
        with DatabaseCursor() as cur:
            cur.execute(insertShipGun, (ship[0], arm['gun']['name'], arm['gun']['ammoType'][0], arm['pos']))

        with DatabaseCursor() as cur:
            #bearing = bearing of ship; elevation = 0
            cur.execute(insertGunState, (ship[0], arm['gun']['name'], ship[12], 0, arm['gun']['ammo'][0]['count']))

    #doesn't run when no torpedos
    if ship[5] != None:
        for torpedo in ship[5]:
            with DatabaseCursor() as cur:
                cur.execute(insertTorpedoState, (ship[0], torpedo['torpedos']['name'], torpedo['location'], torpedo['side'], torpedo['facing']))