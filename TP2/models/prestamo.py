from datetime import date, timedelta
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.libro import Libro
    from models.socio import Socio


class PrestamoBase(SQLModel):
    socio_id: int = Field(foreign_key="socio.id")
    libro_id: int = Field(foreign_key="libro.id")


class Prestamo(PrestamoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_prestamo: date = Field(default_factory=date.today)
    fecha_vencimiento: date = Field(
        default_factory=lambda: date.today() + timedelta(days=14)
    )
    fecha_devolucion: Optional[date] = Field(default=None)
    multa: float = Field(default=0.0, ge=0)

    socio: Optional["Socio"] = Relationship(back_populates="prestamos")
    libro: Optional["Libro"] = Relationship(back_populates="prestamos")


class PrestamoCreate(PrestamoBase):
    fecha_prestamo: Optional[date] = None


class PrestamoDevolucionRequest(SQLModel):
    fecha_devolucion: Optional[date] = None


class PrestamoRead(PrestamoBase):
    id: int
    fecha_prestamo: date
    fecha_vencimiento: date
    fecha_devolucion: Optional[date]
    multa: float