#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the book's light sample-data package.

Everything here is a small clip of a freely available source.  Nothing is
redistributed with the repository: you run this once, it fetches the data
and writes the clips, and the result is a few megabytes that let you run
every code listing in the book end to end.

    python3 sample_data/make_sample_data.py --aoi 51.30 35.65 51.45 35.78

The default area of interest is a small window over Tehran.  Give your own
bounding box (min_lon min_lat max_lon max_lat) to build the package for
your own study area — every notebook in this repository will then run on
your region instead.

What you get:

    s2_small.tif          4 bands (red, NIR, NDVI, slope), 10 m
    dem_small.tif         1 band, SRTM, resampled to the same grid
    roads_small.gpkg      OpenStreetMap road segments inside the AOI
    districts_small.gpkg  administrative polygons inside the AOI
    points_small.csv      sample points with coordinates and a value column

Requires the packages listed in requirements.txt.
"""
import argparse
import csv
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_AOI = (51.30, 35.65, 51.45, 35.78)


def need(module, hint):
    try:
        return __import__(module)
    except ImportError:
        sys.exit("این اسکریپت به %s نیاز دارد. %s" % (module, hint))


def build_points(aoi, path, n=120, seed=42):
    """A small point layer — no download needed, and the values are synthetic.

    The book is explicit that this file is a stand-in (appendix B, table B-4);
    it exists so the tabular examples run, not so anyone models with it.
    """
    rnd = random.Random(seed)
    lon0, lat0, lon1, lat1 = aoi
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "lon", "lat", "slope_deg", "ndvi", "dist_river_m", "label"])
        for i in range(n):
            lon = rnd.uniform(lon0, lon1)
            lat = rnd.uniform(lat0, lat1)
            slope = round(rnd.uniform(0, 25), 2)
            ndvi = round(rnd.uniform(-0.1, 0.75), 3)
            dist = round(rnd.uniform(20, 4000), 1)
            # a deliberately simple, disclosed rule — this is a stand-in, not truth
            label = int(slope < 6 and dist < 900 and ndvi < 0.35)
            w.writerow([i, round(lon, 6), round(lat, 6), slope, ndvi, dist, label])
    print("  wrote %s (%d points, synthetic values — see appendix B)" % (path, n))


def build_osm(aoi, roads_path, districts_path):
    gpd = need("geopandas", "pip install -r requirements.txt")
    import geopandas as gpd  # noqa: F811
    lon0, lat0, lon1, lat1 = aoi
    try:
        import osmnx as ox
    except ImportError:
        print("  osmnx نصب نیست؛ لایه‌های OSM ساخته نشدند.")
        print("  نصب: pip install osmnx   سپس همین اسکریپت را دوباره اجرا کنید.")
        return
    print("  fetching roads from OpenStreetMap ...")
    g = ox.graph_from_bbox(lat1, lat0, lon1, lon0, network_type="drive")
    edges = ox.graph_to_gdfs(g, nodes=False)
    edges = edges[["name", "highway", "length", "geometry"]]
    edges["name"] = edges["name"].astype(str)
    edges["highway"] = edges["highway"].astype(str)
    edges.to_file(roads_path, driver="GPKG")
    print("  wrote %s (%d segments)" % (roads_path, len(edges)))

    print("  fetching administrative polygons ...")
    try:
        adm = ox.features_from_bbox(lat1, lat0, lon1, lon0,
                                    {"boundary": "administrative"})
        adm = adm[adm.geometry.type.isin(["Polygon", "MultiPolygon"])]
        adm = adm[["name", "geometry"]]
        adm["name"] = adm["name"].astype(str)
        adm.to_file(districts_path, driver="GPKG")
        print("  wrote %s (%d polygons)" % (districts_path, len(adm)))
    except Exception as exc:                       # noqa: BLE001
        print("  مرزهای اداری در این محدوده یافت نشد (%s)" % exc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aoi", nargs=4, type=float, metavar=("MIN_LON", "MIN_LAT",
                                                           "MAX_LON", "MAX_LAT"),
                    default=list(DEFAULT_AOI))
    ap.add_argument("--out", default=HERE)
    args = ap.parse_args()
    aoi = tuple(args.aoi)
    os.makedirs(args.out, exist_ok=True)
    print("area of interest: %.4f %.4f %.4f %.4f" % aoi)

    build_points(aoi, os.path.join(args.out, "points_small.csv"))
    build_osm(aoi,
              os.path.join(args.out, "roads_small.gpkg"),
              os.path.join(args.out, "districts_small.gpkg"))

    print("""
باقی‌مانده — دو فایل رستری:

  s2_small.tif و dem_small.tif را نمی‌توان بدون حساب کاربری ساخت، چون
  Copernicus و OpenTopography هر دو ورود می‌خواهند. مسیر دقیق دانلود در
  بخش‌های ۶-۱ و ۶-۳ کتاب و در جدول ب-۱ پیوست ب آمده است؛ پس از دانلود،
  با کد همان بخش‌ها برش بزنید و خروجی را در همین پوشه بگذارید.

  هر دو فایل پس از برش، زیر سه مگابایت می‌شوند.
""")


if __name__ == "__main__":
    main()
