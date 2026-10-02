#!/usr/bin/env bash
# Commands typed in the book, chapter appendix.
# Read before running: some lines are alternatives,
# not a script to execute top to bottom.

# --- ب-۱) داده‌ی پایه: چه چیزی، از کجا، چقدر
# once: install the cutter (linux/mac; on windows use WSL or osmconvert)
# sudo apt install osmium-tool      # or:  brew install osmium-tool

# cut a bounding box out of the country extract.
# order is: left,bottom,right,top  in plain lon/lat degrees.
# the box below is roughly greater Tehran -- replace with your own.
osmium extract \
  --bbox 51.10,35.55,51.65,35.85 \
  --set-bounds \
  -o data/raw/study_area.osm.pbf \
  data/raw/iran.osm.pbf

# 300 MB in, a handful of MB out. every later step reads the small file:
#   from pyrosm import OSM
#   osm = OSM('data/raw/study_area.osm.pbf')
#   roads = osm.get_network(network_type='driving')

# --- ب-۲) قرارداد پوشه‌بندی: سه پوشه، نه بیشتر
mkdir -p GeoAI/data GeoAI/work GeoAI/out
# data/ : raw downloads, never edited by hand
# work/ : clipped, reprojected and intermediate files
# out/  : final maps, saved models, GeoJSON you hand in
