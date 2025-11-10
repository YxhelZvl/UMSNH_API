# src/app/features/laboratorios/infrastructure/mappers/laboratorio_mapper.py
from src.app.features.laboratorios.domain.entities.laboratorio import Laboratorio
from src.app.features.laboratorios.infrastructure.models.laboratorio_model import LaboratorioDB
from src.app.features.laboratorios.domain.value_objects.nombre_laboratorio import NombreLaboratorio
from src.app.features.laboratorios.domain.value_objects.ubicacion_laboratorio import UbicacionLaboratorio

class LaboratorioMapper:
    @staticmethod
    def to_domain(laboratorio_db: LaboratorioDB) -> Laboratorio:
        if not laboratorio_db:
            return None
            
        return Laboratorio(
            id_laboratorio=laboratorio_db.id_laboratorio,
            nombre=NombreLaboratorio(valor=laboratorio_db.nombre),
            ubicacion=UbicacionLaboratorio(valor=laboratorio_db.ubicacion),
            responsable_id=laboratorio_db.responsable_id
        )

    @staticmethod
    def to_db(laboratorio: Laboratorio) -> LaboratorioDB:
        if not laboratorio:
            return None
            
        return LaboratorioDB(
            id_laboratorio=laboratorio.id_laboratorio,
            nombre=laboratorio.nombre.valor,
            ubicacion=laboratorio.ubicacion.valor,
            responsable_id=laboratorio.responsable_id
        )