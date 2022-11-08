

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



CREATE TABLE public.missile (
    id numeric NOT NULL PRIMARY KEY,
    name text,
    "speedCat" numeric,
    "blastCat" numeric
);




INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (0, 'Atlas', 1, 7);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (1, 'Harpoon', 2, 8);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (2, 'Hellfire', 3, 7);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (3, 'Javelin', 4, 7);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (4, 'Minuteman', 5, 9);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (5, 'Patriot', 6, 6);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (6, 'Peacekeeper', 7, 6);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (7, 'SeaSparrow', 8, 5);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (8, 'Titan', 8, 5);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (9, 'Tomahawk', 9, 6);
INSERT INTO public.missile (id, name, "speedCat", "blastCat") VALUES (10, 'Trident', 9, 9);








