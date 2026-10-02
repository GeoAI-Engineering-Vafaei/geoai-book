-- ۱۳-۲) PostgreSQL و زبان SQL
CREATE TABLE hospitals (
    id       SERIAL PRIMARY KEY,          -- auto-increment unique id
    name     VARCHAR(200)     NOT NULL,
    capacity INTEGER          NOT NULL,
    has_icu  BOOLEAN          DEFAULT FALSE,
    lat      DOUBLE PRECISION NOT NULL,
    lon      DOUBLE PRECISION NOT NULL,
    city     VARCHAR(100)
);

INSERT INTO hospitals (name, capacity, has_icu, lat, lon, city)
VALUES ('Milad',    1000, TRUE, 35.7350, 51.3650, 'Tehran'),
       ('Shariati',  450, TRUE, 35.7400, 51.4200, 'Tehran'),
       ('Namazi',    800, TRUE, 29.6320, 52.5400, 'Shiraz');

SELECT name, capacity
FROM hospitals
WHERE capacity > 500;

-- ۱۳-۲) PostgreSQL و زبان SQL
SELECT city, COUNT(*) AS hospital_count, SUM(capacity) AS total_beds
FROM hospitals
GROUP BY city
ORDER BY total_beds DESC;

-- ۱۳-۳) پیوند جداول: JOIN و کلید خارجی
SELECT h.name AS hospital, h.capacity, c.name AS city, c.population
FROM hospitals h
INNER
JOIN cities c
ON h.city_id = c.id;

-- ۱۳-۴) قلب ماجرا: توابع مکانی PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;
ALTER TABLE hospitals ADD COLUMN geom GEOMETRY(POINT, 4326);
UPDATE hospitals
SET geom = ST_SetSRID(ST_MakePoint(lon, lat), 4326);

-- ۱۳-۴) قلب ماجرا: توابع مکانی PostGIS
-- distance from a point, in km (::geography = treat as a sphere)
SELECT name,
       ST_Distance(
           geom::geography,
           ST_SetSRID(ST_MakePoint(51.40, 35.72), 4326)::geography
       ) / 1000 AS distance_km
FROM hospitals
ORDER BY distance_km;

-- hospitals within 5 km of a point (very fast with an index)
SELECT name, capacity
FROM hospitals
WHERE ST_DWithin(
          geom::geography,
          ST_SetSRID(ST_MakePoint(51.40, 35.72), 4326)::geography,
          5000);

-- ۱۳-۵) قانون طلایی سرعت: ایندکس GiST
CREATE INDEX idx_hospitals_geom
ON hospitals
USING GIST(geom);

-- ۱۳-۶) سامانه‌های مرجع مختصات (SRID)
-- exact area of a polygon, in square km (transform to metric UTM first)
SELECT name, ST_Area(ST_Transform(geom, 32639)) / 1000000 AS area_km2
FROM districts;

-- ۱۳-۱۰) پروژه‌ی فصل: تحلیل صنعتی دسترسی و آماده‌سازی برای سرویس سیل
CREATE INDEX IF NOT EXISTS idx_hospitals_geom
ON hospitals
USING GIST(geom);

-- a single SQL query that the API will call on every request:
SELECT name, capacity,
       ST_Distance(
           geom::geography,
           ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography
       ) AS dist_m
FROM hospitals
WHERE ST_DWithin(
          geom::geography,
          ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
          :radius)
ORDER BY dist_m;
