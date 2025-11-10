# src/app/features/carrera/infrastructure/mappers/carrera_mapper.py
from src.app.features.carrera.domain.entities.carrera import Carrera
from src.app.features.carrera.domain.value_objects.nombre_carrera import NombreCarreraValueObject
from src.app.features.carrera.domain.value_objects.facultad import FacultadValueObject
from src.app.features.carrera.infrastructure.models.carrera_model import CarreraDB

class CarreraMapper:
    @staticmethod
    def to_domain(carrera_db: CarreraDB) -> Carrera:
        if not carrera_db:
            return None
            
        return Carrera(
            id_carrera=carrera_db.id_carrera,
            carrera=NombreCarreraValueObject(valor=carrera_db.carrera),
            facultad=FacultadValueObject(valor=carrera_db.facultad)
        )

    @staticmethod
    def to_db(carrera: Carrera) -> CarreraDB:
        if not carrera:
            return None
            
        return CarreraDB(
            id_carrera=carrera.id_carrera,
            carrera=carrera.carrera.valor,
            facultad=carrera.facultad.valor
        )