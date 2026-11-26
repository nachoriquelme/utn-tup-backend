from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session

from models.socio import Socio, SocioCreate, SocioUpdate
from repositories.socio_repository import SocioRepository


def crear_socio(session: Session, data: SocioCreate) -> Socio:
    repo = SocioRepository(session)
    existente = repo.get_by_email(data.email)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un socio registrado con el email '{data.email}'",
        )
    socio = Socio.model_validate(data)
    return repo.create(socio)


def listar_socios(session: Session) -> List[Socio]:
    repo = SocioRepository(session)
    return repo.get_all()


def obtener_socio(session: Session, socio_id: int) -> Socio:
    repo = SocioRepository(session)
    socio = repo.get_by_id(socio_id)
    if not socio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Socio con id {socio_id} no encontrado",
        )
    return socio


def actualizar_socio(session: Session, socio_id: int, data: SocioUpdate) -> Socio:
    repo = SocioRepository(session)
    socio = obtener_socio(session, socio_id)
    update_data = data.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] != socio.email:
        duplicado = repo.get_by_email(update_data["email"])
        if duplicado:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un socio registrado con el email '{update_data['email']}'",
            )

    for key, value in update_data.items():
        setattr(socio, key, value)

    return repo.update(socio)


def eliminar_socio(session: Session, socio_id: int) -> None:
    repo = SocioRepository(session)
    socio = obtener_socio(session, socio_id)
    repo.delete(socio)