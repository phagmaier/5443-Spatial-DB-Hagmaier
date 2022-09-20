--Using the command line I did the following to create the table 

-- shp2pgsql -s 4326 -I /Users/parkerhagmaier/Desktop/BBBB/tl_2019_us_rails/tl_2019_us_rails.shp railroads| psql -d project02 -U parkerhagmaier

CREATE INDEX idx_railroads_geom ON public.railroads USING GIST (the_geom);
