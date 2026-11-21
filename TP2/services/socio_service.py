from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session, select

from models.prestamo import Prestamo
from models.socio import Socio, SocioCreate, SocioUpdate


def crear_socio(session: Session, data: SocioCreate) -> Socio:
    existente = session.exec(select(Socio).where(Socio.email == data.email)).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un socio registrado con el email '{data.email}'",
        )
    socio = Socio.model_validate(data)
    session.add(socio)
    session.commit()
    session.refresh(socio)
    return socio


def listar_socios(session: Session) -> List[Socio]:
    return list(session.exec(select(Socio)).all())


def obtener_socio(session: Session, socio_id: int) -> Socio:
    socio = session.get(Socio, socio_id)
    if not socio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Socio con id {socio_id} no encontrado",
        )
    return socio


def actualizar_socio(session: Session, socio_id: int, data: SocioUpdate) -> Socio:
    socio = obtener_socio(session, socio_id)
    update_data = data.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] != socio.email:
        duplicado = session.exec(
            select(Socio).where(Socio.email == update_data["email"])
        ).first()
        if duplicado:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un socio registrado con el email '{update_data['email']}'",
            )

    for key, value in update_data.items():
        setattr(socio, key, value)

    session.add(socio)
    session.commit()
    session.refresh(socio)
    return socio


def eliminar_socio(session: Session, socio_id: int) -> None:
    socio = obtener_socio(session, socio_id)
    session.delete(socio)
    session.commit()