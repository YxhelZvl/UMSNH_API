# src/app/features/carrera/infrastructure/repositories/carrera_repository_impl.py
from typing import List, Optional
from sqlmodel import select, Session
from src.app.features.carrera.domain.repositories.carrera_repository import CarreraRepository
from src.app.features.carrera.domain.entities.carrera import Carrera
from src.app.features.carrera.infrastructure.models.carrera_model import CarreraDB
from src.app.features.carrera.infrastructure.mappers.carrera_mapper import CarreraMapper

class CarreraRepositoryImpl(CarreraRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Carrera]:
        try:
            statement = select(CarreraDB)
            carreras_db = self.session.exec(statement).all()
            return [CarreraMapper.to_domain(carrera_db) for carrera_db in carreras_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_carrera: int) -> Optional[Carrera]:
        try:
            carrera_db = self.session.get(CarreraDB, id_carrera)
            return CarreraMapper.to_domain(carrera_db) if carrera_db else None
        except Exception as e:
            raise e

    def get_by_nombre(self, nombre_carrera: str) -> Optional[Carrera]:
        try:
            statement = select(CarreraDB).where(CarreraDB.carrera == nombre_carrera)
            carrera_db = self.session.exec(statement).first()
            return CarreraMapper.to_domain(carrera_db) if carrera_db else None
        except Exception as e:
            raise e

    def create(self, carrera: Carrera) -> Carrera:
        try:
            carrera_db = CarreraMapper.to_db(carrera)
            self.session.add(carrera_db)
            self.session.commit()
            self.session.refresh(carrera_db)
            return CarreraMapper.to_domain(carrera_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_carrera: int, carrera: Carrera) -> Optional[Carrera]:
        try:
            carrera_db = self.session.get(CarreraDB, id_carrera)
            if carrera_db:
                carrera_db.carrera = carrera.carrera.valor
                carrera_db.facultad = carrera.facultad.valor
                self.session.add(carrera_db)
                self.session.commit()
                self.session.refresh(carrera_db)
                return CarreraMapper.to_domain(carrera_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_carrera: int) -> bool:
        try:
            carrera_db = self.session.get(CarreraDB, id_carrera)
            if carrera_db:
                self.session.delete(carrera_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def exists_by_nombre(self, nombre_carrera: str) -> bool:
        try:
            statement = select(CarreraDB).where(CarreraDB.carrera == nombre_carrera)
            carrera_db = self.session.exec(statement).first()
            return carrera_db is not None
        except Exception as e:
            raise e