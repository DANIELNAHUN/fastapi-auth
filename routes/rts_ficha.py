from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models.mdl_ficha as m_ficha
from config.db import SessionLocal

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

@route_ficha.get("/api/etl/ficha-inscripcion/", tags=['ETL Scord2'])
async def get_abonado_by_dni(db: db_dependency, dni: int, token: str = Depends()):
    fichas = db.query(m_ficha.FichaInscripcionModel).filter(m_ficha.FichaInscripcionModel.num_documento == dni, m_ficha.FichaInscripcionModel.estado_ficha == "APROBADO").all()
    if not fichas:
        fichas = db.query(m_ficha.FichaInscripcionModel).filter(m_ficha.FichaInscripcionModel.num_documento == dni, m_ficha.FichaInscripcionModel.estado_ficha == "EN EVALUACION").all()
        if not fichas:
            fichas = db.query(m_ficha.FichaInscripcionModel).filter(m_ficha.FichaInscripcionModel.num_documento == dni, m_ficha.FichaInscripcionModel.estado_ficha == "DESAPROBADO").all()
            if not fichas:
                raise HTTPException(status_code=404, detail=f"No existe una Ficha creada con el dni: {dni}")
            return [{"id_ficha": ficha.id_ficha, "mot_desaprobacion": ficha.mot_desaprobacion, "estado_ficha": ficha.estado_ficha} for ficha in fichas]
        return [{"id_ficha": ficha.id_ficha, "id_sede": ficha.id_sede, "estado_ficha": ficha.estado_ficha} for ficha in fichas]
    return [{"id_ficha": ficha.id_ficha, "id_sede": ficha.id_sede, "codigo_abonado": ficha.codigo_abonado, "estado_ficha": ficha.estado_ficha} for ficha in fichas]
