# src/app/features/maestros/infrastructure/repositories/maestro_repository_impl.py
from typing import List, Optional
from sqlmodel import select, Session
from src.app.features.maestros.domain.repositories.maestro_repository import MaestroRepository
from src.app.features.maestros.domain.entities.maestro import Maestro
from src.app.features.maestros.infrastructure.models.maestro_model import MaestroDB
from src.app.features.maestros.infrastructure.mappers.maestro_mapper import MaestroMapper
from src.app.features.user.infrastructure.models.user_model import UserDB

class MaestroRepositoryImpl(MaestroRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Maestro]:
        try:
            statement = select(MaestroDB)
            maestros_db = self.session.exec(statement).all()
            return [MaestroMapper.to_domain(maestro_db) for maestro_db in maestros_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_maestro: int) -> Optional[Maestro]:
        try:
            maestro_db = self.session.get(MaestroDB, id_maestro)
            return MaestroMapper.to_domain(maestro_db) if maestro_db else None
        except Exception as e:
            raise e

    def get_by_usuario_id(self, id_usuario: int) -> Optional[Maestro]:
        try:
            statement = select(MaestroDB).where(MaestroDB.id_usuario == id_usuario)
            maestro_db = self.session.exec(statement).first()
            return MaestroMapper.to_domain(maestro_db) if maestro_db else None
        except Exception as e:
            raise e

    def create(self, maestro: Maestro) -> Maestro:
        try:
            maestro_db = MaestroMapper.to_db(maestro)
            self.session.add(maestro_db)
            self.session.commit()
            self.session.refresh(maestro_db)
            return MaestroMapper.to_domain(maestro_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_maestro: int, maestro: Maestro) -> Optional[Maestro]:
        try:
            maestro_db = self.session.get(MaestroDB, id_maestro)
            if maestro_db:
                # En esta versión simple no hay campos para actualizar
                self.session.add(maestro_db)
                self.session.commit()
                self.session.refresh(maestro_db)
                return MaestroMapper.to_domain(maestro_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_maestro: int) -> bool:
        try:
            maestro_db = self.session.get(MaestroDB, id_maestro)
            if maestro_db:
                self.session.delete(maestro_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def exists_by_usuario_id(self, id_usuario: int) -> bool:
        try:
            statement = select(MaestroDB).where(MaestroDB.id_usuario == id_usuario)
            maestro_db = self.session.exec(statement).first()
            return maestro_db is not None
        except Exception as e:
            raise e

    # Implementación de métodos con JOINs para datos detallados
    def get_all_with_details(self) -> List[dict]:
        try:
            statement = select(MaestroDB, UserDB).join(UserDB, MaestroDB.id_usuario == UserDB.id_usuario)
            results = self.session.exec(statement).all()
            
            maestros_detallados = []
            for maestro_db, user_db in results:
                maestros_detallados.append({
                    'maestro': maestro_db,
                    'usuario': user_db
                })
            
            return maestros_detallados
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id_with_details(self, id_maestro: int) -> Optional[dict]:
        try:
            statement = select(MaestroDB, UserDB).join(
                UserDB, MaestroDB.id_usuario == UserDB.id_usuario
            ).where(MaestroDB.id_maestro == id_maestro)
            result = self.session.exec(statement).first()
            
            if result:
                maestro_db, user_db = result
                return {
                    'maestro': maestro_db,
                    'usuario': user_db
                }
            return None
        except Exception as e:
            raise e

    def get_by_usuario_id_with_details(self, id_usuario: int) -> Optional[dict]:
        try:
            statement = select(MaestroDB, UserDB).join(
                UserDB, MaestroDB.id_usuario == UserDB.id_usuario
            ).where(MaestroDB.id_usuario == id_usuario)
            result = self.session.exec(statement).first()
            
            if result:
                maestro_db, user_db = result
                return {
                    'maestro': maestro_db,
                    'usuario': user_db
                }
            return None
        except Exception as e:
            raise e