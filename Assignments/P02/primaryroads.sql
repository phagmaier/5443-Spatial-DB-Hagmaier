--Using the command line I did the following to create the table 

-- shp2pgsql -s 4326 -I /Users/parkerhagmaier/Desktop/BBBB/tl_2019_us_primaryroads/tl_2019_us_primaryroads.shp primaryroads| psql -d project02 -U parkerhagmaier

CREATE INDEX idx_primaryroads_geom ON public.primaryroads USING GIST (the_geom);

SELECT * FROM public.primaryroads LIMIT 5;
