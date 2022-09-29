import psycopg2.extras
import psycopg2





class DatabaseCursor(object):
    def __enter__(self):
        self.conn = con = psycopg2.connect(host="localhost", database="testing01", user="parkerhagmaier", password="Basketball01!")
        self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

class anotherOne(object):
    def __enter__(self):
        self.conn = con = psycopg2.connect(host="localhost", database="testing01", user="parkerhagmaier", password="Basketball01!")
        self.cur = self.conn.cursor()

        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()



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




def combos(aList):
    combinations = []
    length = len(aList) - 1
    for i in range(len(aList)):
        for x in range(length, 0, -1):
            one = aList[i]
            two = aList[x]
            combinations.append([one, two])
    return combinations





def area():
    with DatabaseCursor() as cur:
        statment = 'SELECT fullname, ST_AREA(geom::geography) * 0.00000038610 sqmiles FROM military_bases ORDER BY sqmiles DESC LIMIT 50'
        cur.execute(statment)
        newResult = cur.fetchall()
        return newResult
      


def adding_areas(arr):
    for i in arr:
        a = i['fullname']
        b = i['sqmiles']
        with DatabaseCursor() as cur:
            statment = "INSERT INTO public.area(fullname, sqmiles) VALUES(%s, %s)"
            cur.execute(statment, [a,b])




def getPoints():

    with DatabaseCursor() as cur:
        statment = "SELECT ST_AsGeoJSON(J.*) FROM (SELECT ST_GeneratePoints(geom, 12, 1996) FROM (SELECT ST_Buffer(ST_GeomFromText('LINESTRING(-129.7844079 19.7433195,-61.9513812 19.7433195 , -61.9513812 54.3457868,-129.7844079 54.3457868)'),1, 'endcap=round join=round')  As geom ) as s )as J"
        #statment = "SELECT ST_AsGeoJSON(J.*) FROM (SELECT ST_GeneratePoints(geom, 12) FROM (SELECT ST_Buffer(ST_GeomFromText('LINESTRING(-129.7844079 19.7433195,-61.9513812 19.7433195 , -61.9513812 54.3457868,-129.7844079 54.3457868, -129.7844079 19.7433195)'),1, 'endcap=round join=round')  As geom ) as s )as J"
        
        cur.execute(statment)
        newResult = cur.fetchall()

        return newResult




def interpolate(a,b,c,d):
    with DatabaseCursor() as cur:
        statment = "SELECT ST_AsGeoJSON(ST_LineInterpolatePoints('LINESTRING(%s %s,%s %s)', 0.01))"
        cur.execute(statment, [a,b,c,d])
        newResult = cur.fetchone()
        return newResult


def addToTable(path):
    with DatabaseCursor() as cur:
        statment = "INSERT INTO public.mypaths(trajectory) VALUES(%s)"
        cur.execute(statment, [path])



def getPaths(points):
    for i in range(len(points)):
        a = points[i][0][0]
        b = points[i][0][1]
        c = points[i][1][0]
        d = points[i][1][1]

        results = interpolate(a,b,c,d)
        results = results['st_asgeojson']
        cleaned = newclean(results)
        cleaned = str(cleaned)
        addToTable(cleaned)



def get_bbox():
    with DatabaseCursor() as cur:
        statment = "SELECT fullname,ST_AsText(ST_Envelope(geom)) bbox, ST_AsText(ST_Centroid(ST_Envelope(geom))) bboxcenter, ST_AsText(ST_Centroid(geom)) center FROM military_bases ORDER BY fullname ASC"
        cur.execute(statment)
        newResult = cur.fetchall()
        return newResult



################################################################################################################
#r = get_bbox()
#print(r[0]['bbox'])

#Replace boxes.bbox with a result from boxes
#statment = 'SELECT fullname from boxes WHERE st_intersects(boxes.bbox, %s)'
def runMe(combinations):
    yesOrNo = []
    #need to pass ccombinations to this
    boxes = get_bbox()
    for i in range(len(boxes)):
        myBox = boxes[i]['bbox']
        for x in range(len(combinations)):
            a = combinations[x][0][0]
            b = combinations[x][0][1]
            c = combinations[x][1][0]
            d = combinations[x][1][1]
            with anotherOne() as cur:
                statment = "SELECT ST_AsText(ST_LineInterpolatePoints('LINESTRING(%s %s,%s %s)', 0.01))"
                cur.execute(statment, [a,b,c,d])
                newResult = cur.fetchall()
            newResult = newResult[0]
            newResult = newResult[0]


            with anotherOne() as cur:
                #statment = 'SELECT fullname from boxes WHERE st_intersects(boxes.bbox, %s)'
                statment = 'SELECT st_intersects(%s, %s)'
                #statment = 'SELECT ST_Contains(%s, %s)'
                cur.execute(statment, [myBox, newResult])
                #cur.execute(statment, [newResult, myBox])
                theResult = cur.fetchall()
                yesOrNo.append(theResult)
            print(theResult)
    return yesOrNo



'''
def getMe(combinations):
    results = []
    for i in range(len(combinations)):
        a = combinations[i][0][0]
        b = combinations[i][0][1]
        c = combinations[i][1][0]
        d = combinations[i][1][1]
        with anotherOne() as cur:
            statment = "SELECT ST_AsText(ST_LineInterpolatePoints('LINESTRING(%s %s,%s %s)', 0.01))"
            cur.execute(statment, [a,b,c,d])
            newResult = cur.fetchall()
            newResult = newResult[0]
            newResult = newResult[0]
            answer = intersects(newResult)
            results.append(answer)
'''
################################################################################################################





def addboxes(aList):
    for i in range(len(aList)):
        with DatabaseCursor() as cur:
            statment = "INSERT INTO public.boxes(fullname, bbox, boxcenter, center) VALUES(%s,%s,%s,%s)"
            a = aList[i]['fullname']
            b = aList[i]['bbox']
            c = aList[i]['bboxcenter']
            d = aList[i]['bboxcenter']
            cur.execute(statment, [a,b,c,d])

#addboxes(c)

#
def intersects(example):
    with DatabaseCursor() as cur:
        statment = 'SELECT fullname from boxes WHERE st_intersects(boxes.bbox, %s)'
        cur.execute(statment, [example])
        newResult = cur.fetchall()
        return newResult




def getMe(combinations):
    results = []
    for i in range(len(combinations)):
        a = combinations[i][0][0]
        b = combinations[i][0][1]
        c = combinations[i][1][0]
        d = combinations[i][1][1]
        with anotherOne() as cur:
            statment = "SELECT ST_AsText(ST_LineInterpolatePoints('LINESTRING(%s %s,%s %s)', 0.01))"
            cur.execute(statment, [a,b,c,d])
            newResult = cur.fetchall()
            newResult = newResult[0]
            newResult = newResult[0]
            answer = intersects(newResult)
            results.append(answer)


    return results




def addToTable(path):
    with DatabaseCursor() as cur:
        statment = "INSERT INTO public.mypaths(trajectory) VALUES(%s)"
        cur.execute(statment, [path])



def main():
    points = getPoints()
    points = points[0]
    points = points['st_asgeojson']
    points = cleanUp(points)
    combinations = combos(points)
    #getPaths(combinations)

    answers = runMe(combinations)
    #print(answers)
    #newFunc(combinations)
    #adding_areas(x)
    #print(intersections) #this is just a test please add it to a table when done

    #intersections = getMe(combinations)
    #print(intersections)
    

    


main()








