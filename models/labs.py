# Defines database models for labs, tests, categories, test_offerings, partners, and customers

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database import Base

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    short_description = Column(String)

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    short_description = Column(String)
    long_description = Column(String)
    also_known_as = Column(String)
    category = Column(String)
    price = Column(Float, nullable=False)

class Lab(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    google_map_id = Column(String)
    latitude = Column(Float)   
    longitude = Column(Float)
    working_hours = Column(String)
    rating = Column(Float)
    reviews = Column(Integer, default=0)
    description = Column(String)
    pincode = Column(String)
    
class TestOffering(Base):
    __tablename__ = "test_offerings"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"))
    lab_id = Column(Integer, ForeignKey("labs.id"))
    price = Column(Float, nullable=False)

class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mobile_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    lab_id = Column(Integer, ForeignKey("labs.id"))

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mobile_number = Column(String, unique=True, nullable=False)
    auth_type = Column(String, nullable=False)

# 


