from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session

from models.autor import Autor, AutorCreate, AutorUpdate
from repositories.autor_repository import AutorRepository


def crear_autor(session: Session, data: AutorCreate) -> Autor:
    repo = AutorRepository(session)
    autor = Autor.model_validate(data)
    return repo.create(autor)


def listar_autores(session: Session) -> List[Autor]:
    repo = AutorRepository(session)
    return repo.get_all()


def obtener_autor(session: Session, autor_id: int) -> Autor:
    repo = AutorRepository(session)
    autor = repo.get_by_id(autor_id)
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor con id {autor_id} no encontrado",
        )
    return autor


def actualizar_autor(session: Session, autor_id: int, data: AutorUpdate) -> Autor:
    repo = AutorRepository(session)
    autor = obtener_autor(session, autor_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(autor, key, value)
    return repo.update(autor)


def eliminar_autor(session: Session, autor_id: int) -> None:
    repo = AutorRepository(session)
    autor = obtener_autor(session, autor_id)
    repo.delete(autor)