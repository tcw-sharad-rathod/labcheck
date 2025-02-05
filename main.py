
from fastapi import FastAPI, Depends, Form ,Query, HTTPException, APIRouter
from sqlalchemy import and_
from sqlalchemy.orm import Session,joinedload


from models.labs import TestOffering, Lab, Test
import math

from external_services.geo_distance import calculate_distance,calculate_distance123 
from database import get_db



app = FastAPI()


#  Get All Labs

@app.get("/home/")
def home():
    return {"message": "Welcome to the Lab Management System!"}


@app.get("/labs/search1234/")
def search_labs(
    db: Session = Depends(get_db),
    category: str = Query(None, description="Category of the lab")
    # min_price: float = Query(None, description="Minimum price of tests available in the lab"),
    # max_price: float = Query(None, description="Maximum price of tests available in the lab"),
    # rating: bool = Query(False, description="Sort by highest rating"),
    # lat: float = Query(None, description="User's latitude for nearby labs"),
    # lon: float = Query(None, description="User's longitude for nearby labs"),
    # sort_by: str = Query("rating", description="Sort by 'rating', 'distance', or 'composite'"),
    # offset: int = Query(10, description="Number of labs to return")
):
    """Fetch labs based on category, rating, location, price range, and sorting method."""
    query = db.query(Lab,Test)

    # Filter by category if provided
    if category:
        query = query.filter(Test.category == category)
        query = query.join(TestOffering, Test.id == TestOffering.lab_id)
        query = query.filter(TestOffering.test_id == Test.id)
        

    # Filter by price range if provided
    # if min_price is not None and max_price is not None:
    #     query = query.filter(and_(Lab.price >= min_price, Lab.price <= max_price))

    # Get all filtered labs
    labs = query.all()

    # If sorting is by rating
    # if sort_by == "rating":
    #     labs = sorted(labs, key=lambda lab: lab.rating, reverse=True)

    # If sorting is by distance and location is provided
    # elif sort_by == "distance" and lat is not None and lon is not None:
    #     user_location = (lat, lon)
    #     labs = sorted(labs, key=lambda lab: calculate_distance(user_location, (lab.latitude, lab.longitude)))

    # If sorting is by composite (both rating and distance)
    # elif sort_by == "composite" and lat is not None and lon is not None:
    #     user_location = (lat, lon)
    #     labs = sorted(
    #         labs, 
    #         key=lambda lab: (-lab.rating, calculate_distance(user_location, (lab.latitude, lab.longitude)))
    #     )

    # return {"labs": labs[: offset]}
# @app.get("/labs/rating_and_location/")
# def get_labs_by_rating_and_location(
#     db: Session = Depends(get_db),
#     lat: float = Query(None, description="Latitude of the user"),
#     lon: float = Query(None, description="Longitude of the user")
# ):
#     if lat is None or lon is None:
#         return db.query(Lab).order_by(Lab.rating.desc()).limit(10).all()
    
#     user_location = (lat, lon)
#     labs = db.query(Lab).all()
    
#     sorted_labs = sorted(
#         labs, key=lambda x: (-calculate_distance(user_location, (x.latitude, x.longitude)), -x.rating)
#     )[:10]
    
#     return {"labs": sorted_labs}

@app.get("/labs/rating_and_location/")
def get_labs_by_rating_and_location(
    db: Session = Depends(get_db),
    lat: float = Query(None, description="Latitude of the user"),
    lon: float = Query(None, description="Longitude of the user")
):
    labs = db.query(Lab).order_by(Lab.rating.desc()).limit(10).all()
    return {"labs": labs}
    
    
@app.get("/labs/nearest/")
def get_nearest_labs(
    db: Session = Depends(get_db),
    lat: float = Query(..., description="User's latitude"),
    lon: float = Query(..., description="User's longitude"),
    limit: int = Query(10, description="Number of labs to return")
):
    """Fetch nearest labs sorted by distance from the user."""
    if lat is None or lon is None:
        return {"error": "Latitude and Longitude are required"}

    user_location = (lat, lon)
    labs = db.query(Lab).all()  # Fetch all labs

    # Sort labs by nearest distance
    sorted_labs = sorted(
        labs, key=lambda lab: calculate_distance123(user_location, (lab.latitude, lab.longitude))
    )[:limit]

    return {"labs": sorted_labs}
    

