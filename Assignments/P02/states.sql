--Using the command line I did the following to create the table 

-- shp2pgsql -s 4326 -I /Users/parkerhagmaier/Desktop/BBBB/tl_2021_us_state/tl_2021_us_state.shp states| psql -d project02 -U parkerhagmaier

CREATE INDEX idx_states_geom ON public.states USING GIST (the_geom);

--Creating the table throught the command line by the way specfied above also creates an index on the spatial column automatically

SELECT * FROM public.states LIMIT 5;
