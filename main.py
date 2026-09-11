from fastapi import FastAPI
from routers import libro

# Instanciamos la aplicación con metadatos para la documentación de Swagger
app = FastAPI(
    title="API de Libros",
    description="API REST para la gestión de un catálogo de libros implementando CRUD completo y arquitectura por capas.",
    version="1.0.0"
)

# Incluimos el router de libros
app.include_router(libro.router)

# Ruta base de bienvenida
@app.get("/", tags=["Inicio"])
def home():
    return {"mensaje": "Bienvenido a la API de Libros. Visita /docs para ver la documentación."}