from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models.etl as m_etl
import models.auth as m_auth 

from config.db import SessionLocal
from routes.rts_auth import oauth_scheme

route_ficha = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


'''
FICHA INSCRIPCION
'''

@route_ficha.get("/ficha-inscripcion/", tags=['ETL Scord2'])
async def get_abonado_by_dni(db: db_dependency, dni: int, token:str):
    usuario = db.query(m_auth.Users).filter(m_auth.Users.token == token).first()
    if usuario is not None:
        fichas = db.query(m_etl.FichaInscripcionModel).filter(m_etl.FichaInscripcionModel.num_documento == dni, m_etl.FichaInscripcionModel.estado_ficha == "APROBADO").all()
        if not fichas:
            fichas = db.query(m_etl.FichaInscripcionModel).filter(m_etl.FichaInscripcionModel.num_documento == dni, m_etl.FichaInscripcionModel.estado_ficha == "EN EVALUACION").all()
            if not fichas:
                fichas = db.query(m_etl.FichaInscripcionModel).filter(m_etl.FichaInscripcionModel.num_documento == dni, m_etl.FichaInscripcionModel.estado_ficha == "DESAPROBADO").all()
                if not fichas:
                    raise HTTPException(status_code=404, detail=f"No existe una Ficha creada con el dni: {dni}")
                return [{"id_ficha": ficha.id_ficha, "mot_desaprobacion": ficha.mot_desaprobacion, "estado_ficha": ficha.estado_ficha} for ficha in fichas]
            return [{"id_ficha": ficha.id_ficha, "id_sede": ficha.id_sede, "estado_ficha": ficha.estado_ficha} for ficha in fichas]
        return [{"id_ficha": ficha.id_ficha, "id_sede": ficha.id_sede, "codigo_abonado": ficha.codigo_abonado, "estado_ficha": ficha.estado_ficha} for ficha in fichas]
    return "Token Invalido"
