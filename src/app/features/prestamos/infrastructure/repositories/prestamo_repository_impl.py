# src/app/features/prestamos/infrastructure/repositories/prestamo_repository_impl.py
from typing import List, Optional
from datetime import datetime, date, timedelta
from sqlmodel import select, Session
from src.app.features.prestamos.domain.repositories.prestamo_repository import PrestamoRepository
from src.app.features.prestamos.domain.entities.prestamo import Prestamo
from src.app.features.prestamos.infrastructure.models.prestamo_model import PrestamoDB
from src.app.features.prestamos.infrastructure.mappers.prestamo_mapper import PrestamoMapper
from src.app.features.user.infrastructure.models.user_model import UserDB
from src.app.features.ejemplares.infrastructure.models.ejemplar_model import EjemplarDB
from src.app.features.catalogo.infrastructure.models.catalogo_model import CatalogoDB

class PrestamoRepositoryImpl(PrestamoRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Prestamo]:
        try:
            statement = select(PrestamoDB)
            prestamos_db = self.session.exec(statement).all()
            return [PrestamoMapper.to_domain(prestamo_db) for prestamo_db in prestamos_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_prestamo: int) -> Optional[Prestamo]:
        try:
            prestamo_db = self.session.get(PrestamoDB, id_prestamo)
            return PrestamoMapper.to_domain(prestamo_db) if prestamo_db else None
        except Exception as e:
            raise e

    def get_by_usuario(self, id_usuario: int) -> List[Prestamo]:
        try:
            statement = select(PrestamoDB).where(PrestamoDB.id_usuario == id_usuario)
            prestamos_db = self.session.exec(statement).all()
            return [PrestamoMapper.to_domain(prestamo_db) for prestamo_db in prestamos_db]
        except Exception as e:
            raise e

    def get_by_ejemplar(self, id_ejemplar: int) -> List[Prestamo]:
        try:
            statement = select(PrestamoDB).where(PrestamoDB.id_ejemplar == id_ejemplar)
            prestamos_db = self.session.exec(statement).all()
            return [PrestamoMapper.to_domain(prestamo_db) for prestamo_db in prestamos_db]
        except Exception as e:
            raise e

    def get_by_estado(self, estado: str) -> List[Prestamo]:
        try:
            statement = select(PrestamoDB).where(PrestamoDB.estado == estado)
            prestamos_db = self.session.exec(statement).all()
            return [PrestamoMapper.to_domain(prestamo_db) for prestamo_db in prestamos_db]
        except Exception as e:
            raise e

    def get_prestamos_activos(self) -> List[Prestamo]:
        try:
            statement = select(PrestamoDB).where(PrestamoDB.estado == "activo")
            prestamos_db = self.session.exec(statement).all()
            return [PrestamoMapper.to_domain(prestamo_db) for prestamo_db in prestamos_db]
        except Exception as e:
            raise e

    def get_prestamos_retrasados(self) -> List[Prestamo]:
        try:
            statement = select(PrestamoDB).where(PrestamoDB.estado == "retrasado")
            prestamos_db = self.session.exec(statement).all()
            return [PrestamoMapper.to_domain(prestamo_db) for prestamo_db in prestamos_db]
        except Exception as e:
            raise e

    def get_prestamos_por_vencer(self, dias: int = 3) -> List[Prestamo]:
        try:
            fecha_limite = date.today() + timedelta(days=dias)
            statement = select(PrestamoDB).where(
                PrestamoDB.estado == "activo",
                PrestamoDB.fecha_devolucion_esperada <= fecha_limite
            )
            prestamos_db = self.session.exec(statement).all()
            return [PrestamoMapper.to_domain(prestamo_db) for prestamo_db in prestamos_db]
        except Exception as e:
            raise e

    def create(self, prestamo: Prestamo) -> Prestamo:
        try:
            prestamo_db = PrestamoMapper.to_db(prestamo)
            self.session.add(prestamo_db)
            self.session.commit()
            self.session.refresh(prestamo_db)
            return PrestamoMapper.to_domain(prestamo_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_prestamo: int, prestamo: Prestamo) -> Optional[Prestamo]:
        try:
            prestamo_db = self.session.get(PrestamoDB, id_prestamo)
            if prestamo_db:
                prestamo_db.id_usuario = prestamo.id_usuario
                prestamo_db.id_ejemplar = prestamo.id_ejemplar
                prestamo_db.fecha_prestamo = prestamo.fechas.fecha_prestamo
                prestamo_db.fecha_devolucion_esperada = prestamo.fechas.fecha_devolucion_esperada
                prestamo_db.fecha_devolucion_real = prestamo.fechas.fecha_devolucion_real
                prestamo_db.estado = prestamo.estado.valor.value
                self.session.add(prestamo_db)
                self.session.commit()
                self.session.refresh(prestamo_db)
                return PrestamoMapper.to_domain(prestamo_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_prestamo: int) -> bool:
        try:
            prestamo_db = self.session.get(PrestamoDB, id_prestamo)
            if prestamo_db:
                self.session.delete(prestamo_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    # Implementación de métodos con JOINs para datos detallados
    def get_all_with_details(self) -> List[dict]:
        try:
            statement = select(
                PrestamoDB, 
                UserDB, 
                EjemplarDB, 
                CatalogoDB
            ).join(
                UserDB, PrestamoDB.id_usuario == UserDB.id_usuario
            ).join(
                EjemplarDB, PrestamoDB.id_ejemplar == EjemplarDB.id_ejemplar
            ).join(
                CatalogoDB, EjemplarDB.id_catalogo == CatalogoDB.id_catalogo
            )
            results = self.session.exec(statement).all()
            
            prestamos_detallados = []
            for prestamo_db, user_db, ejemplar_db, catalogo_db in results:
                prestamos_detallados.append({
                    'prestamo': prestamo_db,
                    'usuario': user_db,
                    'ejemplar': ejemplar_db,
                    'catalogo': catalogo_db
                })
            
            return prestamos_detallados
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id_with_details(self, id_prestamo: int) -> Optional[dict]:
        try:
            statement = select(
                PrestamoDB, 
                UserDB, 
                EjemplarDB, 
                CatalogoDB
            ).join(
                UserDB, PrestamoDB.id_usuario == UserDB.id_usuario
            ).join(
                EjemplarDB, PrestamoDB.id_ejemplar == EjemplarDB.id_ejemplar
            ).join(
                CatalogoDB, EjemplarDB.id_catalogo == CatalogoDB.id_catalogo
            ).where(PrestamoDB.id_prestamo == id_prestamo)
            result = self.session.exec(statement).first()
            
            if result:
                prestamo_db, user_db, ejemplar_db, catalogo_db = result
                return {
                    'prestamo': prestamo_db,
                    'usuario': user_db,
                    'ejemplar': ejemplar_db,
                    'catalogo': catalogo_db
                }
            return None
        except Exception as e:
            raise e

    def get_by_usuario_with_details(self, id_usuario: int) -> List[dict]:
        try:
            statement = select(
                PrestamoDB, 
                UserDB, 
                EjemplarDB, 
                CatalogoDB
            ).join(
                UserDB, PrestamoDB.id_usuario == UserDB.id_usuario
            ).join(
                EjemplarDB, PrestamoDB.id_ejemplar == EjemplarDB.id_ejemplar
            ).join(
                CatalogoDB, EjemplarDB.id_catalogo == CatalogoDB.id_catalogo
            ).where(PrestamoDB.id_usuario == id_usuario)
            results = self.session.exec(statement).all()
            
            prestamos_detallados = []
            for prestamo_db, user_db, ejemplar_db, catalogo_db in results:
                prestamos_detallados.append({
                    'prestamo': prestamo_db,
                    'usuario': user_db,
                    'ejemplar': ejemplar_db,
                    'catalogo': catalogo_db
                })
            
            return prestamos_detallados
        except Exception as e:
            raise e

    def get_prestamos_activos_with_details(self) -> List[dict]:
        try:
            statement = select(
                PrestamoDB, 
                UserDB, 
                EjemplarDB, 
                CatalogoDB
            ).join(
                UserDB, PrestamoDB.id_usuario == UserDB.id_usuario
            ).join(
                EjemplarDB, PrestamoDB.id_ejemplar == EjemplarDB.id_ejemplar
            ).join(
                CatalogoDB, EjemplarDB.id_catalogo == CatalogoDB.id_catalogo
            ).where(PrestamoDB.estado == "activo")
            results = self.session.exec(statement).all()
            
            prestamos_detallados = []
            for prestamo_db, user_db, ejemplar_db, catalogo_db in results:
                prestamos_detallados.append({
                    'prestamo': prestamo_db,
                    'usuario': user_db,
                    'ejemplar': ejemplar_db,
                    'catalogo': catalogo_db
                })
            
            return prestamos_detallados
        except Exception as e:
            raise e