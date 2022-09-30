# PROJECT 3

# FOUND PROBLEM:
## Did not take into account the difference and necesity of using gography not geometry and converting betweent the two
## Or at least I think this is part of the problem 
## Will fix tomorow and also fix my code because it is embarassingly bad
## Mostly writing this in case DR. Griffin is reading this in which case sorry this should have been obvious I don't know why i'm strugguling so much with this stuff

# STILL NEED TO UPDATE CODE WHAT IS IN HERE IS NOT UPDATED
# STILL cannot get any intersections although my code will run and show that I am getting no hits so I assume that means my code is fine but I can not get intersections with random lines so something must be wrong

# OVERVIEW
## In this assignemnt I used a bounding box around the United States
## and from that we generate random points around the edge of the bounding box
## Once we get these points we get all non repeating combinations from these points
## These combinations are then turned into multi point line strings 
## And then saved into a table where all these paths will be stored
## We will also store the area for the 50 largest military bases in a seperate table
## with the idea behind it being to find if these lines intersect any of the locations of the military bases

# Message about output:
## My pg admin is not working for some reason and the data displays horribly on my terminal
## I could output one column at a time from each table but I would rather not take all those screenshots
## If this is problematic please let me know and I will show you my results in class to show you that I have 
## actually completed the assignment and didn't 'fudge' anything

# Requirments:
## PostgreSQL
## psycopg2
## python3

# Files:
## main.py :
### Description of main.py
#### Using pythin and psycopg2 to connect to psql we will query our military bases data
#### create data to store into other tables and we will also clean some of the results of our
#### results from psql using python and also generate combinations with python

## mainsql.sql:
### Description of mainsql.sql
#### Simply create the three tables where we will store our data
