# src/app/features/maestros/infrastructure/mappers/maestro_mapper.py
from src.app.features.maestros.domain.entities.maestro import Maestro
from src.app.features.maestros.infrastructure.models.maestro_model import MaestroDB

class MaestroMapper:
    @staticmethod
    def to_domain(maestro_db: MaestroDB) -> Maestro:
        if not maestro_db:
            return None
            
        return Maestro(
            id_maestro=maestro_db.id_maestro,
            id_usuario=maestro_db.id_usuario
        )

    @staticmethod
    def to_db(maestro: Maestro) -> MaestroDB:
        if not maestro:
            return None
            
        return MaestroDB(
            id_maestro=maestro.id_maestro,
            id_usuario=maestro.id_usuario
        )