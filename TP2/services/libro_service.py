from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session, select

from models.libro import Libro, LibroCreate, LibroUpdate
from models.prestamo import Prestamo
from services.autor_service import obtener_autor

def crear_libro(session: Session, data: LibroCreate) -> Libro:
    existente = session.exec(select(Libro).where(Libro.isbn == data.isbn)).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un libro registrado con el ISBN '{data.isbn}'",
        )
    libro = Libro.model_validate(data)
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro


def listar_libros(session: Session, disponibles: Optional[bool] = None) -> List[Libro]:
    query = select(Libro)
    if disponibles is True:
        query = query.where(Libro.stock > 0)
    return list(session.exec(query).all())


def obtener_libro(session: Session, libro_id: int) -> Libro:
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con id {libro_id} no encontrado",
        )
    return libro


def actualizar_libro(session: Session, libro_id: int, data: LibroUpdate) -> Libro:
    libro = obtener_libro(session, libro_id)
    update_data = data.model_dump(exclude_unset=True)

    if "isbn" in update_data and update_data["isbn"] != libro.isbn:
        duplicado = session.exec(
            select(Libro).where(Libro.isbn == update_data["isbn"])
        ).first()
        if duplicado:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un libro registrado con el ISBN '{update_data['isbn']}'",
            )

    for key, value in update_data.items():
        setattr(libro, key, value)

    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro


def eliminar_libro(session: Session, libro_id: int) -> None:
    libro = obtener_libro(session, libro_id)
    prestamo_asociado = session.exec(
        select(Prestamo).where(Prestamo.libro_id == libro_id)
    ).first()
    if prestamo_asociado:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar un libro que tiene préstamos asociados",
        )
    session.delete(libro)
    session.commit()


def asociar_autor_a_libro(session: Session, libro_id: int, autor_id: int) -> Libro:
    libro = obtener_libro(session, libro_id)
    autor = obtener_autor(session, autor_id)

    if autor not in libro.autores:
        libro.autores.append(autor)
        session.add(libro)
        session.commit()
        session.refresh(libro)

    return libro