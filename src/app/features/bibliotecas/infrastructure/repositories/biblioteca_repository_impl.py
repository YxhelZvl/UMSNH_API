# src/app/features/bibliotecas/infrastructure/repositories/biblioteca_repository_impl.py
from typing import List, Optional
from sqlmodel import select, Session
from src.app.features.bibliotecas.domain.repositories.biblioteca_repository import BibliotecaRepository
from src.app.features.bibliotecas.domain.entities.biblioteca import Biblioteca
from src.app.features.bibliotecas.infrastructure.models.biblioteca_model import BibliotecaDB
from src.app.features.bibliotecas.infrastructure.mappers.biblioteca_mapper import BibliotecaMapper

class BibliotecaRepositoryImpl(BibliotecaRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Biblioteca]:
        try:
            statement = select(BibliotecaDB)
            bibliotecas_db = self.session.exec(statement).all()
            return [BibliotecaMapper.to_domain(bib_db) for bib_db in bibliotecas_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_biblioteca: int) -> Optional[Biblioteca]:
        try:
            biblioteca_db = self.session.get(BibliotecaDB, id_biblioteca)
            return BibliotecaMapper.to_domain(biblioteca_db) if biblioteca_db else None
        except Exception as e:
            raise e

    def get_by_nombre(self, nombre: str) -> Optional[Biblioteca]:
        try:
            statement = select(BibliotecaDB).where(BibliotecaDB.nombre == nombre)
            biblioteca_db = self.session.exec(statement).first()
            return BibliotecaMapper.to_domain(biblioteca_db) if biblioteca_db else None
        except Exception as e:
            raise e

    def create(self, biblioteca: Biblioteca) -> Biblioteca:
        try:
            biblioteca_db = BibliotecaMapper.to_db(biblioteca)
            self.session.add(biblioteca_db)
            self.session.commit()
            self.session.refresh(biblioteca_db)
            return BibliotecaMapper.to_domain(biblioteca_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_biblioteca: int, biblioteca: Biblioteca) -> Optional[Biblioteca]:
        try:
            biblioteca_db = self.session.get(BibliotecaDB, id_biblioteca)
            if biblioteca_db:
                biblioteca_db.nombre = biblioteca.nombre
                biblioteca_db.ubicacion = biblioteca.ubicacion
                self.session.add(biblioteca_db)
                self.session.commit()
                self.session.refresh(biblioteca_db)
                return BibliotecaMapper.to_domain(biblioteca_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_biblioteca: int) -> bool:
        try:
            biblioteca_db = self.session.get(BibliotecaDB, id_biblioteca)
            if biblioteca_db:
                self.session.delete(biblioteca_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def exists_by_nombre(self, nombre: str) -> bool:
        try:
            statement = select(BibliotecaDB).where(BibliotecaDB.nombre == nombre)
            biblioteca_db = self.session.exec(statement).first()
            return biblioteca_db is not None
        except Exception as e:
            raise e