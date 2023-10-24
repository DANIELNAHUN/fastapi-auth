import os

from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
engine = create_engine(f"mysql+pymysql://{os.getenv('USER_DB_ETL')}:{os.getenv('PASS_DB_ETL')}@{os.getenv('IP_DB_ETL')}/{os.getenv('NAME_DB_ETL')}")

SessionLocal = sessionmaker(autoflush=False, autocommit =False, bind=engine)
Base = declarative_base()
meta = MetaData()