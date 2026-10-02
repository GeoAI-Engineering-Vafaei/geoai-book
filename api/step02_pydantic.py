from pydantic import BaseModel, Field
from typing import Optional
class HospitalCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=200) # ... = required
    capacity: int = Field(..., gt=0, le=10000)   # 0 < capacity <= 10000
    has_icu:  bool = False
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    city: Optional[str] = None
