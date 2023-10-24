from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models.etl as m_etl
import models.auth as m_auth 

from config.db_etl import SessionLocal
# from routes.rts_auth import oauth_scheme

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

@route_ficha.get("/abonado-dni/", tags=['ETL Scord2'])
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


@route_ficha.get("/ventas-vendedor/", tags=['ETL Scord2'])
async def get_ventas_by_vendedor(db: db_dependency, token:str, fecha_i: str, fecha_f:str, vendedor: str = None):
    fecha_f = fecha_f+" 23:59:59"
    usuario = db.query(m_auth.Users).filter(m_auth.Users.token == token).first()
    if usuario is not None:
        if not vendedor == None:
            fichas = db.query(m_etl.FichaInscripcionModel).filter(m_etl.FichaInscripcionModel.vendedor == vendedor, m_etl.FichaInscripcionModel.fecha_ingreso >= fecha_i, m_etl.FichaInscripcionModel.fecha_ingreso <= fecha_f).all()
        else:
            fichas = db.query(m_etl.FichaInscripcionModel).filter(m_etl.FichaInscripcionModel.fecha_ingreso >= fecha_i, m_etl.FichaInscripcionModel.fecha_ingreso <= fecha_f).all()
        return [{
            "id_ficha": ficha.id_ficha,
            "id_sede": ficha.id_sede,
            "codigo_abonado": ficha.codigo_abonado,
            "nombres": ficha.nombres,
            "estado_ficha": ficha.estado_ficha,
            "fecha_ingreso": ficha.fecha_ingreso,
            "celulares": {f"cel_{i+1}": num.strip() for i, num in enumerate(ficha.celulares.split("/")[:-1]) if num},
            } for ficha in fichas]
    return "Token Invalido"
