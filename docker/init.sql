-- Database: ml_data

-- DROP DATABASE ml_data;

CREATE DATABASE ml_data
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

CREATE TABLE public.items
(
    site character varying(100),
    id character varying(100),
    price character varying(100),
    start_time character varying(100),
    name character varying(100),
    description character varying(100),
    nickname character varying(100)
)

ALTER TABLE public.items
    OWNER to postgres;