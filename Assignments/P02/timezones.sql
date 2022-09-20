--Using the command line I did the following to create the table 

-- shp2pgsql -s 4326 -I /Users/parkerhagmaier/Desktop/BBBB/ne_10m_time_zones/ne_10m_time_zones.shp timezones| psql -d project02 -U parkerhagmaier

CREATE INDEX idx_timezones_geom ON public.timezones USING GIST (the_geom);

--Creating the table throught the command line by the way specfied above also creates an index on the spatial column automatically
SELECT * FROM public.timezones LIMIT 5;
