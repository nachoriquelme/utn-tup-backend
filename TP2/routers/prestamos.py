from typing import Optional
from fastapi import APIRouter, Body, Depends, status
from sqlmodel import Session

from auth import UsuarioActual, require_bibliotecario
from database import get_session
from models.prestamo import PrestamoCreate, PrestamoDevolucionRequest, PrestamoRead
from services import prestamo_service

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])

@router.post("", response_model=PrestamoRead, status_code=status.HTTP_201_CREATED)
def crear_prestamo(
    data: PrestamoCreate,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    return prestamo_service.registrar_prestamo(session, data)


@router.post("/{prestamo_id}/devolucion", response_model=PrestamoRead)
def devolver_prestamo(
    prestamo_id: int,
    body: Optional[PrestamoDevolucionRequest] = Body(default=None),
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    fecha_dev = body.fecha_devolucion if body else None
    return prestamo_service.registrar_devolucion(
        session, prestamo_id, fecha_devolucion=fecha_dev
    )