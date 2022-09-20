--Using the command line I did the following to create the table 

-- shp2pgsql -s 4326 -I /Users/parkerhagmaier/Desktop/BBBB/tl_2021_us_mil/tl_2021_us_mil.shp militarybases| psql -d project02 -U parkerhagmaier

CREATE INDEX idx_militarybases_geom ON public.militarybases USING GIST (the_geom);

--Creating the table throught the command line by the way specfied above also creates an index on the spatial column automatically
SELECT * FROM public.militarybases LIMIT 5;
