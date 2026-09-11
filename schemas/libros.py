from pydantic import BaseModel, Field
from typing import Optional

# Esquema base con validaciones
class LibroBase(BaseModel):
    # Validación: Mínimo 3 caracteres
    titulo: str = Field(..., min_length=3, description="Título del libro, mínimo 3 caracteres")
    autor: str = Field(..., min_length=2, description="Nombre del autor")
    # Validación: Precio mayor a 0
    precio: float = Field(..., gt=0, description="Precio del libro, debe ser positivo")
    disponible: bool = Field(default=True, description="Indica si el libro está disponible")

# Esquema para crear (hereda de la base sin cambios)
class LibroCreate(LibroBase):
    pass

# Esquema para actualizar (campos opcionales)
class LibroUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=3)
    autor: Optional[str] = Field(None, min_length=2)
    precio: Optional[float] = Field(None, gt=0)
    disponible: Optional[bool] = None

# Esquema de respuesta (incluye el ID asignado)
class LibroResponse(LibroBase):
    id: int
    
    class Config:
        from_attributes = True