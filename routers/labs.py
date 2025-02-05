# Defines routes for lab-related endpoints

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud.labs import get_top_rated_labs, get_labs_by_test
from schemas.labs import LabSchema, LabWithDistanceSchema

router = APIRouter(prefix="/labs", tags=["Labs"])

@router.get("/top-rated", response_model=list[LabSchema])
def top_rated_labs(pincode: str = Query(...), db: Session = Depends(get_db)):
    labs = get_top_rated_labs(db, pincode)
    if not labs:
        raise HTTPException(status_code=404, detail="No labs found for this pincode")
    return labs

@router.get("/", response_model=list[LabWithDistanceSchema], response_model_exclude_unset=True)
def labs_by_test(
    test_name: str = Query(...),
    lat: float = Query(...),
    lon: float = Query(...),
    db: Session = Depends(get_db)
):
    labs = get_labs_by_test(db, test_name, lat, lon)
    if not labs:
        raise HTTPException(status_code=404, detail="No labs found for this test")
    return labs
