--Using the command line I did the following to create the table 

-- shp2pgsql -s 4326 -I /Users/parkerhagmaier/Desktop/BBBB/tl_2021_us_state/tl_2021_us_state.shp states| psql -d project02 -U parkerhagmaier

CREATE INDEX idx_states_geom ON public.states USING GIST (the_geom);
