# 1. Nombre del proyecto
API REST de Gestión de Libros

# 2. Descripción de la API
Esta API permite administrar un catálogo de libros. Está construida utilizando FastAPI y Python, y aplica una arquitectura de software basada en separación por capas (Routers, Services y Schemas). Los datos se almacenan de forma persistente en una base de datos SQLite local.

# 3. Recurso seleccionado
Libros

# 4. Tecnologías utilizadas
- Python 3.10+
- FastAPI
- Pydantic
- Uvicorn (Servidor ASGI)

# 5. Estructura de carpetas
El proyecto respeta la siguiente arquitectura:
- `app/main.py`: Punto de entrada y configuración de FastAPI.
- `app/routers/libro.py`: Definición de los endpoints.
- `app/services/libro_service.py`: Lógica de negocio y persistencia en SQLite.
- `app/schemas/libro.py`: Modelos Pydantic para validación de datos.

# 6. Modelo del recurso
El recurso **Libro** consta de los siguientes campos:
- `id` (int): Identificador único (autogenerado).
- `titulo` (str): Nombre del libro (mínimo 3 caracteres).
- `autor` (str): Nombre del autor.
- `precio` (float): Precio del libro (debe ser mayor a 0).
- `disponible` (bool): Disponibilidad de stock.

# 7 y 8. Endpoints disponibles y Contratos de la API

| Método | Endpoint | Recibe | Devuelve | Éxito | Posibles errores |
|---|---|---|---|---|---|
| GET | `/libros/` | - | Lista de libros | 200 | - |
| GET | `/libros/{id}` | ID | Objeto libro | 200 | 404 |
| POST | `/libros/` | JSON | Objeto creado | 201 | 400, 422 |
| PUT | `/libros/{id}` | ID + JSON | Objeto actualizado | 200 | 400, 404, 422 |
| DELETE | `/libros/{id}` | ID | Objeto eliminado | 200 | 404 |

### Detalle de contratos

**POST /libros/**
- **Propósito:** Registrar un nuevo libro.
- **Datos de entrada:**
  ```json
  {
    "titulo": "Cien años de soledad",
    "autor": "Gabriel García Márquez",
    "precio": 45000,
    "disponible": true
  }