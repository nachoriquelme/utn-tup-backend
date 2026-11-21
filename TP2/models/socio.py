from typing import TYPE_CHECKING, List, Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from models.prestamo import Prestamo


class SocioBase(SQLModel):
    nombre: str = Field(min_length=1, max_length=150)
    email: EmailStr = Field(unique=True, index=True)
    activo: bool = Field(default=True)


class Socio(SocioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prestamos: List["Prestamo"] = Relationship(back_populates="socio")


class SocioCreate(SocioBase):
    pass


class SocioUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=150)
    email: Optional[EmailStr] = None
    activo: Optional[bool] = None


class SocioRead(SocioBase):
    id: int