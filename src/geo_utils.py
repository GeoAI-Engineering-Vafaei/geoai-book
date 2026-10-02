"""GeoAI Toolkit - basic helpers for spatial analysis. v1.0"""
from math import radians, sin, cos, sqrt, asin

EARTH_RADIUS_KM = 6371

def validate_coordinates(lat, lon):
    """Return True if the coordinate is within valid ranges."""
    return -90 <= lat <= 90 and -180 <= lon <= 180

def haversine(lat1, lon1, lat2, lon2):
    """Great-circle distance in km; raises on invalid input."""
    if not (validate_coordinates(lat1, lon1)
            and validate_coordinates(lat2, lon2)):
        raise ValueError("invalid coordinates")
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return EARTH_RADIUS_KM * 2 * asin(sqrt(a))

def create_buffer_box(lat, lon, radius_km):
    """Return the bounding box around a point.

    North-south is a constant 111 km per degree, but east-west shrinks
    towards the poles, so the longitude step is divided by cos(lat).
    """
    d_lat = radius_km / 111
    d_lon = radius_km / (111 * cos(radians(lat)))
    return {
        "north": lat + d_lat,
        "south": lat - d_lat,
        "east": lon + d_lon,
        "west": lon - d_lon,
    }

def find_nearest(target, candidates, top_n=3):
    """Return the top_n nearest candidates to the target point."""
    out = []
    for c in candidates:
        try:
            d = haversine(target["lat"], target["lon"], c["lat"], c["lon"])
            out.append({**c, "distance": d})
        except (ValueError, KeyError):
            continue   # skip dirty records
    out.sort(key=lambda x: x["distance"])
    return out[:top_n]
