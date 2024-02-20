from sqlalchemy import create_engine
from sqlalchemy.ext.declative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2 #Database driver to make queries
from psycopg2.extras import RealDictCursor
import time
from .config import settings

#connexion string
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/<{settings.database_name}'

#The engine is responsible for establishing the connexion
engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#extend base class to define models
Base = declarative_base()

#Create a session for every request and close it once it's done
def get_db() : 
    db = SessionLocal()
    try:
       yield db
    finally:
       db.close()

