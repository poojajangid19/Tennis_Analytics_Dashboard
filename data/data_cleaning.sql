-- =====================================================================
-- Tennis Analytics: SQL data cleaning & validation (PostgreSQL)
-- Run in pgAdmin Query Tool on tennis_db AFTER loading the CSVs.
-- Every statement is safe to run more than once.
-- =====================================================================


-- =====================================================================
-- PART 1: DATA QUALITY CHECKS (each should return 0 unless noted)
-- =====================================================================

-- 1.1 Row counts (expected: 18 / 6673 / 778 / 4115 / 1000 / 1000)
SELECT 'categories' AS table_name, COUNT(*) AS row_count FROM categories
UNION ALL SELECT 'competitions',        COUNT(*) FROM competitions
UNION ALL SELECT 'complexes',           COUNT(*) FROM complexes
UNION ALL SELECT 'venues',              COUNT(*) FROM venues
UNION ALL SELECT 'competitors',         COUNT(*) FROM competitors
UNION ALL SELECT 'competitor_rankings', COUNT(*) FROM competitor_rankings;

-- 1.2 Orphan rows (foreign keys should already prevent these)
SELECT COUNT(*) AS competitions_without_category
FROM competitions c LEFT JOIN categories cat USING (category_id)
WHERE cat.category_id IS NULL;

SELECT COUNT(*) AS venues_without_complex
FROM venues v LEFT JOIN complexes cx USING (complex_id)
WHERE cx.complex_id IS NULL;

SELECT COUNT(*) AS rankings_without_competitor
FROM competitor_rankings r LEFT JOIN competitors c USING (competitor_id)
WHERE c.competitor_id IS NULL;

-- 1.3 Text problems: leading/trailing spaces or repeated spaces
SELECT COUNT(*) AS bad_competition_names
FROM competitions
WHERE competition_name <> BTRIM(competition_name) OR competition_name ~ '\s{2,}';

SELECT COUNT(*) AS bad_venue_names
FROM venues
WHERE venue_name <> BTRIM(venue_name) OR venue_name ~ '\s{2,}';

SELECT COUNT(*) AS bad_competitor_names
FROM competitors
WHERE name <> BTRIM(name) OR name ~ '\s{2,}';

-- 1.4 Country codes must be 3 uppercase letters
SELECT COUNT(*) AS bad_venue_country_codes
FROM venues WHERE country_code !~ '^[A-Z]{3}$';

SELECT COUNT(*) AS bad_competitor_country_codes
FROM competitors WHERE country_code !~ '^[A-Z]{3}$';

-- 1.5 Categorical values (review the output; no unexpected labels)
SELECT type,   COUNT(*) FROM competitions GROUP BY type   ORDER BY 2 DESC;
SELECT gender, COUNT(*) FROM competitions GROUP BY gender ORDER BY 2 DESC;

-- 1.6 Numeric sanity checks on rankings
SELECT COUNT(*) AS invalid_ranking_numbers
FROM competitor_rankings
WHERE rank < 1 OR points < 0 OR competitions_played < 0;

-- 1.7 Known, intentional data characteristics (informational)
SELECT COUNT(*) AS top_level_competitions_null_parent
FROM competitions WHERE parent_id IS NULL;                  -- expect 597

SELECT COUNT(*) AS neutral_athletes_unk_country_code
FROM competitors WHERE country_code = 'UNK';                -- expect 49

SELECT COUNT(*) AS complexes_with_no_venues
FROM complexes cx LEFT JOIN venues v USING (complex_id)
WHERE v.venue_id IS NULL;                                   -- expect 160

-- 1.8 Duplicate business keys (venues with same name, city and complex)
SELECT venue_name, city_name, complex_id, COUNT(*) AS copies
FROM venues
GROUP BY venue_name, city_name, complex_id
HAVING COUNT(*) > 1
ORDER BY copies DESC;                                       -- expect 15 groups; different IDs, kept

-- 1.9 Rankings must not mix boards: one row per player per board
SELECT ranking_type, year, week, COUNT(*) AS rows, COUNT(DISTINCT competitor_id) AS players
FROM competitor_rankings
GROUP BY ranking_type, year, week;                          -- ATP 500/500, WTA 500/500


-- =====================================================================
-- PART 2: CLEANING STATEMENTS (idempotent)
-- =====================================================================

