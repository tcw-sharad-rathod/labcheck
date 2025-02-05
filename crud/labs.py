# Defines CRUD operations for labs

from sqlalchemy.orm import Session
from sqlalchemy import text
from models.labs import Lab
from external_services.geo_distance import calculate_distance

def get_top_rated_labs(db: Session, pincode: str):
    query = text("""
        SELECT id, name, latitude, longitude, rating
        FROM labs
        WHERE pincode = :pincode
        ORDER BY rating DESC
        LIMIT 10
    """)
    
    result = db.execute(query, {"pincode": pincode}).fetchall()
    return result

def get_labs(db: Session, test_name: str, lat: float, lon: float):
    query = text("""
        SELECT l.id, l.name, l.latitude, l.longitude, lt.price
        FROM labs l
        JOIN lab_tests lt ON l.id = lt.lab_id
        WHERE lt.test_name = :test_name
    """)
    
    result = db.execute(query, {"test_name": test_name}).fetchall()
    
    labs = []
    for row in result:
        lab_data = {
            "id": row.id,
            "name": row.name,
            "latitude": row.latitude,
            "longitude": row.longitude,
            "price": row.price,
            "distance": calculate_distance(lat, lon, row.latitude, row.longitude)
        }
        labs.append(lab_data)
    
    return sorted(labs, key=lambda x: x["distance"])[:50]
