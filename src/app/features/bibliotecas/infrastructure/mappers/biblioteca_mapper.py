# src/app/features/bibliotecas/infrastructure/mappers/biblioteca_mapper.py
from src.app.features.bibliotecas.domain.entities.biblioteca import Biblioteca
from src.app.features.bibliotecas.infrastructure.models.biblioteca_model import BibliotecaDB

class BibliotecaMapper:
    @staticmethod
    def to_domain(biblioteca_db: BibliotecaDB) -> Biblioteca:
        if not biblioteca_db:
            return None
            
        return Biblioteca(
            id_biblioteca=biblioteca_db.id_biblioteca,
            nombre=biblioteca_db.nombre,
            ubicacion=biblioteca_db.ubicacion
        )

    @staticmethod
    def to_db(biblioteca: Biblioteca) -> BibliotecaDB:
        if not biblioteca:
            return None
            
        return BibliotecaDB(
            id_biblioteca=biblioteca.id_biblioteca,
            nombre=biblioteca.nombre,
            ubicacion=biblioteca.ubicacion
        )