# src/app/features/estudiante/infrastructure/mappers/estudiante_mapper.py
from src.app.features.estudiante.domain.entities.estudiante import Estudiante
from src.app.features.estudiante.infrastructure.models.estudiante_model import EstudianteDB

class EstudianteMapper:
    @staticmethod
    def to_domain(estudiante_db: EstudianteDB) -> Estudiante:
        if not estudiante_db:
            return None
            
        return Estudiante(
            id_estudiante=estudiante_db.id_estudiante,
            id_usuario=estudiante_db.id_usuario,
            id_carrera=estudiante_db.id_carrera
        )

    @staticmethod
    def to_db(estudiante: Estudiante) -> EstudianteDB:
        if not estudiante:
            return None
            
        return EstudianteDB(
            id_estudiante=estudiante.id_estudiante,
            id_usuario=estudiante.id_usuario,
            id_carrera=estudiante.id_carrera
        )