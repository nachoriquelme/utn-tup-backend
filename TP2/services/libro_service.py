from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session

from models.libro import Libro, LibroCreate, LibroUpdate
from repositories.libro_repository import LibroRepository
from services.autor_service import obtener_autor


def crear_libro(session: Session, data: LibroCreate) -> Libro:
    repo = LibroRepository(session)
    existente = repo.get_by_isbn(data.isbn)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un libro registrado con el ISBN '{data.isbn}'",
        )
    libro = Libro.model_validate(data)
    return repo.create(libro)


def listar_libros(session: Session, disponibles: Optional[bool] = None) -> List[Libro]:
    repo = LibroRepository(session)
    return repo.get_all(disponibles=disponibles)


def obtener_libro(session: Session, libro_id: int) -> Libro:
    repo = LibroRepository(session)
    libro = repo.get_by_id(libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con id {libro_id} no encontrado",
        )
    return libro


def actualizar_libro(session: Session, libro_id: int, data: LibroUpdate) -> Libro:
    repo = LibroRepository(session)
    libro = obtener_libro(session, libro_id)
    update_data = data.model_dump(exclude_unset=True)

    if "isbn" in update_data and update_data["isbn"] != libro.isbn:
        duplicado = repo.get_by_isbn(update_data["isbn"])
        if duplicado:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un libro registrado con el ISBN '{update_data['isbn']}'",
            )

    for key, value in update_data.items():
        setattr(libro, key, value)

    return repo.update(libro)


def eliminar_libro(session: Session, libro_id: int) -> None:
    repo = LibroRepository(session)
    libro = obtener_libro(session, libro_id)
    if repo.has_prestamos(libro_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar un libro que tiene préstamos asociados",
        )
    repo.delete(libro)


def asociar_autor_a_libro(session: Session, libro_id: int, autor_id: int) -> Libro:
    repo = LibroRepository(session)
    libro = obtener_libro(session, libro_id)
    autor = obtener_autor(session, autor_id)
    return repo.add_autor(libro, autor)