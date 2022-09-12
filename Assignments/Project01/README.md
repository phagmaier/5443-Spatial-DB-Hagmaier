# Description:
## In this program I loaded data from a csv file to a databse firenews using the public schema. 
## I then created an API using fasta api to return three specific pieces of information.
## 1. Return the entire table. 
## 2. Return a specific item from the table by giving the id
## 3. Enter a longitude and latitude and have the closest geography in the table returned
## The table creation is done in the sqlmain.sql file
## The api and the three get functions are done in The main.py file
## psycopg2 is used to work with the databse while using python and creating the api
