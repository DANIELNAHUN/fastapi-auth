from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from config.db_etl import SessionLocal
from sqlalchemy.orm import Session

import models.auth as m_auth 

oauth_scheme = OAuth2PasswordBearer("/api/auth/token")

route_auth = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@route_auth.post("/token/", tags=['Auth'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username, form_data.password)
    return {
        "access_token": "Mi Token Seguro",
        "token_type": "bearer"
    }

@route_auth.get("/security/", tags=['Auth'])
async def test_security(token:str = Depends(oauth_scheme)):
    return "Acceso Permitido"

@route_auth.get("/me", tags=['Auth'])
async def get_user(db: db_dependency, token: str):
    fichas = db.query(m_auth.Users).filter(m_auth.Users.token== token).all()
    return fichas