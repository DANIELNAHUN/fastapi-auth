from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class FichaInscripcionModel(BaseModel):
    id : Optional[int] = None
    id_sede : Optional[int] = None
    nom_sede: Optional[str] = None
    fecha: Optional[date] = None
    tipo_contrato: Optional[str] = None
    servicio: Optional[str] = None
    num_contrato: Optional[str] = None
    tipo_persona: Optional[str] = None
    tipo_documento: Optional[str] = None
    num_documento : Optional[int] = None
    nombres: Optional[str] = None
    categoria: Optional[str] = None
    zona: Optional[str] = None
    distrito: Optional[str] = None
    telefono: Optional[str] = None
    celulares: Optional[str] = None
    correo: Optional[str] = None
    estado_ficha: Optional[str] = None
    canal_atencion: Optional[str] = None
    vendedor: Optional[str] = None
    fecha_ingreso: Optional[datetime] = None
    nombre_aprobador: Optional[str] = None
    fecha_aprobación: Optional[datetime] = None
    obs_servicio: Optional[str] = None
    obs_vendedor: Optional[str] = None
    mot_desaprobacion: Optional[str] = None
    codigo_abonado : Optional[int] = None
    fecha_inst_catv : Optional[date] = None
    horai_ejec_cable : Optional[str] = None
    horaf_ejec_cable : Optional[str] = None
    fecha_inst_int : Optional[date] = None
    horai_ejec_int : Optional[str] = None
    horaf_ejec_int : Optional[str] = None
    id_ficha : Optional[int] = None
    usuario_ingreso : Optional[str] = None
    paq_inicial : Optional[str] = None
    fecha_insert : Optional[datetime] = None
    fecha_update : Optional[datetime] = None
    class Config:
        orm_mode = True