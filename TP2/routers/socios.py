from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from auth import UsuarioActual, get_current_user, require_bibliotecario
from database import get_session
from models.prestamo import PrestamoRead
from models.socio import SocioCreate, SocioRead, SocioUpdate
from services import prestamo_service, socio_service

router = APIRouter(prefix="/socios", tags=["Socios"])

@router.post("", response_model=SocioRead, status_code=status.HTTP_201_CREATED)
def crear_socio(
    data: SocioCreate,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    return socio_service.crear_socio(session, data)


@router.get("", response_model=List[SocioRead])
def listar_socios(
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    return socio_service.listar_socios(session)


@router.get("/{socio_id}", response_model=SocioRead)
def obtener_socio(
    socio_id: int,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    return socio_service.obtener_socio(session, socio_id)


@router.put("/{socio_id}", response_model=SocioRead)
def actualizar_socio(
    socio_id: int,
    data: SocioUpdate,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    return socio_service.actualizar_socio(session, socio_id, data)


@router.delete("/{socio_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_socio(
    socio_id: int,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    socio_service.eliminar_socio(session, socio_id)


@router.get("/{socio_id}/prestamos", response_model=List[PrestamoRead])
def listar_prestamos_socio(
    socio_id: int,
    activos: Optional[bool] = Query(default=None),
    session: Session = Depends(get_session),
    current_user: UsuarioActual = Depends(get_current_user),
):
    return prestamo_service.listar_prestamos_socio_autorizado(
        session, socio_id, current_user=current_user, activos=activos
    )