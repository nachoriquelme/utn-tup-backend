from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel
from models.autor import AutorRead
from models.libro_autor import LibroAutor

if TYPE_CHECKING:
    from models.autor import Autor
    from models.prestamo import Prestamo


class LibroBase(SQLModel):
    titulo: str = Field(min_length=1, max_length=200)
    isbn: str = Field(unique=True, index=True, min_length=1, max_length=30)
    stock: int = Field(default=0, ge=0)
    anio: int = Field(ge=0)


class Libro(LibroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    autores: List["Autor"] = Relationship(
        back_populates="libros", link_model=LibroAutor
    )
    prestamos: List["Prestamo"] = Relationship(back_populates="libro")


class LibroCreate(LibroBase):
    pass


class LibroUpdate(SQLModel):
    titulo: Optional[str] = Field(default=None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(default=None, min_length=1, max_length=30)
    stock: Optional[int] = Field(default=None, ge=0)
    anio: Optional[int] = Field(default=None, ge=0)


class LibroRead(LibroBase):
    id: int


class LibroReadWithAutores(LibroBase):
    id: int
    autores: List[AutorRead] = []