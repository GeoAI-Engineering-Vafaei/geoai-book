from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from dependencies import get_db

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.get("/nearest-hospitals")     # a read-only search -> GET
def nearest_hospitals(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10, gt=0, le=100),
    db: Session = Depends(get_db),
):
    sql = text("""
        SELECT name, capacity,
               ST_Distance(geom::geography,
                   ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography
               ) / 1000 AS km
        FROM hospitals
        WHERE ST_DWithin(geom::geography,
                  ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography, :r)
        ORDER BY km
        LIMIT 10
    """)
    rows = db.execute(sql, {"lon": lon, "lat": lat,
                            "r": radius_km * 1000}).mappings().all()
    return {"count": len(rows), "results": [dict(r) for r in rows]}
