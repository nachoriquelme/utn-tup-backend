from typing import List, Optional
from sqlmodel import Session, select

from models.autor import Autor
from models.libro import Libro
from models.prestamo import Prestamo


class LibroRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, libro: Libro) -> Libro:
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro

    def get_all(self, disponibles: Optional[bool] = None) -> List[Libro]:
        query = select(Libro)
        if disponibles is True:
            query = query.where(Libro.stock > 0)
        return list(self.session.exec(query).all())

    def get_by_id(self, libro_id: int) -> Optional[Libro]:
        return self.session.get(Libro, libro_id)

    def get_by_isbn(self, isbn: str) -> Optional[Libro]:
        return self.session.exec(select(Libro).where(Libro.isbn == isbn)).first()

    def has_prestamos(self, libro_id: int) -> bool:
        prestamo = self.session.exec(
            select(Prestamo).where(Prestamo.libro_id == libro_id)
        ).first()
        return prestamo is not None

    def add_autor(self, libro: Libro, autor: Autor) -> Libro:
        if autor not in libro.autores:
            libro.autores.append(autor)
            self.session.add(libro)
            self.session.commit()
            self.session.refresh(libro)
        return libro

    def update(self, libro: Libro) -> Libro:
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro

    def delete(self, libro: Libro) -> None:
        self.session.delete(libro)
        self.session.commit()