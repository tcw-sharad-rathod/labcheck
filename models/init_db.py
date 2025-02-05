import sys
import os

# Add the parent directory of 'App' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from App.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")