from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel
from models.libro_autor import LibroAutor

if TYPE_CHECKING:
    from models.libro import Libro


class AutorBase(SQLModel):
    nombre: str = Field(min_length=1, max_length=150)
    nacionalidad: str = Field(min_length=1, max_length=100)


class Autor(AutorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    libros: List["Libro"] = Relationship(
        back_populates="autores", link_model=LibroAutor
    )


class AutorCreate(AutorBase):
    pass


class AutorUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=150)
    nacionalidad: Optional[str] = Field(default=None, min_length=1, max_length=100)


class AutorRead(AutorBase):
    id: int