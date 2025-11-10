# src/app/features/catalogo/infrastructure/mappers/catalogo_mapper.py
from src.app.features.catalogo.domain.entities.catalogo import Catalogo
from src.app.features.catalogo.infrastructure.models.catalogo_model import CatalogoDB
from src.app.features.catalogo.domain.value_objects.tipo_item import TipoItem
from src.app.features.catalogo.domain.value_objects.nombre_item import NombreItem
from src.app.features.catalogo.domain.value_objects.isbn import ISBN

class CatalogoMapper:
    @staticmethod
    def to_domain(catalogo_db: CatalogoDB) -> Catalogo:
        if not catalogo_db:
            return None
            
        return Catalogo(
            id_catalogo=catalogo_db.id_catalogo,
            tipo=TipoItem(valor=catalogo_db.tipo),
            nombre=NombreItem(valor=catalogo_db.nombre),
            autor=catalogo_db.autor,
            isbn=ISBN(valor=catalogo_db.isbn) if catalogo_db.isbn else None,
            descripcion=catalogo_db.descripcion
        )

    @staticmethod
    def to_db(catalogo: Catalogo) -> CatalogoDB:
        if not catalogo:
            return None
            
        return CatalogoDB(
            id_catalogo=catalogo.id_catalogo,
            tipo=catalogo.tipo.valor.value,
            nombre=catalogo.nombre.valor,
            autor=catalogo.autor,
            isbn=catalogo.isbn.valor if catalogo.isbn and catalogo.isbn.valor else None,
            descripcion=catalogo.descripcion
        )