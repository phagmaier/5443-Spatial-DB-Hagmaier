missile_blast.sqlSET statement_timeout = 0;
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



CREATE TABLE public.missile_blast (
    cat numeric NOT NULL,
    blast_radius numeric
);




INSERT INTO public.missile_blast (cat, blast_radius) VALUES (1, 100.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (2, 150.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (3, 200.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (4, 250.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (5, 300.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (6, 350.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (7, 400.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (8, 450.0000000000000000);
INSERT INTO public.missile_blast (cat, blast_radius) VALUES (9, 500.0000000000000000);



ALTER TABLE ONLY public.missile_blast
    ADD CONSTRAINT missile_blast_pkey PRIMARY KEY (cat);