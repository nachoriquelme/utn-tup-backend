from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from auth import UsuarioActual, get_current_user, require_bibliotecario
from database import get_session
from models.libro import LibroCreate, LibroReadWithAutores, LibroUpdate
from services import libro_service

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.post("", response_model=LibroReadWithAutores, status_code=status.HTTP_201_CREATED)
def crear_libro(
    data: LibroCreate,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    return libro_service.crear_libro(session, data)


@router.get("", response_model=List[LibroReadWithAutores])
def listar_libros(
    disponibles: Optional[bool] = Query(default=None),
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(get_current_user),
):
    return libro_service.listar_libros(session, disponibles=disponibles)


@router.get("/{libro_id}", response_model=LibroReadWithAutores)
def obtener_libro(
    libro_id: int,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(get_current_user),
):
    return libro_service.obtener_libro(session, libro_id)


@router.put("/{libro_id}", response_model=LibroReadWithAutores)
def actualizar_libro(
    libro_id: int,
    data: LibroUpdate,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    return libro_service.actualizar_libro(session, libro_id, data)


@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(
    libro_id: int,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    libro_service.eliminar_libro(session, libro_id)


@router.post("/{libro_id}/autores/{autor_id}", response_model=LibroReadWithAutores)
def asociar_autor(
    libro_id: int,
    autor_id: int,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    return libro_service.asociar_autor_a_libro(session, libro_id, autor_id)