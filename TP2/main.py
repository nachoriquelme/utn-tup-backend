from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import create_db_and_tables
# Importar modelos para asegurar que SQLModel registre todas las tablas
import models  
from routers import autores, libros, prestamos, socios


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="API Sistema de Biblioteca",
    description="Gestión de catálogo, socios y préstamos con FastAPI y SQLModel",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(autores.router)
app.include_router(libros.router)
app.include_router(socios.router)
app.include_router(prestamos.router)
