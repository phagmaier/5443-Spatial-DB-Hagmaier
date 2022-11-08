SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;



CREATE TABLE public.missile_speed (
    category numeric NOT NULL,
    ms numeric,
    mph numeric
);





INSERT INTO public.missile_speed (category, ms, mph) VALUES (1, 111, 248.307);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (2, 222, 496.614);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (3, 333, 744.921);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (4, 444, 993.228);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (5, 555, 1241.535);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (6, 666, 1489.842);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (7, 777, 1738.149);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (8, 888, 1986.456);
INSERT INTO public.missile_speed (category, ms, mph) VALUES (9, 999, 2234.763);




ALTER TABLE ONLY public.missile_speed
    ADD CONSTRAINT missile_speed_pkey PRIMARY KEY (category);