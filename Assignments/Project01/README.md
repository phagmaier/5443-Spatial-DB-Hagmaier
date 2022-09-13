# Description:
## In this program I loaded data from a csv file to a databse airports using the public schema. 
## I then created an API using fasta api to return three specific pieces of information.
## 1. Return the entire table. To do so go to the /everything endpoint
## 2. Return a specific item from the table by giving the id. To do this go to the /one endpoint of the api
## 3. Enter a longitude and latitude and have the closest geography in the table returned. To do this go to the /closest endpoint of the api
## The functions use to generate the output of these endpoints are titled the same as the endpoint itself. 
## The returned data is generated through psql using psycopg2 in our main.py file to create queries to generate the output.
## we use a class called DatabaseCursor to create a secure connection that only 'turns on' the cursor when a function is being called
## The table creation is done in the sqlmain.sql file
## The api and the three get functions are done in The main.py file
## psycopg2 is used to work with the databse while using python and creating the api
## The original csv file also had to have some data that was stored as null cleaned up since null values were saved as "\N"
## The file reformatCSV.py transforms the data so it is able to be copied into the psql database by eliminating these characters.

#Sources:
## For the cursor used in main: 
## https://github.com/rugbyprof/5443-Spatial-DB/blob/main/Lectures/02_Chap2/main.py
## https://stackoverflow.com/questions/32812463/setting-schema-for-all-queries-of-a-connection-in-psycopg2-getting-race-conditi
## https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit

## Getting the closest geography:
## https://stackoverflow.com/questions/37827468/find-the-nearest-location-by-latitude-and-longitude-in-postgresql

## SQLMain file the template was of how to load data comes from:
## PostGis cookbook 
