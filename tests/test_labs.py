 # Test file for labs API

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)  

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to LabsCheck API"}

def test_top_rated_labs():
    response = client.get("/labs/top-rated?pincode=110001")
    assert response.status_code in [200, 404]

def test_labs_by_test():
    response = client.get("/labs/?test_name=ECG&lat=28.6139&lon=77.2090")
    assert response.status_code in [200, 404]


