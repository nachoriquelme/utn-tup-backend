from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from models.users import (
    User,
    GetUsersResponse,
    CreateUserResponse,
    DeleteUserResponse,
    UpdateUserResponse,
)

router = APIRouter()

usuarios: list[User] = [
    User(id=1, name="juan perez", is_active = True),
    User(id=2, name="pepe sanchez", is_active = False),
]


@router.get("/user")
def get_users(is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo")) -> GetUsersResponse:
    if is_active is not None:
        usuarioFiltrados = [u for u in usuarios if u.is_active == is_active]
        return GetUsersResponse(users=usuarioFiltrados)

    return GetUsersResponse(users=usuarios)
    


@router.delete("/user/{id}")
def delete_user(id: int) -> DeleteUserResponse:
    for user in usuarios:
        if user.id == id:
            usuarios.remove(user)
            return DeleteUserResponse(message="usuario borrado")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


@router.put("/user/{id}")
def update_user(id: int, user_modificado: User) -> UpdateUserResponse:
    for user in usuarios:
        if user.id == id:
            if user_modificado.name is not None:
                user.name = user_modificado.name
            if user_modificado.is_active is not None:
                user.is_active = user_modificado.is_active
            return UpdateUserResponse(message="usuario actualizado", user = user_modificado)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


@router.post("/user")
def create_user(user: User) -> CreateUserResponse:
    usuarios.append(user)
    return CreateUserResponse(message="usuario creado")
