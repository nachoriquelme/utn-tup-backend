from dataclasses import dataclass
from enum import Enum
from typing import Optional
from fastapi import Depends, Header, HTTPException, status


class Rol(str, Enum):
    BIBLIOTECARIO = "bibliotecario"
    SOCIO = "socio"


@dataclass
class UsuarioActual:
    rol: Rol
    socio_id: Optional[int] = None


def get_current_user(
    x_role: Optional[str] = Header(default=None, alias="X-Role"),
    x_socio_id: Optional[int] = Header(default=None, alias="X-Socio-Id"),
) -> UsuarioActual:
    if not x_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta el header X-Role ('bibliotecario' o 'socio')",
        )

    try:
        rol = Rol(x_role.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Rol '{x_role}' no válido. Use 'bibliotecario' o 'socio'",
        )

    if rol == Rol.SOCIO and x_socio_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El header X-Socio-Id es obligatorio para el rol 'socio'",
        )

    return UsuarioActual(rol=rol, socio_id=x_socio_id)


def require_bibliotecario(
    current_user: UsuarioActual = Depends(get_current_user),
) -> UsuarioActual:
    if current_user.rol != Rol.BIBLIOTECARIO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un bibliotecario puede administrar el catálogo o gestionar este recurso",
        )
    return current_user