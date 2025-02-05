# Defines dependencies


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



DATABASE_URL = "mysql+pymysql://root:root@localhost/lab_tests_db"

# Create Engine
engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Base class for models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
