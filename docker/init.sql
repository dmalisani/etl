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

-- Table: public.items

-- DROP TABLE public.items;

CREATE TABLE public.items
(
    site character varying(100) COLLATE pg_catalog."default",
    id character varying(100) COLLATE pg_catalog."default",
    price character varying(100) COLLATE pg_catalog."default",
    start_time character varying(100) COLLATE pg_catalog."default",
    name character varying(100) COLLATE pg_catalog."default",
    description character varying(100) COLLATE pg_catalog."default",
    nickname character varying(100) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public.items
    OWNER to postgres;
