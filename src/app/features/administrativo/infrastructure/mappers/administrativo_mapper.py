# src/app/features/administrativo/infrastructure/mappers/administrativo_mapper.py
from src.app.features.administrativo.domain.entities.administrativo import Administrativo
from src.app.features.administrativo.infrastructure.models.administrativo_model import AdministrativoDB

class AdministrativoMapper:
    @staticmethod
    def to_domain(administrativo_db: AdministrativoDB) -> Administrativo:
        if not administrativo_db:
            return None
            
        return Administrativo(
            id_administrativo=administrativo_db.id_administrativo,
            id_usuario=administrativo_db.id_usuario,
            departamento=administrativo_db.departamento
        )

    @staticmethod
    def to_db(administrativo: Administrativo) -> AdministrativoDB:
        if not administrativo:
            return None
            
        return AdministrativoDB(
            id_administrativo=administrativo.id_administrativo,
            id_usuario=administrativo.id_usuario,
            departamento=administrativo.departamento
        )