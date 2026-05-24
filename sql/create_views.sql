DROP VIEW IF EXISTS yearly_temperature;
DROP VIEW IF EXISTS yearly_rain;
DROP VIEW IF EXISTS hot_days;

CREATE VIEW yearly_temperature AS
SELECT
    EXTRACT(YEAR FROM date) AS year,
    AVG(tx) AS avg_max_temperature,
    AVG(tn) AS avg_min_temperature,
    MAX(tx) AS absolute_max_temperature,
    MIN(tn) AS absolute_min_temperature
FROM weather_observations
WHERE date IS NOT NULL
GROUP BY year
ORDER BY year;

CREATE VIEW yearly_rain AS
SELECT
    EXTRACT(YEAR FROM date) AS year,
    SUM(rr) AS total_rain
FROM weather_observations
WHERE date IS NOT NULL
GROUP BY year
ORDER BY year;

CREATE VIEW hot_days AS
SELECT
    EXTRACT(YEAR FROM date) AS year,
    COUNT(*) AS hot_days
FROM weather_observations
WHERE tx >= 30
GROUP BY year
ORDER BY year;