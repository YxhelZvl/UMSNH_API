# src/app/features/ejemplares/infrastructure/repositories/ejemplar_repository_impl.py
from typing import List, Optional
from sqlmodel import select, Session
from src.app.features.ejemplares.domain.repositories.ejemplar_repository import EjemplarRepository
from src.app.features.ejemplares.domain.entities.ejemplar import Ejemplar
from src.app.features.ejemplares.infrastructure.models.ejemplar_model import EjemplarDB
from src.app.features.ejemplares.infrastructure.mappers.ejemplar_mapper import EjemplarMapper
from src.app.features.catalogo.infrastructure.models.catalogo_model import CatalogoDB
from src.app.features.bibliotecas.infrastructure.models.biblioteca_model import BibliotecaDB
from src.app.features.laboratorios.infrastructure.models.laboratorio_model import LaboratorioDB

class EjemplarRepositoryImpl(EjemplarRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Ejemplar]:
        try:
            statement = select(EjemplarDB)
            ejemplares_db = self.session.exec(statement).all()
            return [EjemplarMapper.to_domain(ejemplar_db) for ejemplar_db in ejemplares_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_ejemplar: int) -> Optional[Ejemplar]:
        try:
            ejemplar_db = self.session.get(EjemplarDB, id_ejemplar)
            return EjemplarMapper.to_domain(ejemplar_db) if ejemplar_db else None
        except Exception as e:
            raise e

    def get_by_codigo_inventario(self, codigo_inventario: str) -> Optional[Ejemplar]:
        try:
            statement = select(EjemplarDB).where(EjemplarDB.codigo_inventario == codigo_inventario)
            ejemplar_db = self.session.exec(statement).first()
            return EjemplarMapper.to_domain(ejemplar_db) if ejemplar_db else None
        except Exception as e:
            raise e

    def get_by_catalogo(self, id_catalogo: int) -> List[Ejemplar]:
        try:
            statement = select(EjemplarDB).where(EjemplarDB.id_catalogo == id_catalogo)
            ejemplares_db = self.session.exec(statement).all()
            return [EjemplarMapper.to_domain(ejemplar_db) for ejemplar_db in ejemplares_db]
        except Exception as e:
            raise e

    def get_by_ubicacion(self, ubicacion: str) -> List[Ejemplar]:
        try:
            statement = select(EjemplarDB).where(EjemplarDB.ubicacion == ubicacion)
            ejemplares_db = self.session.exec(statement).all()
            return [EjemplarMapper.to_domain(ejemplar_db) for ejemplar_db in ejemplares_db]
        except Exception as e:
            raise e

    def get_by_estado(self, estado: str) -> List[Ejemplar]:
        try:
            statement = select(EjemplarDB).where(EjemplarDB.estado == estado)
            ejemplares_db = self.session.exec(statement).all()
            return [EjemplarMapper.to_domain(ejemplar_db) for ejemplar_db in ejemplares_db]
        except Exception as e:
            raise e

    def get_by_biblioteca(self, id_biblioteca: int) -> List[Ejemplar]:
        try:
            statement = select(EjemplarDB).where(EjemplarDB.id_biblioteca == id_biblioteca)
            ejemplares_db = self.session.exec(statement).all()
            return [EjemplarMapper.to_domain(ejemplar_db) for ejemplar_db in ejemplares_db]
        except Exception as e:
            raise e

    def get_by_laboratorio(self, id_laboratorio: int) -> List[Ejemplar]:
        try:
            statement = select(EjemplarDB).where(EjemplarDB.id_laboratorio == id_laboratorio)
            ejemplares_db = self.session.exec(statement).all()
            return [EjemplarMapper.to_domain(ejemplar_db) for ejemplar_db in ejemplares_db]
        except Exception as e:
            raise e

    def create(self, ejemplar: Ejemplar) -> Ejemplar:
        try:
            ejemplar_db = EjemplarMapper.to_db(ejemplar)
            self.session.add(ejemplar_db)
            self.session.commit()
            self.session.refresh(ejemplar_db)
            return EjemplarMapper.to_domain(ejemplar_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_ejemplar: int, ejemplar: Ejemplar) -> Optional[Ejemplar]:
        try:
            ejemplar_db = self.session.get(EjemplarDB, id_ejemplar)
            if ejemplar_db:
                ejemplar_db.id_catalogo = ejemplar.id_catalogo
                ejemplar_db.codigo_inventario = ejemplar.codigo_inventario.valor
                ejemplar_db.ubicacion = ejemplar.ubicacion.valor.value
                ejemplar_db.id_laboratorio = ejemplar.id_laboratorio
                ejemplar_db.id_biblioteca = ejemplar.id_biblioteca
                ejemplar_db.estado = ejemplar.estado.valor.value
                self.session.add(ejemplar_db)
                self.session.commit()
                self.session.refresh(ejemplar_db)
                return EjemplarMapper.to_domain(ejemplar_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_ejemplar: int) -> bool:
        try:
            ejemplar_db = self.session.get(EjemplarDB, id_ejemplar)
            if ejemplar_db:
                self.session.delete(ejemplar_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def exists_by_codigo_inventario(self, codigo_inventario: str) -> bool:
        try:
            statement = select(EjemplarDB).where(EjemplarDB.codigo_inventario == codigo_inventario)
            ejemplar_db = self.session.exec(statement).first()
            return ejemplar_db is not None
        except Exception as e:
            raise e

    # Implementación de métodos con JOINs para datos detallados
    def get_all_with_details(self) -> List[dict]:
        try:
            statement = select(
                EjemplarDB, 
                CatalogoDB, 
                BibliotecaDB, 
                LaboratorioDB
            ).join(
                CatalogoDB, EjemplarDB.id_catalogo == CatalogoDB.id_catalogo
            ).join(
                BibliotecaDB, EjemplarDB.id_biblioteca == BibliotecaDB.id_biblioteca, isouter=True
            ).join(
                LaboratorioDB, EjemplarDB.id_laboratorio == LaboratorioDB.id_laboratorio, isouter=True
            )
            results = self.session.exec(statement).all()
            
            ejemplares_detallados = []
            for ejemplar_db, catalogo_db, biblioteca_db, laboratorio_db in results:
                ejemplares_detallados.append({
                    'ejemplar': ejemplar_db,
                    'catalogo': catalogo_db,
                    'biblioteca': biblioteca_db,
                    'laboratorio': laboratorio_db
                })
            
            return ejemplares_detallados
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id_with_details(self, id_ejemplar: int) -> Optional[dict]:
        try:
            statement = select(
                EjemplarDB, 
                CatalogoDB, 
                BibliotecaDB, 
                LaboratorioDB
            ).join(
                CatalogoDB, EjemplarDB.id_catalogo == CatalogoDB.id_catalogo
            ).join(
                BibliotecaDB, EjemplarDB.id_biblioteca == BibliotecaDB.id_biblioteca, isouter=True
            ).join(
                LaboratorioDB, EjemplarDB.id_laboratorio == LaboratorioDB.id_laboratorio, isouter=True
            ).where(EjemplarDB.id_ejemplar == id_ejemplar)
            result = self.session.exec(statement).first()
            
            if result:
                ejemplar_db, catalogo_db, biblioteca_db, laboratorio_db = result
                return {
                    'ejemplar': ejemplar_db,
                    'catalogo': catalogo_db,
                    'biblioteca': biblioteca_db,
                    'laboratorio': laboratorio_db
                }
            return None
        except Exception as e:
            raise e

    def get_disponibles_for_prestamo(self) -> List[dict]:
        try:
            statement = select(
                EjemplarDB, 
                CatalogoDB
            ).join(
                CatalogoDB, EjemplarDB.id_catalogo == CatalogoDB.id_catalogo
            ).where(
                EjemplarDB.estado == "disponible"
            )
            results = self.session.exec(statement).all()
            
            ejemplares_disponibles = []
            for ejemplar_db, catalogo_db in results:
                ejemplares_disponibles.append({
                    'ejemplar': ejemplar_db,
                    'catalogo': catalogo_db
                })
            
            return ejemplares_disponibles
        except Exception as e:
            raise e