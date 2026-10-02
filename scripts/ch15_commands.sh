#!/usr/bin/env bash
# Commands typed in the book, chapter ch15.
# Read before running: some lines are alternatives,
# not a script to execute top to bottom.

# --- ۱۵-۲) Dockerfile: دستور ساخت ایمیج
docker build -t geoai-api .          # build the image, tag it "geoai-api"
docker run -p 8000:8000 geoai-api    # run a container, map port 8000

# the API is now reachable at http://localhost:8000/docs
