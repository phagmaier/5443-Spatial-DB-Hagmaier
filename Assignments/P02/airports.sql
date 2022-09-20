

CREATE TABLE public.airports
(
  id int,
  name varchar(255),
  city varchar(255),
  country varchar(255),
  three_code varchar(3),
  four_code varchar(4),
  lat float8,
  lon float8,
  elevation int,
  gmt float,
  tz_short varchar(1),
  time_zone varchar(255),
  typee varchar(8),
  the_geom geometry(POINT, 4326)
);


COPY public.airports (id, name, city, country, three_code, four_code, lat, lon, elevation, gmt, tz_short, time_zone, typee) 
FROM '/Users/parkerhagmaier/Desktop/AAAA/newAirports.csv'
WITH CSV HEADER;



UPDATE public.airports SET the_geom = ST_SetSRID(ST_MakePoint(lon,lat), 4326);

UPDATE public.airports SET the_geom = ST_PointFromText('POINT(' || lon || ' ' || lat || ')', 4326);


CREATE INDEX idx_airports_geom ON public.airports USING GIST (the_geom);

SELECT * FROM public.airports LIMIT 5;
