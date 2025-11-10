# src/app/features/rol/infrastructure/repositories/rol_repository_impl.py
from typing import List, Optional
from sqlmodel import select, Session
from src.app.features.rol.domain.repositories.rol_repository import RolRepository
from src.app.features.rol.domain.entities.rol import Rol
from src.app.features.rol.infrastructure.models.rol_model import RolDB
from src.app.features.rol.infrastructure.mappers.rol_mapper import RolMapper

class RolRepositoryImpl(RolRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Rol]:
        try:
            statement = select(RolDB)
            roles_db = self.session.exec(statement).all()
            return [RolMapper.to_domain(rol_db) for rol_db in roles_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_rol: int) -> Optional[Rol]:
        try:
            rol_db = self.session.get(RolDB, id_rol)
            return RolMapper.to_domain(rol_db) if rol_db else None
        except Exception as e:
            raise e

    def get_by_tipo(self, tipo_rol: str) -> Optional[Rol]:
        try:
            statement = select(RolDB).where(RolDB.tipo_rol == tipo_rol)
            rol_db = self.session.exec(statement).first()
            return RolMapper.to_domain(rol_db) if rol_db else None
        except Exception as e:
            raise e

    def create(self, rol: Rol) -> Rol:
        try:
            rol_db = RolMapper.to_db(rol)
            self.session.add(rol_db)
            self.session.commit()
            self.session.refresh(rol_db)
            return RolMapper.to_domain(rol_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_rol: int, rol: Rol) -> Optional[Rol]:
        try:
            rol_db = self.session.get(RolDB, id_rol)
            if rol_db:
                # Actualizamos los campos
                rol_db.tipo_rol = rol.tipo_rol.valor
                self.session.add(rol_db)
                self.session.commit()
                self.session.refresh(rol_db)
                return RolMapper.to_domain(rol_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_rol: int) -> bool:
        try:
            rol_db = self.session.get(RolDB, id_rol)
            if rol_db:
                self.session.delete(rol_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def exists_by_tipo(self, tipo_rol: str) -> bool:
        try:
            statement = select(RolDB).where(RolDB.tipo_rol == tipo_rol)
            rol_db = self.session.exec(statement).first()
            return rol_db is not None
        except Exception as e:
            raise e