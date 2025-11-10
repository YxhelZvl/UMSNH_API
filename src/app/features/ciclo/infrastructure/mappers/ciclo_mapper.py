# src/app/features/ciclo/infrastructure/mappers/ciclo_mapper.py
from src.app.features.ciclo.domain.entities.ciclo import Ciclo
from src.app.features.ciclo.domain.value_objects.nombre_ciclo import NombreCicloValueObject
from src.app.features.ciclo.domain.value_objects.rango_fechas import RangoFechasValueObject
from src.app.features.ciclo.infrastructure.models.ciclo_model import CicloDB

class CicloMapper:
    @staticmethod
    def to_domain(ciclo_db: CicloDB) -> Ciclo:
        if not ciclo_db:
            return None
            
        return Ciclo(
            id_ciclo=ciclo_db.id_ciclo,
            ciclo=NombreCicloValueObject(valor=ciclo_db.ciclo),
            rango_fechas=RangoFechasValueObject(
                fecha_inicio=ciclo_db.fecha_inicio,
                fecha_final=ciclo_db.fecha_final
            )
        )

    @staticmethod
    def to_db(ciclo: Ciclo) -> CicloDB:
        if not ciclo:
            return None
            
        return CicloDB(
            id_ciclo=ciclo.id_ciclo,
            ciclo=ciclo.ciclo.valor,
            fecha_inicio=ciclo.rango_fechas.fecha_inicio,
            fecha_final=ciclo.rango_fechas.fecha_final
        )