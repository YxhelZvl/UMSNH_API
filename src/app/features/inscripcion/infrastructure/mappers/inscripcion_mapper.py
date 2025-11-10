# src/app/features/inscripcion/infrastructure/mappers/inscripcion_mapper.py
from src.app.features.inscripcion.domain.entities.inscripcion import Inscripcion
from src.app.features.inscripcion.domain.value_objects.estado_inscripcion import EstadoInscripcionValueObject, EstadoInscripcionEnum
from src.app.features.inscripcion.infrastructure.models.inscripcion_model import InscripcionDB

class InscripcionMapper:
    @staticmethod
    def to_domain(inscripcion_db: InscripcionDB) -> Inscripcion:
        if not inscripcion_db:
            return None
            
        return Inscripcion(
            id_inscripcion=inscripcion_db.id_inscripcion,
            id_usuario=inscripcion_db.id_usuario,
            id_ciclo=inscripcion_db.id_ciclo,
            fecha_inscripcion=inscripcion_db.fecha_inscripcion,
            estado=EstadoInscripcionValueObject(valor=EstadoInscripcionEnum(inscripcion_db.estado))
        )

    @staticmethod
    def to_db(inscripcion: Inscripcion) -> InscripcionDB:
        if not inscripcion:
            return None
            
        return InscripcionDB(
            id_inscripcion=inscripcion.id_inscripcion,
            id_usuario=inscripcion.id_usuario,
            id_ciclo=inscripcion.id_ciclo,
            fecha_inscripcion=inscripcion.fecha_inscripcion,
            estado=inscripcion.estado.valor.value
        )