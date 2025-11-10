# src/app/features/catalogo/infrastructure/repositories/catalogo_repository_impl.py
from typing import List, Optional
from sqlmodel import select, Session
from src.app.features.catalogo.domain.repositories.catalogo_repository import CatalogoRepository
from src.app.features.catalogo.domain.entities.catalogo import Catalogo
from src.app.features.catalogo.infrastructure.models.catalogo_model import CatalogoDB
from src.app.features.catalogo.infrastructure.mappers.catalogo_mapper import CatalogoMapper

class CatalogoRepositoryImpl(CatalogoRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Catalogo]:
        try:
            statement = select(CatalogoDB)
            catalogos_db = self.session.exec(statement).all()
            return [CatalogoMapper.to_domain(cat_db) for cat_db in catalogos_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_catalogo: int) -> Optional[Catalogo]:
        try:
            catalogo_db = self.session.get(CatalogoDB, id_catalogo)
            return CatalogoMapper.to_domain(catalogo_db) if catalogo_db else None
        except Exception as e:
            raise e

    def get_by_nombre(self, nombre: str) -> Optional[Catalogo]:
        try:
            statement = select(CatalogoDB).where(CatalogoDB.nombre == nombre)
            catalogo_db = self.session.exec(statement).first()
            return CatalogoMapper.to_domain(catalogo_db) if catalogo_db else None
        except Exception as e:
            raise e

    def get_by_tipo(self, tipo: str) -> List[Catalogo]:
        try:
            statement = select(CatalogoDB).where(CatalogoDB.tipo == tipo)
            catalogos_db = self.session.exec(statement).all()
            return [CatalogoMapper.to_domain(cat_db) for cat_db in catalogos_db]
        except Exception as e:
            raise e

    def get_by_autor(self, autor: str) -> List[Catalogo]:
        try:
            statement = select(CatalogoDB).where(CatalogoDB.autor == autor)
            catalogos_db = self.session.exec(statement).all()
            return [CatalogoMapper.to_domain(cat_db) for cat_db in catalogos_db]
        except Exception as e:
            raise e

    def get_by_isbn(self, isbn: str) -> Optional[Catalogo]:
        try:
            if not isbn:
                return None
            statement = select(CatalogoDB).where(CatalogoDB.isbn == isbn)
            catalogo_db = self.session.exec(statement).first()
            return CatalogoMapper.to_domain(catalogo_db) if catalogo_db else None
        except Exception as e:
            raise e

    def create(self, catalogo: Catalogo) -> Catalogo:
        try:
            catalogo_db = CatalogoMapper.to_db(catalogo)
            self.session.add(catalogo_db)
            self.session.commit()
            self.session.refresh(catalogo_db)
            return CatalogoMapper.to_domain(catalogo_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_catalogo: int, catalogo: Catalogo) -> Optional[Catalogo]:
        try:
            catalogo_db = self.session.get(CatalogoDB, id_catalogo)
            if catalogo_db:
                catalogo_db.tipo = catalogo.tipo.valor.value
                catalogo_db.nombre = catalogo.nombre.valor
                catalogo_db.autor = catalogo.autor
                catalogo_db.isbn = catalogo.isbn.valor if catalogo.isbn and catalogo.isbn.valor else None
                catalogo_db.descripcion = catalogo.descripcion
                self.session.add(catalogo_db)
                self.session.commit()
                self.session.refresh(catalogo_db)
                return CatalogoMapper.to_domain(catalogo_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_catalogo: int) -> bool:
        try:
            catalogo_db = self.session.get(CatalogoDB, id_catalogo)
            if catalogo_db:
                self.session.delete(catalogo_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def exists_by_nombre(self, nombre: str) -> bool:
        try:
            statement = select(CatalogoDB).where(CatalogoDB.nombre == nombre)
            catalogo_db = self.session.exec(statement).first()
            return catalogo_db is not None
        except Exception as e:
            raise e

    def exists_by_isbn(self, isbn: str) -> bool:
        try:
            if not isbn:
                return False
            statement = select(CatalogoDB).where(CatalogoDB.isbn == isbn)
            catalogo_db = self.session.exec(statement).first()
            return catalogo_db is not None
        except Exception as e:
            raise e

    # Métodos para tipos específicos
    def get_libros(self) -> List[Catalogo]:
        try:
            statement = select(CatalogoDB).where(CatalogoDB.tipo == "libro")
            catalogos_db = self.session.exec(statement).all()
            print(catalogos_db)
            return [CatalogoMapper.to_domain(cat_db) for cat_db in catalogos_db]
        except Exception as e:
            raise e

    def get_herramientas(self) -> List[Catalogo]:
        try:
            statement = select(CatalogoDB).where(CatalogoDB.tipo == "herramienta")
            catalogos_db = self.session.exec(statement).all()
            return [CatalogoMapper.to_domain(cat_db) for cat_db in catalogos_db]
        except Exception as e:
            raise e

    def get_equipos(self) -> List[Catalogo]:
        try:
            statement = select(CatalogoDB).where(CatalogoDB.tipo == "equipo")
            catalogos_db = self.session.exec(statement).all()
            return [CatalogoMapper.to_domain(cat_db) for cat_db in catalogos_db]
        except Exception as e:
            raise e