--Using the command line I did the following to create the table 

-- shp2pgsql -s 4326 -I /Users/parkerhagmaier/Desktop/BBBB/tl_2021_us_mil/tl_2021_us_mil.shp militarybases| psql -d project02 -U parkerhagmaier

CREATE INDEX idx_militarybases_geom ON public.militarybases USING GIST (the_geom);
