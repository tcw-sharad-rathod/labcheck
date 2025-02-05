# # Defines schemas for labs 

from pydantic import BaseModel
from typing import List, Optional

class LabSchema(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    rating: float
    pincode: str
    distance: Optional[float] = None  # Renamed from `calculate_distance`

    class Config:
        orm_mode = True

class LabTestSchema(BaseModel):
    lab_id: int
    test_name: str
    price: float

    class Config:
        orm_mode = True

class LabWithDistanceSchema(LabSchema):
    distance: float  # This will override the Optional[float] in LabSchema

    class Config:
        orm_mode = True
