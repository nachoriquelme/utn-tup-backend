from datetime import date, timedelta
from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session

from auth import Rol, UsuarioActual
from models.prestamo import Prestamo, PrestamoCreate
from repositories.prestamo_repository import PrestamoRepository
from services.libro_service import obtener_libro
from services.socio_service import obtener_socio

MAX_PRESTAMOS_ACTIVOS = 3
PLAZO_DIAS = 14
MULTA_POR_DIA = 100.0


def registrar_prestamo(session: Session, data: PrestamoCreate) -> Prestamo:
    repo = PrestamoRepository(session)
    socio = obtener_socio(session, data.socio_id)
    libro = obtener_libro(session, data.libro_id)

    if not socio.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El socio se encuentra inactivo y no puede solicitar préstamos",
        )

    cantidad_activos = repo.count_activos_by_socio(socio.id)
    if cantidad_activos >= MAX_PRESTAMOS_ACTIVOS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El socio ya alcanzó el límite máximo de {MAX_PRESTAMOS_ACTIVOS} préstamos activos",
        )

    if libro.stock <= 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El libro '{libro.titulo}' no tiene stock disponible",
        )

    fecha_inicio = data.fecha_prestamo or date.today()
    fecha_venc = fecha_inicio + timedelta(days=PLAZO_DIAS)

    libro.stock -= 1
    prestamo = Prestamo(
        socio_id=socio.id,
        libro_id=libro.id,
        fecha_prestamo=fecha_inicio,
        fecha_vencimiento=fecha_venc,
        fecha_devolucion=None,
        multa=0.0,
    )

    return repo.create_with_stock_update(prestamo, libro)


def registrar_devolucion(
    session: Session,
    prestamo_id: int,
    fecha_devolucion: Optional[date] = None,
) -> Prestamo:
    repo = PrestamoRepository(session)
    prestamo = repo.get_by_id(prestamo_id)
    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Préstamo con id {prestamo_id} no encontrado",
        )

    if prestamo.fecha_devolucion is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este préstamo ya fue devuelto previamente",
        )

    fecha_efectiva = fecha_devolucion or date.today()
    dias_atraso = max(0, (fecha_efectiva - prestamo.fecha_vencimiento).days)
    prestamo.multa = float(dias_atraso * MULTA_POR_DIA)
    prestamo.fecha_devolucion = fecha_efectiva

    libro = obtener_libro(session, prestamo.libro_id)
    libro.stock += 1

    return repo.update_with_stock_update(prestamo, libro)


def listar_prestamos_socio(
    session: Session,
    socio_id: int,
    activos: Optional[bool] = None,
) -> List[Prestamo]:
    obtener_socio(session, socio_id)
    repo = PrestamoRepository(session)
    return repo.get_by_socio(socio_id, activos=activos)


def listar_prestamos_socio_autorizado(
    session: Session,
    socio_id: int,
    current_user: UsuarioActual,
    activos: Optional[bool] = None,
) -> List[Prestamo]:
    if current_user.rol == Rol.SOCIO and current_user.socio_id != socio_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Un socio solo puede consultar sus propios préstamos",
        )
    return listar_prestamos_socio(session, socio_id, activos=activos)