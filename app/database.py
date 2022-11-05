from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import config

# "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
user_name = config.settings.database_username
user_password = config.settings.database_password
hostname = config.settings.database_hostname
port = config.settings.database_port
database_name = config.settings.database_name

SQLALCHEMY_DATABASE_URL= f"postgresql://{user_name}:{user_password}@{hostname}/{database_name}"
# SQLALCHEMY_DATABASE_URL= f"postgresql://postgres:@localhost/fastapi"
# Connect to database
Engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
# Declare base for ORM models (create table in database)
Base = declarative_base()

# Dependency
def get_db():
    """
    Create an independent database session/connection per request,
    use the same session through all the request
    and then close it after the request is finished.
    And then a new session will be created for the next request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    print(SQLALCHEMY_DATABASE_URL)