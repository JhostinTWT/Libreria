from fastapi import APIRouter, status
from typing import List
from schemas.libros import LibroCreate, LibroResponse, LibroUpdate
from services import libros_services

# Creamos el router con prefijo para mantener limpio main.py
router = APIRouter(prefix="/libros", tags=["Libros"])

# GET /libros/ - Listar todos
@router.get("/", response_model=List[LibroResponse], summary="Listar todos los libros")
def listar_libros():
    return libros_services.obtener_todos()

# GET /libros/{id} - Consultar uno por ID
@router.get("/{id}", response_model=LibroResponse, summary="Consultar un libro por ID")
def obtener_libro(id: int):
    return libros_services.obtener_por_id(id)

# POST /libros/ - Crear (Devuelve 201 Created)
@router.post("/", response_model=LibroResponse, status_code=status.HTTP_201_CREATED, summary="Registrar un nuevo libro")
def crear_libro(libro: LibroCreate):
    return libros_services.crear_libro(libro)

# PUT /libros/{id} - Actualizar
@router.put("/{id}", response_model=LibroResponse, summary="Actualizar un libro existente")
def actualizar_libro(id: int, libro: LibroUpdate):
    return libros_services.actualizar_libro(id, libro)

# DELETE /libros/{id} - Eliminar
@router.delete("/{id}", response_model=LibroResponse, summary="Eliminar un libro")
def eliminar_libro(id: int):
    return libros_services.eliminar_libro(id)