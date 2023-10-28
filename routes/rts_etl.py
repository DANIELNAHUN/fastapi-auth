from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models.auth as m_auth
import models.etl as m_etl
from config.db_etl import SessionLocal as SL_ETL
from config.db_users_api import SessionLocal as SL_API

route_etl = APIRouter()

def get_db_etl():
    db = SL_ETL()
    try:
        yield db
    finally:
        db.close()
db_dependency_etl = Annotated[Session, Depends(get_db_etl)]

def get_db_users():
    db = SL_API()
    try:
        yield db
    finally:
        db.close()
db_dependency_users = Annotated[Session, Depends(get_db_users)]


'''
FICHA INSCRIPCION
'''

@route_etl.get("/abonado-dni/", tags=['ETL Scord2'])
async def get_abonado_by_dni(db: db_dependency_etl, db_2: db_dependency_users, dni: int, token:str):
    usuario = db_2.query(m_auth.Users).filter(m_auth.Users.token == token).first()
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


@route_etl.get("/ventas/", tags=['ETL Scord2'])
async def get_ventas(db: db_dependency_etl, db_2: db_dependency_users, token:str, fecha_i: str, fecha_f:str, vendedor: str = None):
    fecha_f = fecha_f+" 23:59:59"
    usuario = db_2.query(m_auth.Users).filter(m_auth.Users.token == token).first()
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
            "vendedor": ficha.vendedor,
            "fecha_ingreso": ficha.fecha_ingreso,
            "celulares": {f"cel_{i+1}": num.strip() for i, num in enumerate(ficha.celulares.split("/")[:-1]) if num},
            } for ficha in fichas]
    return "Token Invalido"

@route_etl.get("/estado-venta-abonado/", tags=['ETL Scord2'])
async def get_venta_by_abonado(db: db_dependency_etl, db_2: db_dependency_users, token: str, id_sede: int, cod_abonado: int):
    usuario = db_2.query(m_auth.Users).filter(m_auth.Users.token == token).first()
    if usuario is not None:
        os = db.query(m_etl.ordenServicioModel).filter(m_etl.ordenServicioModel.abonado == cod_abonado, m_etl.ordenServicioModel.id_sede == id_sede, m_etl.ordenServicioModel.tipo_os == "INSTALACION SERVICIO").all()
        if not os:
            raise HTTPException(status_code=404, detail=f"No se encontraron Ordenes de Servicio para: {cod_abonado} de la sede {id_sede}")
        return [{
            "id_sede": orden.id_sede,
            "abonado": orden.abonado,
            "nombres": orden.nom_abonado,
            "servicio": orden.servicio,
            "estado_os": orden.estado_os,
            "tecnico_asignado": orden.tec_responsable,
            "tecnico_ejecutor": orden.tec_ejecutor,
            "obs_tecnico": orden.observaciones
            }for orden in os]
    return "Token Invalido"

@route_etl.post("/estado-venta-lista-abonados/", tags=['ETL Scord2'])
async def get_venta_by_lista_abonados(db: db_dependency_etl, db_2: db_dependency_users, token: str, abonados: List[dict]):
    usuario = db_2.query(m_auth.Users).filter(m_auth.Users.token == token).first()
    if usuario is not None:
        ordenes = []
        for ab in abonados:
            cod_abonado = ab['cod_abonado']
            id_sede = ab['id_sede']
            os = db.query(m_etl.ordenServicioModel).filter(m_etl.ordenServicioModel.abonado == cod_abonado, m_etl.ordenServicioModel.id_sede == id_sede, m_etl.ordenServicioModel.tipo_os == "INSTALACION SERVICIO").all()
            if not os:
                ordenes.append(
                    {
                    "id_sede": ab["id_sede"],
                    "abonado": ab['cod_abonado'],
                    "result": "Orden de Instalacion no encontrada"
                    }
                )
            else:
                ordenes.extend(
                    {
                    "id_sede": orden.id_sede,
                    "abonado": orden.abonado,
                    "nombres": orden.nom_abonado,
                    "servicio": orden.servicio,
                    "estado_os": orden.estado_os,
                    "tecnico_asignado": orden.tec_responsable,
                    "tecnico_ejecutor": orden.tec_ejecutor,
                    "obs_tecnico": orden.observaciones,
                    "result": "Orden de Instalacion encontrada"
                    }for orden in os
                )
        return ordenes
    return "Token Invalido"
