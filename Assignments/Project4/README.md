# PROJECT 4 Missile Game
This project consisted of two teams the attackers and the defenders. The two teams communicate information through API calls.
The defending team will send a team id to the attackers and the attackers will supply us with a region and and an arsenal. We save each of these 
into a table and then call a the radar sweep every second which is an API call which will give updates on missile positions. 
It is the job of the defenders to use this information to calculate bearing distance and drop rate in order to attempt to intercept the missile before it reaches a 
city in the region. The attacker team introduces randomness to these missiles so that a hit cannot always be guranteed even if an intersection is calculated perfectly. 
When we have all our calculations and believe we can intercept a missile we post to the api a 'solution' which is a json file containing information on where we believe 
the missile will be at what time along with the blast rate and speed of our missile so the attackers can validate that our missile will in fact be where we are claiming
it will be along with stroing that information so they can inform us if the missile was sucesfully intercepted or not. When our arsenal is depleated we call the end game
api or if the attackers are out of enemy missiles they end the game. 


## Files:
### Solutions.py
This file uses psycopg2 so that we can use python to interact with psql. It is this file that handles all API calls, loads/creates tables with information 
supplied to us by the attackers. It is also where all calculations are performed including: calculating the bearing, drop rate, intersection, distance, whether it 
is headed towards a city in our region, and getting the extreme points of our region which will fucntion as our weapon batteries.

### missile_blasts.sql
This file must be run prior to running the program. It contains a foreign key id that tells us what missile is associated with what missile blast radius.

### missile_speed.sql
This file must be run prior to running the program. It contains a foreign key id that tells us what missile is associated with what missile speed.

### missile.sql
This file must be run prior to running the program. It contains basic information about the missile such as foreign keys to it's blast radius and speed along with
the name of the missile.

## Requirments
Python3
PostgresSql
psycopg2
geojson
json 
atexit

## HOW TO RUN:
Run all three sql files before starting the solutions.py file. Edit the login.json file to match your PostgresSql information. Run the Soultions.py file in whatever 
way you prefer either through an editor or through the command line.

