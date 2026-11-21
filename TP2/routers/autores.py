from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from auth import UsuarioActual, get_current_user, require_bibliotecario
from database import get_session
from models.autor import AutorCreate, AutorRead, AutorUpdate
from services import autor_service

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.post("", response_model=AutorRead, status_code=status.HTTP_201_CREATED)
def crear_autor(
    data: AutorCreate,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    return autor_service.crear_autor(session, data)


@router.get("", response_model=List[AutorRead])
def listar_autores(
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(get_current_user),
):
    return autor_service.listar_autores(session)


@router.get("/{autor_id}", response_model=AutorRead)
def obtener_autor(
    autor_id: int,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(get_current_user),
):
    return autor_service.obtener_autor(session, autor_id)


@router.put("/{autor_id}", response_model=AutorRead)
def actualizar_autor(
    autor_id: int,
    data: AutorUpdate,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    return autor_service.actualizar_autor(session, autor_id, data)


@router.delete("/{autor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_autor(
    autor_id: int,
    session: Session = Depends(get_session),
    _: UsuarioActual = Depends(require_bibliotecario),
):
    autor_service.eliminar_autor(session, autor_id)