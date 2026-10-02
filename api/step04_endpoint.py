import joblib, numpy as np
from fastapi import APIRouter, Query

router = APIRouter(prefix="/predict", tags=["flood"])

# load ONCE at startup, not on every request
model = joblib.load("rf_flood.pkl")

@router.get("/flood-risk")           # a read-only prediction -> GET
def predict_flood_risk(
    slope: float = Query(..., ge=0, le=90),          # degrees
    ndvi: float = Query(..., ge=-1, le=1),
    dist_river_m: float = Query(..., ge=0),          # metres to a river
    elevation: float = Query(..., ge=-500, le=9000), # metres a.s.l.
):
    """Return the flood-risk probability for one location."""
    features = np.array([[slope, ndvi, dist_river_m, elevation]])
    prob = float(model.predict_proba(features)[0][1])   # P(flood)
    level = ("high" if prob > 0.66
             else "medium" if prob > 0.33
             else "low")
    return {"flood_probability": round(prob, 3), "risk_level": level}

# call it straight from the browser:
#   http://127.0.0.1:8000/predict/flood-risk
#       ?slope=3.4&ndvi=0.21&dist_river_m=180&elevation=1180
