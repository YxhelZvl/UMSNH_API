# src/app/features/ejemplares/infrastructure/mappers/ejemplar_mapper.py
from src.app.features.ejemplares.domain.entities.ejemplar import Ejemplar
from src.app.features.ejemplares.infrastructure.models.ejemplar_model import EjemplarDB
from src.app.features.ejemplares.domain.value_objects.codigo_inventario import CodigoInventario
from src.app.features.ejemplares.domain.value_objects.ubicacion_ejemplar import UbicacionEjemplar
from src.app.features.ejemplares.domain.value_objects.estado_ejemplar import EstadoEjemplar

class EjemplarMapper:
    @staticmethod
    def to_domain(ejemplar_db: EjemplarDB) -> Ejemplar:
        if not ejemplar_db:
            return None
            
        return Ejemplar(
            id_ejemplar=ejemplar_db.id_ejemplar,
            id_catalogo=ejemplar_db.id_catalogo,
            codigo_inventario=CodigoInventario(valor=ejemplar_db.codigo_inventario),
            ubicacion=UbicacionEjemplar(valor=ejemplar_db.ubicacion),
            id_laboratorio=ejemplar_db.id_laboratorio,
            id_biblioteca=ejemplar_db.id_biblioteca,
            estado=EstadoEjemplar(valor=ejemplar_db.estado)
        )

    @staticmethod
    def to_db(ejemplar: Ejemplar) -> EjemplarDB:
        if not ejemplar:
            return None
            
        return EjemplarDB(
            id_ejemplar=ejemplar.id_ejemplar,
            id_catalogo=ejemplar.id_catalogo,
            codigo_inventario=ejemplar.codigo_inventario.valor,
            ubicacion=ejemplar.ubicacion.valor.value,
            id_laboratorio=ejemplar.id_laboratorio,
            id_biblioteca=ejemplar.id_biblioteca,
            estado=ejemplar.estado.valor.value
        )