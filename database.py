from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Update your PostgreSQL database URL
# SQLALCHEMY_DATABASE_URL = "postgresql://admin:12345Rs@localhost:8568/postgres"
SQLALCHEMY_DATABASE_URL = "sqlite:///blog.db"

# Create the PostgreSQL engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()