#  Get Lab by ID
@app.get("/labs-id/")
def get_lab_by_id(lab_id: int, db: Session = Depends(get_db)):
    lab = db.query(TestOffering.test_id).filter(TestOffering.test_id.id == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found.")
    return {"lab": lab}


#  Add New Lab
@app.post("/test_id/")
def create_lab(name: str, address: str, city: str, rating: float, db: Session = Depends(get_db)):
    new_lab = Lab.Lab(name=name, address=address, rating=rating)
    db.add(new_lab)
    db.commit()
    db.refresh(new_lab)
    return {"message": "Lab added successfully!", "lab": new_lab}


#  Get All Tests
@app.get("/tests/")
def get_tests(db: Session = Depends(get_db)):
    tests = db.query(Lab.Test).all()
    return {"tests": tests}

#  Get All Partners
@app.get("/partners/")
def get_partners(db: Session = Depends(get_db)):
    partners = db.query(Lab.Partner).all()
    return {"partners": partners}


# Filter  by Category Test Name and Lab Name =================================================================
@app.get("/labs/filter/")
def search_labs(
    category: str = Query(None, description="Category of the lab"),
    db: Session = Depends(get_db)
):
    """
    Fetch labs based on the category of tests they provide.
    """
    # Get all tests matching the given category
    tests = db.query(Test).filter(Test.category == category).all()

    if not tests:
        return {"message": "No tests found for the given category"}

    # Extract test IDs
    test_ids = [test.id for test in tests]

    # Fetch labs with the list of tests they offer
    labs = (
        db.query(Lab)
        .join(TestOffering, Lab.id == TestOffering.lab_id)
        .filter(TestOffering.test_id.in_(test_ids))
        .distinct()
        .all()
    )

    # Construct response with lab details and their associated tests
    lab_list = []
    for lab in labs:
        lab_tests = (
            db.query(Test)
            .join(TestOffering, Test.id == TestOffering.test_id)
            .filter(TestOffering.lab_id == lab.id, Test.id.in_(test_ids))
            .all()
        )

        lab_list.append({
            "lab_id": lab.id,
            "lab_name": lab.name,
            "lab_address": lab.address,
            "rating": lab.rating,
            "location": lab.address,
            "description": lab.description,
            "working_hours": lab.working_hours,
            "reviews": lab.reviews,
            "tests": [{"test_id": test.id, "test_name": test.name, "short_description": test.short_description, "also_known_as":test.also_known_as, "price":test.price} for test in lab_tests]
        })

    return {"labs": lab_list}



# i all categories with associated tests, no parameters passed  
@app.get("/labs/categories_associate/")
def get_tests_by_category(db: Session = Depends(get_db)):
    """
    Fetch all categories with their associated tests.
    """
    # Get distinct categories from the Test table
    categories = db.query(Test.category).distinct().all()
    
    if not categories:
        return {"message": "No categories found"}

    # Construct response structure
    category_data = {}
    
    for category in categories:
        category_name = category[0]  # Extract category name from tuple
        
        # Fetch all tests under this category
        tests = db.query(Test).filter(Test.category == category_name).all()
        
        # Store test details under the respective category
        category_data[category_name] = [
            {"test_id": test.id, "test_name": test.name}
            for test in tests
        ]

    return {"categories": category_data}

@app.get("/search/")
def search_tests_and_labs(
    query: str = Query(..., description="Search keyword"),
    db: Session = Depends(get_db)
):
    """
    Search for labs and tests by name based on user input.
    The query can be a number or alphabet, and it will search both tables.
    """

    # Search in Tests table
    matching_tests = (
        db.query(Test)
        .filter(Test.name.ilike(f"%{query}%"))
        .all()
    )

    # Search in Labs table
    matching_labs = (
        db.query(Lab)
        .filter(Lab.name.ilike(f"%{query}%"))
        .all()
    )

    return {
        "search_query": query,
        "matching_tests": matching_tests,
        "matching_labs": matching_labs
    }



