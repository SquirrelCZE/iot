

CREATE TABLE public.spot (
	tag varchar PRIMARY KEY,
	name varchar NOT NULL
);
ALTER TABLE public.spot OWNER TO pi;
INSERT INTO public.spot(tag,name) VALUES ('BCN1', 'Balcon 1');

CREATE TABLE public.light (
    id SERIAL PRIMARY KEY,
    value integer NOT NULL,
    spot_tag varchar NOT NULL REFERENCES public.spot (tag),
    measured_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE public.light OWNER TO pi;
ALTER TABLE public.light_id_seq OWNER TO pi;

CREATE TABLE public.pressure (
    id SERIAL PRIMARY KEY,
    value real NOT NULL,
    spot_tag varchar NOT NULL REFERENCES public.spot (tag),
    measured_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE public.pressure OWNER TO pi;
ALTER TABLE public.pressure_id_seq OWNER TO pi;


CREATE TABLE public.temp (
    id SERIAL PRIMARY KEY,
    value real NOT NULL,
    spot_tag varchar NOT NULL REFERENCES public.spot (tag),
    measured_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE public.temp OWNER TO pi;
ALTER TABLE public.temp_id_seq OWNER TO pi;

CREATE TABLE public.device (
    id SERIAL PRIMARY KEY,
    name varchar NOT NULL
);
GRANT SELECT ON TABLE public.device TO PUBLIC;

CREATE TYPE event_type AS ENUM ('update', 'reboot');
CREATE TABLE public.events (
    id SERIAL PRIMARY KEY,
    etype event_type NOT NULL,
    device integer REFERENCES public.device(id),
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    finished boolean NOT NULL DEFAULT false
);
GRANT SELECT ON TABLE public.events TO PUBLIC;


GRANT SELECT ON TABLE public.light TO grafana;
GRANT SELECT ON TABLE public.pressure TO grafana;
GRANT SELECT ON TABLE public.temp TO grafana;

