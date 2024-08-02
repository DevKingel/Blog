CREATE table IF NOT EXISTS posts (
    id  INTEGER CONSTRAINT pk_id PRIMARY KEY,
    title   VARCHAR(100) NOT NULL,
    description TEXT
);