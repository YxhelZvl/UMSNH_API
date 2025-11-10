# src/app/features/estudiante/infrastructure/repositories/estudiante_repository_impl.py
from typing import List, Optional
from sqlmodel import select, Session
from src.app.features.estudiante.domain.repositories.estudiante_repository import EstudianteRepository
from src.app.features.estudiante.domain.entities.estudiante import Estudiante
from src.app.features.estudiante.infrastructure.models.estudiante_model import EstudianteDB
from src.app.features.estudiante.infrastructure.mappers.estudiante_mapper import EstudianteMapper
from src.app.features.user.infrastructure.models.user_model import UserDB
from src.app.features.carrera.infrastructure.models.carrera_model import CarreraDB
class EstudianteRepositoryImpl(EstudianteRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Estudiante]:
        try:
            statement = select(EstudianteDB)
            estudiantes_db = self.session.exec(statement).all()
            return [EstudianteMapper.to_domain(estudiante_db) for estudiante_db in estudiantes_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_estudiante: int) -> Optional[Estudiante]:
        try:
            estudiante_db = self.session.get(EstudianteDB, id_estudiante)
            return EstudianteMapper.to_domain(estudiante_db) if estudiante_db else None
        except Exception as e:
            raise e

    def get_by_usuario_id(self, id_usuario: int) -> Optional[Estudiante]:
        try:
            statement = select(EstudianteDB).where(EstudianteDB.id_usuario == id_usuario)
            estudiante_db = self.session.exec(statement).first()
            return EstudianteMapper.to_domain(estudiante_db) if estudiante_db else None
        except Exception as e:
            raise e

    def get_by_carrera_id(self, id_carrera: int) -> List[Estudiante]:
        try:
            statement = select(EstudianteDB).where(EstudianteDB.id_carrera == id_carrera)
            estudiantes_db = self.session.exec(statement).all()
            return [EstudianteMapper.to_domain(estudiante_db) for estudiante_db in estudiantes_db]
        except Exception as e:
            raise e

    def create(self, estudiante: Estudiante) -> Estudiante:
        try:
            estudiante_db = EstudianteMapper.to_db(estudiante)
            self.session.add(estudiante_db)
            self.session.commit()
            self.session.refresh(estudiante_db)
            return EstudianteMapper.to_domain(estudiante_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_estudiante: int, estudiante: Estudiante) -> Optional[Estudiante]:
        try:
            estudiante_db = self.session.get(EstudianteDB, id_estudiante)
            if estudiante_db:
                estudiante_db.id_carrera = estudiante.id_carrera
                self.session.add(estudiante_db)
                self.session.commit()
                self.session.refresh(estudiante_db)
                return EstudianteMapper.to_domain(estudiante_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_estudiante: int) -> bool:
        try:
            estudiante_db = self.session.get(EstudianteDB, id_estudiante)
            if estudiante_db:
                self.session.delete(estudiante_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def exists_by_usuario_id(self, id_usuario: int) -> bool:
        try:
            statement = select(EstudianteDB).where(EstudianteDB.id_usuario == id_usuario)
            estudiante_db = self.session.exec(statement).first()
            return estudiante_db is not None
        except Exception as e:
            raise e
        
    def get_all_with_details(self) -> List[dict]:
        """Obtener todos los estudiantes con JOIN para usuario y carrera"""
        try:
            statement = (
                select(EstudianteDB, UserDB, CarreraDB)
                .join(UserDB, EstudianteDB.id_usuario == UserDB.id_usuario)
                .join(CarreraDB, EstudianteDB.id_carrera == CarreraDB.id_carrera)
            )
            results = self.session.exec(statement).all()
            
            estudiantes_detallados = []
            for estudiante_db, user_db, carrera_db in results:
                estudiantes_detallados.append({
                    'estudiante': estudiante_db,
                    'usuario': user_db,
                    'carrera': carrera_db
                })
            
            return estudiantes_detallados
            
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id_with_details(self, id_estudiante: int) -> Optional[dict]:
        """Obtener estudiante por ID con JOIN"""
        try:
            statement = (
                select(EstudianteDB, UserDB, CarreraDB)
                .join(UserDB, EstudianteDB.id_usuario == UserDB.id_usuario)
                .join(CarreraDB, EstudianteDB.id_carrera == CarreraDB.id_carrera)
                .where(EstudianteDB.id_estudiante == id_estudiante)
            )
            result = self.session.exec(statement).first()
            
            if result:
                estudiante_db, user_db, carrera_db = result
                return {
                    'estudiante': estudiante_db,
                    'usuario': user_db,
                    'carrera': carrera_db
                }
            return None
            
        except Exception as e:
            raise e

    def get_by_usuario_id_with_details(self, id_usuario: int) -> Optional[dict]:
        """Obtener estudiante por ID de usuario con JOIN"""
        try:
            statement = (
                select(EstudianteDB, UserDB, CarreraDB)
                .join(UserDB, EstudianteDB.id_usuario == UserDB.id_usuario)
                .join(CarreraDB, EstudianteDB.id_carrera == CarreraDB.id_carrera)
                .where(EstudianteDB.id_usuario == id_usuario)
            )
            result = self.session.exec(statement).first()
            
            if result:
                estudiante_db, user_db, carrera_db = result
                return {
                    'estudiante': estudiante_db,
                    'usuario': user_db,
                    'carrera': carrera_db
                }
            return None
            
        except Exception as e:
            raise e

    def get_by_carrera_id_with_details(self, id_carrera: int) -> List[dict]:
        """Obtener estudiantes por ID de carrera con JOIN"""
        try:
            statement = (
                select(EstudianteDB, UserDB, CarreraDB)
                .join(UserDB, EstudianteDB.id_usuario == UserDB.id_usuario)
                .join(CarreraDB, EstudianteDB.id_carrera == CarreraDB.id_carrera)
                .where(EstudianteDB.id_carrera == id_carrera)
            )
            results = self.session.exec(statement).all()
            
            estudiantes_detallados = []
            for estudiante_db, user_db, carrera_db in results:
                estudiantes_detallados.append({
                    'estudiante': estudiante_db,
                    'usuario': user_db,
                    'carrera': carrera_db
                })
            
            return estudiantes_detallados
            
        except Exception as e:
            raise e