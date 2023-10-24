from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import  DateTime, Integer, String, Text, Boolean

from config.db import Base


class Users(Base):
    __tablename__ = 'users_api_etl'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(250))
    passw = Column(Text)
    token = Column(Text)
    fullname = Column(String(250))
    isactive = Column(Boolean)
    fecha_create = Column(DateTime)
    fecha_update = Column(DateTime)
    fecha_delete = Column(DateTime)