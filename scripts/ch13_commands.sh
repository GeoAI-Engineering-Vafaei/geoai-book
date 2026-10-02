#!/usr/bin/env bash
# Commands typed in the book, chapter ch13.
# Read before running: some lines are alternatives,
# not a script to execute top to bottom.

# --- ۱۳-۷) وارد کردن داده‌ی مکانی به پایگاه‌داده
ogr2ogr -f "PostgreSQL" \
  PG:"host=localhost user=postgres dbname=geoai_db password=***" \
  tehran_districts.gpkg \
  -nln districts -nlt PROMOTE_TO_MULTI \
  -lco GEOMETRY_NAME=geom
