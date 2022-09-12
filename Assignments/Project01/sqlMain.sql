-- From POSTGIS cookbook Ch1 with some edits 
--Also Added an index to the origanal table to help with queries

CREATE EXTENSION postgis;
CREATE TABLE public.firenews
(
  x float8,
  y float8,
  place varchar(100),
  size float8,
  update date,
  startdate date,
  enddate date,
  title varchar(255),
  url varchar(255),
  the_geom geometry(POINT, 4326),
  id int
);

COPY public.firenews (x, y, place, size, update, startdate, enddate, title, url, id) 
FROM '/Users/parkerhagmaier/Desktop/AAAA/blank.csv' 
WITH CSV HEADER;

SELECT f_table_name, f_geometry_column, coord_dimension, srid, type 
FROM geometry_columns 
where f_table_name = 'firenews';

UPDATE public.firenews SET the_geom = ST_SetSRID(ST_MakePoint(x,y), 4326);

UPDATE public.firenews SET the_geom = ST_PointFromText('POINT(' || x || ' ' || y || ')', 4326);

CREATE INDEX idx_firenews_geom ON public.firenews USING GIST (the_geom);
