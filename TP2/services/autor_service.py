from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session, select

from models.autor import Autor, AutorCreate, AutorUpdate

def crear_autor(session: Session, data: AutorCreate) -> Autor:
    autor = Autor.model_validate(data)
    session.add(autor)
    session.commit()
    session.refresh(autor)
    return autor


def listar_autores(session: Session) -> List[Autor]:
    return list(session.exec(select(Autor)).all())


def obtener_autor(session: Session, autor_id: int) -> Autor:
    autor = session.get(Autor, autor_id)
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor con id {autor_id} no encontrado",
        )
    return autor


def actualizar_autor(session: Session, autor_id: int, data: AutorUpdate) -> Autor:
    autor = obtener_autor(session, autor_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(autor, key, value)
    session.add(autor)
    session.commit()
    session.refresh(autor)
    return autor


def eliminar_autor(session: Session, autor_id: int) -> None:
    autor = obtener_autor(session, autor_id)
    session.delete(autor)
    session.commit()