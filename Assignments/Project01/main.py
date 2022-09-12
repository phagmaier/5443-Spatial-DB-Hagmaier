#imports:
#FastAPI: for the api
#psycopg2: to work with psql in python
#uvicron to run the api 

from fastapi import FastAPI
import psycopg2.extras
import uvicorn
#import json
import uvicorn
from fastapi import FastAPI
#from psycopg2.extensions import AsIs



'''
PROGRAM DESCRIPTION:
Create and API where we use psycopg2 to connect to the database public.firenews
Created three functions that correspond with thre eget statments that return all the data
in the database as a dictionary, a function that retuns a single entry of the database based on
entering the unique id associated with the that specific piece of data. Find the closest item in the 
data base based on two entered cords long and lat.
'''


app = FastAPI()


#Class DatabaseCursor allows us to 'turn on' the cursor when running inside a function using a with method
#Making it more secure 

#copied (with some changes listed below) from: https://github.com/rugbyprof/5443-Spatial-DB/blob/main/Lectures/02_Chap2/main.py
#since I didn't originally know how to create __enter__ and exit methods for a cursor
#after seeing this it I don't know why I struggled doing this I shoudl have been able to make this
#(Thank you proffesor Griffin)
#changes: 
#set self.cur and use RealDictCursor in order to return a dictionary instead of a list
#lazy and did not use a config file and therfore didn't need the __init__ func
class DatabaseCursor(object):
    """https://stackoverflow.com/questions/32812463/setting-schema-for-all-queries-of-a-connection-in-psycopg2-getting-race-conditi
    https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
    """
    '''
    def __init__(self, conn_config_file):
        with open(conn_config_file) as config_file:
            self.conn_config = json.load(config_file)
    '''

    def __enter__(self):
        self.conn = con = psycopg2.connect(host="localhost", database="newproj", user="parkerhagmaier", password="Basketball01!")
        self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        #self.cur.execute("SET search_path TO " + self.conn_config["schema"])

        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # some logic to commit/rollback

        self.conn.commit()
        self.conn.close()


#returns a dictionary from the database firenews in the public schema 
#with allows us to securly turn on our cursor when using it and turn it off when finished
#cur.execute fetches the query from the database
#stored in results and then returned to \everything
@app.get("/everything")
def everything():
    with DatabaseCursor() as cur:
        cur.execute('SELECT * FROM "public"."firenews"')
        results = cur.fetchall()
        return results

#Enter the id of the item in the database you want to retrieve
#result of the query stored in oneresult
#statment is executed with cur.execute
@app.get("/one/{num}")
def one(num: int):
    with DatabaseCursor() as cur:
        statment = 'SELECT * FROM "public"."firenews" WHERE id = %s'
        cur.execute(statment, (num,))
        oneresults = cur.fetchall()
        return oneresults

#using psql's ST_MAKEPOINT we create a point based on the x and y entered (longitude and lat)
#we then use psql's ORDER BY to order by the closest geography
#return the first (closest) result in newResult
@app.get("/closest/{x}/{y}")
def closest(x:float, y:float):
    with DatabaseCursor() as cur:
        closer = 'SELECT * FROM "public"."firenews" ORDER BY "public"."firenews"."the_geom" <-> ST_MakePoint(%s,%s)::geography'
        cur.execute(closer, [x,y])
        newResult = cur.fetchone()
        return newResult
