import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", os.getenv("LOCAL_DB_URL"))
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

Base = declarative_base()
