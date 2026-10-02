from fastapi import HTTPException, status

@app.get("/hospitals/{hid}")
def get_hospital(hid: int, db: Session = Depends(get_db)):
    row = db.execute(text("SELECT * FROM hospitals WHERE id = :id"),
                     {"id": hid}).fetchone()
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"hospital {hid} not found")
    return row._mapping
