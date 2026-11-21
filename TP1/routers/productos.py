from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from models.productos import (
    Producto,
    GetProductosResponse,
    CreateProductoResponse,
    UpdateProductoResponse,
    DeleteProductoResponse
)

router = APIRouter()

productosLista: list[Producto] = [
    Producto(id=1, nombre="Monitor", precio=500000, stock=10, categoria="Tecnologia"),
    Producto(id=2, nombre="Mouse", precio=15000, stock=50, categoria="Accesorios"),
]


@router.get("/producto")
def get_productos(categoria: Optional[str] = Query(None, description="Filtrar por categoría")) -> GetProductosResponse:
    if categoria is not None:
        productosFiltrados = [p for p in productosLista if p.categoria.lower() == categoria.lower()]
        return GetProductosResponse(productos=productosFiltrados)
    return GetProductosResponse(productos=productosLista)

@router.get("/producto/{id}")
def get_producto_by_id(id: int) -> Producto:
    for p in productosLista:
        if p.id == id:
            return p
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Producto no encontrado"
    )

@router.post("/producto")
def create_producto(producto: Producto) -> CreateProductoResponse:
    productosLista.append(producto)
    return CreateProductoResponse(message="Producto creado")

@router.put("/producto/{id}")
def update_producto(id: int, producto_data: Producto) -> UpdateProductoResponse:
    for index, p in enumerate(productosLista):
        if p.id == id:
            producto_data.id = id
            productosLista[index] = producto_data
            return UpdateProductoResponse(message="producto actualizado", producto=producto_data)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Producto no encontrado"
    )

@router.delete("/producto/{id}")
def delete_producto(id: int) -> DeleteProductoResponse:
    for p in productosLista:
        if p.id == id:
            productosLista.remove(p)
            return DeleteProductoResponse(message="producto borrado")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Producto no encontrado"
    )