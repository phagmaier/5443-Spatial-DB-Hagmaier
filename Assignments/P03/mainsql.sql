-- Create military bases table which has our main information by using the command line and entering:
-- shp2pgsql -s 4326 -I /Users/parkerhagmaier/Desktop/BBBB/tl_2021_us_mil/tl_2021_us_mil.shp militarybases| psql -d testing01 -U parkerhagmaier

CREATE EXTENSION postgis;
CREATE TABLE public.area
(
  fullname varchar(100),
  sqmiles float8
);


CREATE TABLE public.mypaths
(
  trajectory path
);
