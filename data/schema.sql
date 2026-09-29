-- Tennis Analytics schema (PostgreSQL)
-- Run in pgAdmin Query Tool while connected to tennis_db

DROP TABLE IF EXISTS competitor_rankings, competitors, venues, complexes, competitions, categories CASCADE;

CREATE TABLE categories (
    category_id   VARCHAR(50)  PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE competitions (
    competition_id   VARCHAR(50)  PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    parent_id        VARCHAR(50),              -- no FK: parents are not in this table
    type             VARCHAR(20)  NOT NULL,
    gender           VARCHAR(10)  NOT NULL,
    level            VARCHAR(30),              -- NULL for most rows (normal)
    category_id      VARCHAR(50)  NOT NULL REFERENCES categories(category_id)
);

CREATE TABLE complexes (
    complex_id   VARCHAR(50)  PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);

CREATE TABLE venues (
    venue_id     VARCHAR(50)  PRIMARY KEY,
    venue_name   VARCHAR(100) NOT NULL,
    city_name    VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_code CHAR(3)      NOT NULL,
    timezone     VARCHAR(100) NOT NULL,
    complex_id   VARCHAR(50)  NOT NULL REFERENCES complexes(complex_id)
);

CREATE TABLE competitors (
    competitor_id VARCHAR(50)  PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    country       VARCHAR(100) NOT NULL,
    country_code  CHAR(3)      NOT NULL,   -- 'UNK' = Neutral athlete
    abbreviation  VARCHAR(10)  NOT NULL
);

CREATE TABLE competitor_rankings (
    rank_id             SERIAL PRIMARY KEY,
    ranking_type        VARCHAR(10) NOT NULL,   -- ATP / WTA
    gender              VARCHAR(10) NOT NULL,
    year                INT NOT NULL,
    week                INT NOT NULL,
    rank                INT NOT NULL,
    movement            INT NOT NULL,
    points              INT NOT NULL,
    competitions_played INT NOT NULL,
    competitor_id       VARCHAR(50) NOT NULL REFERENCES competitors(competitor_id),
    UNIQUE (ranking_type, year, week, competitor_id)
);

CREATE INDEX idx_comp_category ON competitions(category_id);
CREATE INDEX idx_comp_parent   ON competitions(parent_id);
CREATE INDEX idx_comp_type     ON competitions(type);
CREATE INDEX idx_venue_complex ON venues(complex_id);
CREATE INDEX idx_venue_country ON venues(country_name);
CREATE INDEX idx_rank_comp     ON competitor_rankings(competitor_id);
CREATE INDEX idx_rank_rank     ON competitor_rankings(gender, rank);
