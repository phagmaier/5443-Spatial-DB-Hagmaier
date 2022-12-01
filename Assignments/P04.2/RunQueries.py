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

outfile = open("Output.txt", "w")

getFireRow = "SELECT * FROM gun_state WHERE ship_id = 3 and gun_id = 'Mark13'"

with DatabaseCursor() as cur:
    cur.execute(getFireRow)
    output = cur.fetchall()

outfile.write('-'*400 + '\n\n')
outfile.write("Row Before: " + str(output) + '\n\n')

fire = "UPDATE gun_state SET ammo = ammo - 1 WHERE ammo > 0 and ship_id = 3 and gun_id = 'Mark13'"
outfile.write("Query: " + fire + '\n\n')

with DatabaseCursor() as cur:
    cur.execute(fire)

with DatabaseCursor() as cur:
    cur.execute(getFireRow)
    output = cur.fetchall()

outfile.write("Row After: " + str(output) + '\n\n')
outfile.write('-'*400 + '\n\n')

getShipStateRow = "SELECT * FROM ship_state WHERE ship_id = 3"
ChangeSpeedAndDirection = "UPDATE ship_state SET bearing = 45, speed = 40 WHERE ship_id = 3"

with DatabaseCursor() as cur:
    cur.execute(getShipStateRow)
    output = cur.fetchall()

outfile.write("Row Before: " + str(output) + '\n\n')
outfile.write("Query: " + ChangeSpeedAndDirection + '\n\n')

with DatabaseCursor() as cur:
    cur.execute(ChangeSpeedAndDirection)

with DatabaseCursor() as cur:
    cur.execute(getShipStateRow)
    output = cur.fetchall()

outfile.write("Row After: " + str(output) + '\n\n')
outfile.write('-'*400 + '\n\n')

getShipStateRow = "SELECT ship_id, bearing FROM ship_state"
ChangeDirection = "UPDATE ship_state SET bearing = 270"

with DatabaseCursor() as cur:
    cur.execute(getShipStateRow)
    output = cur.fetchall()

outfile.write("Row Before: " + str(output) + '\n\n')
outfile.write("Query: " + ChangeDirection + '\n\n')

with DatabaseCursor() as cur:
    cur.execute(ChangeDirection)

with DatabaseCursor() as cur:
    cur.execute(getShipStateRow)
    output = cur.fetchall()

outfile.write("Row After: " + str(output) + '\n\n')
outfile.write('-'*400 + '\n\n')

getGunStateRow = "SELECT ship_id, gun_id, bearing FROM gun_state WHERE ship_id = 6"
ChangeDirection = "UPDATE gun_state SET bearing = 22 WHERE ship_id = 6"

with DatabaseCursor() as cur:
    cur.execute(getGunStateRow)
    output = cur.fetchall()

outfile.write("Row Before: " + str(output) + '\n\n')
outfile.write("Query: " + ChangeDirection + '\n\n')

with DatabaseCursor() as cur:
    cur.execute(ChangeDirection)

with DatabaseCursor() as cur:
    cur.execute(getGunStateRow)
    output = cur.fetchall()

outfile.write("Row After: " + str(output) + '\n\n')
outfile.write('-'*400 + '\n\n')

getTorpedo = "SELECT * FROM torpedo_state WHERE ship_id = 21 and t_id = 'MK31' and location = 'bow' and side = 'port' and facing = 'ahead'"
FireTorpedo = "DELETE FROM torpedo_state WHERE ship_id = 21 and t_id = 'MK31' and location = 'bow' and side = 'port' and facing = 'ahead'"

with DatabaseCursor() as cur:
    cur.execute(getTorpedo)
    output = cur.fetchall()

outfile.write("Row Before: " + str(output) + '\n\n')
outfile.write("Query: " + FireTorpedo + '\n\n')

with DatabaseCursor() as cur:
    cur.execute(FireTorpedo)

outfile.write("Result: " + "DELETED 1" + '\n\n')
outfile.write('-'*400 + '\n\n')