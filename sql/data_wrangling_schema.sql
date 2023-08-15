/*
DROP TABLE nodes CASCADE;
DROP TABLE nodes_tags CASCADE;
DROP TABLE ways CASCADE;
DROP TABLE ways_tags CASCADE;
DROP TABLE ways_nodes CASCADE;
*/

CREATE TABLE nodes (
    id BIGINT PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    _user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TIMESTAMP
);

CREATE TABLE nodes_tags (
    id BIGINT,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);

CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    _user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TIMESTAMP
);

CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);

CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id BIGINT NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);

GRANT ALL ON TABLE public.nodes TO project_user;

GRANT ALL ON TABLE public.nodes_tags TO project_user;

GRANT ALL ON TABLE public.ways TO project_user;

GRANT ALL ON TABLE public.ways_nodes TO project_user;

GRANT ALL ON TABLE public.ways_tags TO project_user;