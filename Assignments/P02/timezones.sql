--Using the command line I did the following to create the table 

-- shp2pgsql -s 4326 -I INPUTSHAPEFILE.shp TABLENAME| psql -d DATABASENAME -U USERNAME

CREATE INDEX idx_timezones_geom ON public.timezones USING GIST (the_geom);
