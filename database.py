import boto3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

def get_database_url():
    if os.getenv("ENV") != "production":
        return os.getenv("DATABASE_URL")
    
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.get_secret_value(
        SecretId="home-services/database-url"
    )
    # Secret is stored as plain string, not JSON
    return response["SecretString"]

DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
