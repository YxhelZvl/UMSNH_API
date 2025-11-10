# src/app/features/administrativo/infrastructure/repositories/administrativo_repository_impl.py
from typing import List, Optional
from sqlmodel import select, Session
from src.app.features.administrativo.domain.repositories.administrativo_repository import AdministrativoRepository
from src.app.features.administrativo.domain.entities.administrativo import Administrativo
from src.app.features.administrativo.infrastructure.models.administrativo_model import AdministrativoDB
from src.app.features.administrativo.infrastructure.mappers.administrativo_mapper import AdministrativoMapper
from src.app.features.user.infrastructure.models.user_model import UserDB

class AdministrativoRepositoryImpl(AdministrativoRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Administrativo]:
        try:
            statement = select(AdministrativoDB)
            administrativos_db = self.session.exec(statement).all()
            return [AdministrativoMapper.to_domain(admin_db) for admin_db in administrativos_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_administrativo: int) -> Optional[Administrativo]:
        try:
            administrativo_db = self.session.get(AdministrativoDB, id_administrativo)
            return AdministrativoMapper.to_domain(administrativo_db) if administrativo_db else None
        except Exception as e:
            raise e

    def get_by_usuario_id(self, id_usuario: int) -> Optional[Administrativo]:
        try:
            statement = select(AdministrativoDB).where(AdministrativoDB.id_usuario == id_usuario)
            administrativo_db = self.session.exec(statement).first()
            return AdministrativoMapper.to_domain(administrativo_db) if administrativo_db else None
        except Exception as e:
            raise e

    def get_by_departamento(self, departamento: str) -> List[Administrativo]:
        try:
            statement = select(AdministrativoDB).where(AdministrativoDB.departamento == departamento)
            administrativos_db = self.session.exec(statement).all()
            return [AdministrativoMapper.to_domain(admin_db) for admin_db in administrativos_db]
        except Exception as e:
            raise e

    def create(self, administrativo: Administrativo) -> Administrativo:
        try:
            administrativo_db = AdministrativoMapper.to_db(administrativo)
            self.session.add(administrativo_db)
            self.session.commit()
            self.session.refresh(administrativo_db)
            return AdministrativoMapper.to_domain(administrativo_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_administrativo: int, administrativo: Administrativo) -> Optional[Administrativo]:
        try:
            administrativo_db = self.session.get(AdministrativoDB, id_administrativo)
            if administrativo_db:
                administrativo_db.departamento = administrativo.departamento
                self.session.add(administrativo_db)
                self.session.commit()
                self.session.refresh(administrativo_db)
                return AdministrativoMapper.to_domain(administrativo_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_administrativo: int) -> bool:
        try:
            administrativo_db = self.session.get(AdministrativoDB, id_administrativo)
            if administrativo_db:
                self.session.delete(administrativo_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def exists_by_usuario_id(self, id_usuario: int) -> bool:
        try:
            statement = select(AdministrativoDB).where(AdministrativoDB.id_usuario == id_usuario)
            administrativo_db = self.session.exec(statement).first()
            return administrativo_db is not None
        except Exception as e:
            raise e

    # Implementación de métodos con JOINs para datos detallados
    def get_all_with_details(self) -> List[dict]:
        try:
            statement = select(AdministrativoDB, UserDB).join(UserDB, AdministrativoDB.id_usuario == UserDB.id_usuario)
            results = self.session.exec(statement).all()
            
            administrativos_detallados = []
            for administrativo_db, user_db in results:
                administrativos_detallados.append({
                    'administrativo': administrativo_db,
                    'usuario': user_db
                })
            
            return administrativos_detallados
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id_with_details(self, id_administrativo: int) -> Optional[dict]:
        try:
            statement = select(AdministrativoDB, UserDB).join(
                UserDB, AdministrativoDB.id_usuario == UserDB.id_usuario
            ).where(AdministrativoDB.id_administrativo == id_administrativo)
            result = self.session.exec(statement).first()
            
            if result:
                administrativo_db, user_db = result
                return {
                    'administrativo': administrativo_db,
                    'usuario': user_db
                }
            return None
        except Exception as e:
            raise e

    def get_by_usuario_id_with_details(self, id_usuario: int) -> Optional[dict]:
        try:
            statement = select(AdministrativoDB, UserDB).join(
                UserDB, AdministrativoDB.id_usuario == UserDB.id_usuario
            ).where(AdministrativoDB.id_usuario == id_usuario)
            result = self.session.exec(statement).first()
            
            if result:
                administrativo_db, user_db = result
                return {
                    'administrativo': administrativo_db,
                    'usuario': user_db
                }
            return None
        except Exception as e:
            raise e

    def get_by_departamento_with_details(self, departamento: str) -> List[dict]:
        try:
            statement = select(AdministrativoDB, UserDB).join(
                UserDB, AdministrativoDB.id_usuario == UserDB.id_usuario
            ).where(AdministrativoDB.departamento == departamento)
            results = self.session.exec(statement).all()
            
            administrativos_detallados = []
            for administrativo_db, user_db in results:
                administrativos_detallados.append({
                    'administrativo': administrativo_db,
                    'usuario': user_db
                })
            
            return administrativos_detallados
        except Exception as e:
            raise e