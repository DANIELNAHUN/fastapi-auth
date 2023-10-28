from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.rts_auth import route_auth
from routes.rts_etl import route_etl

load_dotenv()

app = FastAPI(
  title="API ETL-APK",
  version="1.0",
  description="Conexion ETL con aplicativo de ventas",
  contact={
    "name":"Daniel Calcina",
    "email": "danielnahuncalcinafuentes@gmail.com"
  }
)

origins = [
  "https://localhost",
  "https://localhost:8081",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins = origins,
  allow_credentials = True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(route_etl, prefix='/api/etl')
# app.include_router(route_auth, prefix='/api/auth')