-- 2.1 Trim and collapse repeated whitespace
UPDATE competitions
SET competition_name = REGEXP_REPLACE(BTRIM(competition_name), '\s+', ' ', 'g')
WHERE competition_name <> REGEXP_REPLACE(BTRIM(competition_name), '\s+', ' ', 'g');

UPDATE venues
SET venue_name   = REGEXP_REPLACE(BTRIM(venue_name),   '\s+', ' ', 'g'),
    city_name    = REGEXP_REPLACE(BTRIM(city_name),    '\s+', ' ', 'g'),
    country_name = REGEXP_REPLACE(BTRIM(country_name), '\s+', ' ', 'g'),
    timezone     = BTRIM(timezone)
WHERE venue_name   <> REGEXP_REPLACE(BTRIM(venue_name),   '\s+', ' ', 'g')
   OR city_name    <> REGEXP_REPLACE(BTRIM(city_name),    '\s+', ' ', 'g')
   OR country_name <> REGEXP_REPLACE(BTRIM(country_name), '\s+', ' ', 'g')
   OR timezone     <> BTRIM(timezone);

UPDATE complexes
SET complex_name = REGEXP_REPLACE(BTRIM(complex_name), '\s+', ' ', 'g')
WHERE complex_name <> REGEXP_REPLACE(BTRIM(complex_name), '\s+', ' ', 'g');

UPDATE competitors
SET name         = REGEXP_REPLACE(BTRIM(name), '\s+', ' ', 'g'),
    country      = BTRIM(country)
WHERE name    <> REGEXP_REPLACE(BTRIM(name), '\s+', ' ', 'g')
   OR country <> BTRIM(country);

-- 2.2 Standardise case for codes and categorical columns
UPDATE venues      SET country_code = UPPER(BTRIM(country_code)) WHERE country_code <> UPPER(BTRIM(country_code));
UPDATE competitors SET country_code = UPPER(BTRIM(country_code)) WHERE country_code <> UPPER(BTRIM(country_code));
UPDATE competitors SET abbreviation = UPPER(BTRIM(abbreviation)) WHERE abbreviation <> UPPER(BTRIM(abbreviation));

UPDATE competitions
SET type   = LOWER(BTRIM(type)),
    gender = LOWER(BTRIM(gender)),
    level  = LOWER(BTRIM(level))
WHERE type   <> LOWER(BTRIM(type))
   OR gender <> LOWER(BTRIM(gender))
   OR level  <> LOWER(BTRIM(level));

-- 2.3 Empty strings should be real NULLs
UPDATE competitions SET parent_id = NULL WHERE BTRIM(parent_id) = '';
UPDATE competitions SET level     = NULL WHERE BTRIM(level)     = '';

-- 2.4 Neutral athletes have no ISO code in the API: mark them clearly
UPDATE competitors
SET country_code = 'UNK'
WHERE country ILIKE 'neutral' AND country_code <> 'UNK';


-- =====================================================================
-- PART 3: CONSTRAINTS & INDEXES THAT KEEP DATA CLEAN
-- =====================================================================

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'chk_rankings_positive') THEN
        ALTER TABLE competitor_rankings
            ADD CONSTRAINT chk_rankings_positive
            CHECK (rank >= 1 AND points >= 0 AND competitions_played >= 0);
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'chk_competitions_gender') THEN
        ALTER TABLE competitions
            ADD CONSTRAINT chk_competitions_gender
            CHECK (gender IN ('men', 'women', 'mixed'));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'chk_competitions_type') THEN
        ALTER TABLE competitions
            ADD CONSTRAINT chk_competitions_type
            CHECK (type IN ('singles', 'doubles', 'mixed', 'mixed_doubles'));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'chk_venues_country_code') THEN
        ALTER TABLE venues
            ADD CONSTRAINT chk_venues_country_code
            CHECK (country_code ~ '^[A-Z]{3}$');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'chk_competitors_country_code') THEN
        ALTER TABLE competitors
            ADD CONSTRAINT chk_competitors_country_code
            CHECK (country_code ~ '^[A-Z]{3}$');
    END IF;
END $$;


-- =====================================================================
-- PART 4: FINAL VERIFICATION (rerun Part 1 and confirm)
-- =====================================================================
-- Expected: bad_* counts = 0, invalid_ranking_numbers = 0,
--           rows per table = 18 / 6673 / 778 / 4115 / 1000 / 1000
ANALYZE;   -- refresh planner statistics after loading and cleaning
