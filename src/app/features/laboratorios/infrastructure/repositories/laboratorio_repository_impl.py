# src/app/features/laboratorios/infrastructure/repositories/laboratorio_repository_impl.py
from typing import List, Optional
from sqlmodel import select, Session
from src.app.features.laboratorios.domain.repositories.laboratorio_repository import LaboratorioRepository
from src.app.features.laboratorios.domain.entities.laboratorio import Laboratorio
from src.app.features.laboratorios.infrastructure.models.laboratorio_model import LaboratorioDB
from src.app.features.laboratorios.infrastructure.mappers.laboratorio_mapper import LaboratorioMapper
from src.app.features.user.infrastructure.models.user_model import UserDB

class LaboratorioRepositoryImpl(LaboratorioRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Laboratorio]:
        try:
            statement = select(LaboratorioDB)
            laboratorios_db = self.session.exec(statement).all()
            return [LaboratorioMapper.to_domain(lab_db) for lab_db in laboratorios_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_laboratorio: int) -> Optional[Laboratorio]:
        try:
            laboratorio_db = self.session.get(LaboratorioDB, id_laboratorio)
            return LaboratorioMapper.to_domain(laboratorio_db) if laboratorio_db else None
        except Exception as e:
            raise e

    def get_by_nombre(self, nombre: str) -> Optional[Laboratorio]:
        try:
            statement = select(LaboratorioDB).where(LaboratorioDB.nombre == nombre)
            laboratorio_db = self.session.exec(statement).first()
            return LaboratorioMapper.to_domain(laboratorio_db) if laboratorio_db else None
        except Exception as e:
            raise e

    def get_by_responsable(self, responsable_id: int) -> List[Laboratorio]:
        try:
            statement = select(LaboratorioDB).where(LaboratorioDB.responsable_id == responsable_id)
            laboratorios_db = self.session.exec(statement).all()
            return [LaboratorioMapper.to_domain(lab_db) for lab_db in laboratorios_db]
        except Exception as e:
            raise e

    def create(self, laboratorio: Laboratorio) -> Laboratorio:
        try:
            laboratorio_db = LaboratorioMapper.to_db(laboratorio)
            self.session.add(laboratorio_db)
            self.session.commit()
            self.session.refresh(laboratorio_db)
            return LaboratorioMapper.to_domain(laboratorio_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_laboratorio: int, laboratorio: Laboratorio) -> Optional[Laboratorio]:
        try:
            laboratorio_db = self.session.get(LaboratorioDB, id_laboratorio)
            if laboratorio_db:
                laboratorio_db.nombre = laboratorio.nombre.valor
                laboratorio_db.ubicacion = laboratorio.ubicacion.valor
                laboratorio_db.responsable_id = laboratorio.responsable_id
                self.session.add(laboratorio_db)
                self.session.commit()
                self.session.refresh(laboratorio_db)
                return LaboratorioMapper.to_domain(laboratorio_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_laboratorio: int) -> bool:
        try:
            laboratorio_db = self.session.get(LaboratorioDB, id_laboratorio)
            if laboratorio_db:
                self.session.delete(laboratorio_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def exists_by_nombre(self, nombre: str) -> bool:
        try:
            statement = select(LaboratorioDB).where(LaboratorioDB.nombre == nombre)
            laboratorio_db = self.session.exec(statement).first()
            return laboratorio_db is not None
        except Exception as e:
            raise e

    # Implementación de métodos con JOINs para datos detallados
    def get_all_with_details(self) -> List[dict]:
        try:
            statement = select(LaboratorioDB, UserDB).join(
                UserDB, LaboratorioDB.responsable_id == UserDB.id_usuario, isouter=True
            )
            results = self.session.exec(statement).all()
            
            laboratorios_detallados = []
            for laboratorio_db, user_db in results:
                laboratorios_detallados.append({
                    'laboratorio': laboratorio_db,
                    'responsable': user_db
                })
            
            return laboratorios_detallados
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id_with_details(self, id_laboratorio: int) -> Optional[dict]:
        try:
            statement = select(LaboratorioDB, UserDB).join(
                UserDB, LaboratorioDB.responsable_id == UserDB.id_usuario, isouter=True
            ).where(LaboratorioDB.id_laboratorio == id_laboratorio)
            result = self.session.exec(statement).first()
            
            if result:
                laboratorio_db, user_db = result
                return {
                    'laboratorio': laboratorio_db,
                    'responsable': user_db
                }
            return None
        except Exception as e:
            raise e

    def get_by_responsable_with_details(self, responsable_id: int) -> List[dict]:
        try:
            statement = select(LaboratorioDB, UserDB).join(
                UserDB, LaboratorioDB.responsable_id == UserDB.id_usuario
            ).where(LaboratorioDB.responsable_id == responsable_id)
            results = self.session.exec(statement).all()
            
            laboratorios_detallados = []
            for laboratorio_db, user_db in results:
                laboratorios_detallados.append({
                    'laboratorio': laboratorio_db,
                    'responsable': user_db
                })
            
            return laboratorios_detallados
        except Exception as e:
            raise e

    def get_by_nombre_with_details(self, nombre: str) -> Optional[dict]:
        try:
            statement = select(LaboratorioDB, UserDB).join(
                UserDB, LaboratorioDB.responsable_id == UserDB.id_usuario, isouter=True
            ).where(LaboratorioDB.nombre == nombre)
            result = self.session.exec(statement).first()
            
            if result:
                laboratorio_db, user_db = result
                return {
                    'laboratorio': laboratorio_db,
                    'responsable': user_db
                }
            return None
        except Exception as e:
            raise e