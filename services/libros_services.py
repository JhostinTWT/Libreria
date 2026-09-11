import sqlite3
from contextlib import contextmanager
from pathlib import Path

from fastapi import HTTPException
from schemas.libros import LibroCreate, LibroUpdate

DATABASE_PATH = Path(__file__).resolve().parent.parent / "libros.db"


@contextmanager
def _get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _initialize_database():
    with _get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL COLLATE NOCASE UNIQUE,
                autor TEXT NOT NULL,
                precio REAL NOT NULL CHECK (precio > 0),
                disponible INTEGER NOT NULL DEFAULT 1
            )
            """
        )


def _to_dict(row):
    libro = dict(row)
    libro["disponible"] = bool(libro["disponible"])
    return libro


_initialize_database()


def obtener_todos():
    with _get_connection() as connection:
        rows = connection.execute("SELECT * FROM libros ORDER BY id").fetchall()
    return [_to_dict(row) for row in rows]


def obtener_por_id(libro_id: int):
    with _get_connection() as connection:
        row = connection.execute("SELECT * FROM libros WHERE id = ?", (libro_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return _to_dict(row)


def crear_libro(libro: LibroCreate):
    try:
        with _get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO libros (titulo, autor, precio, disponible)
                VALUES (?, ?, ?, ?)
                """,
                (libro.titulo, libro.autor, libro.precio, int(libro.disponible)),
            )
            row = connection.execute(
                "SELECT * FROM libros WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Ya existe un libro con este título")
    return _to_dict(row)


def actualizar_libro(libro_id: int, libro_update: LibroUpdate):
    obtener_por_id(libro_id)
    update_data = libro_update.model_dump(exclude_unset=True)

    if not update_data:
        return obtener_por_id(libro_id)

    fields = []
    values = []
    for field, value in update_data.items():
        fields.append(f"{field} = ?")
        values.append(int(value) if field == "disponible" else value)
    values.append(libro_id)

    try:
        with _get_connection() as connection:
            connection.execute(
                f"UPDATE libros SET {', '.join(fields)} WHERE id = ?", values
            )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="El título ya está en uso por otro libro")

    return obtener_por_id(libro_id)


def eliminar_libro(libro_id: int):
    libro_existente = obtener_por_id(libro_id)
    with _get_connection() as connection:
        connection.execute("DELETE FROM libros WHERE id = ?", (libro_id,))
    return libro_existente