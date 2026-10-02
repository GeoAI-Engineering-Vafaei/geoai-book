#!/usr/bin/env bash
# Commands typed in the book, chapter ch12.
# Read before running: some lines are alternatives,
# not a script to execute top to bottom.

# --- ۱۲-۲) نصب پایتون روی سیستم شخصی
python --version      # e.g. Python 3.12.0
python3 --version     # on macOS / Linux

# --- ۱۲-۴) محیط‌های مجازی: پایان جهنم وابستگی‌ها
mkdir geoai_project && cd geoai_project
python -m venv venv            # create an isolated environment

venv\Scripts\activate          # activate it - Windows
source venv/bin/activate       # activate it - macOS / Linux
# the prompt now starts with (venv). to leave it again:
deactivate

# --- ۱۲-۶) کنترل نسخه با Git
git init   # start tracking this folder
git add .   # stage all changed files
git commit -m "add haversine function"   # save a snapshot with a message
git status   # what changed since the last commit?
git log --oneline   # the history of commits

# --- ۱۲-۷) GitHub: مخزن شما روی ابر و رزومه‌ی شما
git remote add origin https://github.com/username/geoai-toolkit.git
git branch -M main
git push -u origin main   # upload your commits to GitHub

# --- ۱۲-۸) پروژه‌ی فصل: انتشار حرفه‌ای geo_utils
git init
git add .
git commit -m "first release of geoai-toolkit"
git remote add origin https://github.com/username/geoai-toolkit.git
git branch -M main
git push -u origin main
