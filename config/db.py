import os

from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(f"mysql+pymysql://{os.getenv('USER_DB')}:{os.getenv('PASS_DB')}@{os.getenv('IP_DB')}/{os.getenv('NAME_DB')}")

SessionLocal = sessionmaker(autoflush=False, autocommit =False, bind=engine)
Base = declarative_base()
meta = MetaData()