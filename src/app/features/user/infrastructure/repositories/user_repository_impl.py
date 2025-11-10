# src/app/features/user/infrastructure/repositories/user_repository_impl.py
from typing import List, Optional
from sqlmodel import select, Session
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.features.user.domain.entities.user import User
from src.app.features.user.infrastructure.models.user_model import UserDB
from src.app.features.user.infrastructure.mappers.user_mapper import UserMapper

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[User]:
        try:
            statement = select(UserDB)
            users_db = self.session.exec(statement).all()
            return [UserMapper.to_domain(user_db) for user_db in users_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_usuario: int) -> Optional[User]:
        try:
            user_db = self.session.get(UserDB, id_usuario)
            return UserMapper.to_domain(user_db) if user_db else None
        except Exception as e:
            raise e

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            statement = select(UserDB).where(UserDB.email == email)
            user_db = self.session.exec(statement).first()
            return UserMapper.to_domain(user_db) if user_db else None
        except Exception as e:
            raise e

    def get_by_matricula(self, matricula: str) -> Optional[User]:
        try:
            statement = select(UserDB).where(UserDB.matricula == matricula)
            user_db = self.session.exec(statement).first()
            return UserMapper.to_domain(user_db) if user_db else None
        except Exception as e:
            raise e

    def get_by_rol(self, id_rol: int) -> List[User]:
        try:
            statement = select(UserDB).where(UserDB.id_rol == id_rol)
            users_db = self.session.exec(statement).all()
            return [UserMapper.to_domain(user_db) for user_db in users_db]
        except Exception as e:
            raise e

    def create(self, user: User) -> User:
        try:
            user_db = UserMapper.to_db(user)
            self.session.add(user_db)
            self.session.commit()
            self.session.refresh(user_db)
            return UserMapper.to_domain(user_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_usuario: int, user: User) -> Optional[User]:
        try:
            user_db = self.session.get(UserDB, id_usuario)
            if user_db:
                # Actualizamos los campos
                user_db.nombre = user.nombre.valor
                user_db.apellidoP = user.apellidoP
                user_db.apellidoM = user.apellidoM
                user_db.matricula = user.matricula.valor
                user_db.email = user.email.valor
                user_db.contraseña = user.contraseña
                user_db.id_rol = user.id_rol
                user_db.status = "activo" if user.status else "inactivo"
                
                self.session.add(user_db)
                self.session.commit()
                self.session.refresh(user_db)
                return UserMapper.to_domain(user_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_usuario: int) -> bool:
        try:
            user_db = self.session.get(UserDB, id_usuario)
            if user_db:
                # Delete lógico: cambiar status a inactivo
                user_db.status = "inactivo"
                self.session.add(user_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def exists_by_email(self, email: str) -> bool:
        try:
            statement = select(UserDB).where(UserDB.email == email)
            user_db = self.session.exec(statement).first()
            return user_db is not None
        except Exception as e:
            raise e

    def exists_by_matricula(self, matricula: str) -> bool:
        try:
            statement = select(UserDB).where(UserDB.matricula == matricula)
            user_db = self.session.exec(statement).first()
            return user_db is not None
        except Exception as e:
            raise e