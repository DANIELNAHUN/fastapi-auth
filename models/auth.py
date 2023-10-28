from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer, String, Text

from config.db_users_api import Base


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