'''
Parker Hagmaier
09/28/2022
Spatial DataBases
Griffin
'''


#importing psycopg2 in order to connect to our db
#generate a cursor so that we can generate and put in data 
import psycopg2.extras
import psycopg2

# Creates a connection and cursor to our psql databse
# Done to ensure a easy and secure connection that 
#we will call with open every time we need to interact with psql
class DatabaseCursor(object):
    def __enter__(self):
        self.conn = con = psycopg2.connect(host="localhost", database="testing01", user="parkerhagmaier", password="Basketball01!")
        self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


'''
WARNING:
I am an idiot and there is definetley a better way to do this
I am inexpercienced at psql writing queries and using psyopg2 so i did it this dumb way
Would probably be better to convert output to json file or even just use the query as 
input into another query but my incompetence has led me to this
Description:
converts the output of our points query to an array so that we can generate all the combinations
amoung these points
We first seperate all of them in a list split by the ']'
Just makes it easy to create all combiantions
'''
def cleanUp(aString):
    d = aString.split('[')
    fresh = []
    word = ''
    for i in range(len(d)):
        fresh.append([])
        for x in range(len(d[i])):
            if d[i][x].isdigit() or d[i][x] == '.':
                word += d[i][x]
            else:
                if len(word) > 0:
                    fresh[i].append(float(word))
                word = ''
    fresh = [ele for ele in fresh if ele != []]
    return fresh

'''
WARNING:
Same as above:
I am an idiot and there is definetley a better way to do this
I am inexpercienced at psql writing queries and using psyopg2 so i did it this dumb way
Would probably be better to convert output to json file or even just use the query as 
input into another query but my incompetence has led me to this
Description:
We convert our combinations into a string that we can plug in to our interpolate query
in order to generate multi line strings or Missile paths
'''
def newclean(aString):
    clean = []
    aList = aString.split('[')
    word = ''
    group = []
    for i in range(len(aList)):
        for x in range(len(aList[i])):
            if aList[i][x].isdigit() or aList[i][x] == '.':
                word += aList[i][x]
            else:
                if len(word) > 0:
                    word = float(word)
                    if len(group) > 1:
                        clean.append((group[0], group[1]))
                        group = []
                        group.append(word)
                        word = ''
                    else:
                        group.append(float(word))
                        word = ''

    if len(group) > 0:
        clean.append((group[0], group[1]))
    return clean



#pass in a nested list in order to generate all combinations with respect to order
#so that there are no repeats 
# we output an array of arrays with two sets of cordinates 
def combos(aList):
    combinations = []
    length = len(aList) - 1
    for i in range(len(aList)):
        for x in range(length, 0, -1):
            one = aList[i]
            two = aList[x]
            combinations.append([one, two])
    return combinations




'''
Gets the 50 largest Military bases that need to be checked to see if any of the random lines interest
Currently it is operational and should be the easiest to work with
We return a query containing the areas and the name of the base 
'''
def area():
    with DatabaseCursor() as cur:
        statment = 'SELECT fullname, ST_AREA(geom::geography) * 0.00000038610 sqmiles FROM military_bases ORDER BY sqmiles DESC LIMIT 50'
        cur.execute(statment)
        newResult = cur.fetchall()
        return newResult
      

#We take the output of the above function area() and place them in the table public.area 
# we use a for loop to add in every name and coresponding sqrmiles to the table 
# again probably a more effeciant way of doing this 
def adding_areas(arr):
	for i in arr:
		a = i['fullname']
		b = i['sqmiles']
		with DatabaseCursor() as cur:
			statment = "INSERT INTO public.area(fullname, sqmiles) VALUES(%s, %s)"
			cur.execute(statment, [a,b])



'''
This will generate the random points from which you can connect 
them and see if they intesect the millitary base
Our output will come in the form of a GeoJson 
Probably a way to convert it to a geojson but I didn't know how and didn't know to use this as 
input into another query hence the very stupid clean up functions at the top of this program
'''
def getPoints():

    with DatabaseCursor() as cur:
        statment = "SELECT ST_AsGeoJSON(J.*) FROM (SELECT ST_GeneratePoints(geom, 12, 1996) FROM (SELECT ST_Buffer(ST_GeomFromText('LINESTRING(-129.7844079 19.7433195,-61.9513812 19.7433195 , -61.9513812 54.3457868,-129.7844079 54.3457868)'),1, 'endcap=round join=round')  As geom ) as s )as J"
        cur.execute(statment)
        newResult = cur.fetchall()

        return newResult



'''
This function will be called by get paths in a for loop where we use the
cleaned data of combinations to interpolate a multipoint line string 
of each combination 
we return this result which we will also clean up and turn to a stirng that we can pass in to the 
addToTable function
'''
def interpolate(a,b,c,d):
    with DatabaseCursor() as cur:
        statment = "SELECT ST_AsGeoJSON(ST_LineInterpolatePoints('LINESTRING(%s %s,%s %s)', 0.01))"
        cur.execute(statment, [a,b,c,d])
        newResult = cur.fetchone()
        return newResult

'''
We simply add all the multi line strings to the table mypaths meant to hold the line of the 
projectiles trajectory is of the type path
'''
def addToTable(path):
    with DatabaseCursor() as cur:
        statment = "INSERT INTO public.mypaths(trajectory) VALUES(%s)"
        cur.execute(statment, [path])


'''
This function splits all the combinations
So that we can get the multi line string from interpolate 
we then clean the data and add it to the table this function
Mostly just calls other functions 
'''
def getPaths(points):
	for i in range(len(points)):
		a = combinations[i][0][0]
		b = combinations[i][0][1]
		c = combinations[i][1][0]
		d = combinations[i][1][1]

		results = interpolate(a,b,c,d)
		results = results['st_asgeojson']
		cleaned = newclean(results)
		cleaned = str(cleaned)
		addToTable(cleaned)



'''
The function that runs all the other progrems 
A standard main function
We do, do a little clean up here because I'm lazy
'''
def main():
	points = getPoints()
	points = points[0]
	points = points['st_asgeojson']
	points = cleanUp(points)
	combinations = combos(points)
	getPaths(combinations)

	x = area()
	areas = []
	for i in x:
		areas.append(i)

	adding_areas(x)



main()
