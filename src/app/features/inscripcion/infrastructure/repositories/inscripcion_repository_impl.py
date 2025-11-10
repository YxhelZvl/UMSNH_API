# src/app/features/inscripcion/infrastructure/repositories/inscripcion_repository_impl.py
from typing import List, Optional
from sqlmodel import select, Session
from src.app.features.inscripcion.domain.repositories.inscripcion_repository import InscripcionRepository
from src.app.features.inscripcion.domain.entities.inscripcion import Inscripcion
from src.app.features.inscripcion.infrastructure.models.inscripcion_model import InscripcionDB
from src.app.features.inscripcion.infrastructure.mappers.inscripcion_mapper import InscripcionMapper
from src.app.features.inscripcion.domain.value_objects.estado_inscripcion import EstadoInscripcionEnum

class InscripcionRepositoryImpl(InscripcionRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Inscripcion]:
        try:
            statement = select(InscripcionDB)
            inscripciones_db = self.session.exec(statement).all()
            return [InscripcionMapper.to_domain(inscripcion_db) for inscripcion_db in inscripciones_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_inscripcion: int) -> Optional[Inscripcion]:
        try:
            inscripcion_db = self.session.get(InscripcionDB, id_inscripcion)
            return InscripcionMapper.to_domain(inscripcion_db) if inscripcion_db else None
        except Exception as e:
            raise e

    def get_by_usuario_id(self, id_usuario: int) -> List[Inscripcion]:
        try:
            statement = select(InscripcionDB).where(InscripcionDB.id_usuario == id_usuario)
            inscripciones_db = self.session.exec(statement).all()
            return [InscripcionMapper.to_domain(inscripcion_db) for inscripcion_db in inscripciones_db]
        except Exception as e:
            raise e

    def get_by_ciclo_id(self, id_ciclo: int) -> List[Inscripcion]:
        try:
            statement = select(InscripcionDB).where(InscripcionDB.id_ciclo == id_ciclo)
            inscripciones_db = self.session.exec(statement).all()
            return [InscripcionMapper.to_domain(inscripcion_db) for inscripcion_db in inscripciones_db]
        except Exception as e:
            raise e

    def get_inscripciones_activas_by_usuario(self, id_usuario: int) -> List[Inscripcion]:
        try:
            statement = select(InscripcionDB).where(
                InscripcionDB.id_usuario == id_usuario,
                InscripcionDB.estado == EstadoInscripcionEnum.ACTIVA.value
            )
            inscripciones_db = self.session.exec(statement).all()
            return [InscripcionMapper.to_domain(inscripcion_db) for inscripcion_db in inscripciones_db]
        except Exception as e:
            raise e

    def create(self, inscripcion: Inscripcion) -> Inscripcion:
        try:
            inscripcion_db = InscripcionMapper.to_db(inscripcion)
            self.session.add(inscripcion_db)
            self.session.commit()
            self.session.refresh(inscripcion_db)
            return InscripcionMapper.to_domain(inscripcion_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_inscripcion: int, inscripcion: Inscripcion) -> Optional[Inscripcion]:
        try:
            inscripcion_db = self.session.get(InscripcionDB, id_inscripcion)
            if inscripcion_db:
                inscripcion_db.estado = inscripcion.estado.valor.value
                self.session.add(inscripcion_db)
                self.session.commit()
                self.session.refresh(inscripcion_db)
                return InscripcionMapper.to_domain(inscripcion_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_inscripcion: int) -> bool:
        try:
            inscripcion_db = self.session.get(InscripcionDB, id_inscripcion)
            if inscripcion_db:
                self.session.delete(inscripcion_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def exists_inscripcion_activa(self, id_usuario: int, id_ciclo: int) -> bool:
        try:
            statement = select(InscripcionDB).where(
                InscripcionDB.id_usuario == id_usuario,
                InscripcionDB.id_ciclo == id_ciclo,
                InscripcionDB.estado == EstadoInscripcionEnum.ACTIVA.value
            )
            inscripcion_db = self.session.exec(statement).first()
            return inscripcion_db is not None
        except Exception as e:
            raise e

    def get_inscripciones_by_usuario_and_ciclo(self, id_usuario: int, id_ciclo: int) -> List[Inscripcion]:
        try:
            statement = select(InscripcionDB).where(
                InscripcionDB.id_usuario == id_usuario,
                InscripcionDB.id_ciclo == id_ciclo
            )
            inscripciones_db = self.session.exec(statement).all()
            return [InscripcionMapper.to_domain(inscripcion_db) for inscripcion_db in inscripciones_db]
        except Exception as e:
            raise e