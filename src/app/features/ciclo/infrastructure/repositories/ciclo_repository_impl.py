# src/app/features/ciclo/infrastructure/repositories/ciclo_repository_impl.py
from typing import List, Optional
from datetime import date
from sqlmodel import select, Session
from src.app.features.ciclo.domain.repositories.ciclo_repository import CicloRepository
from src.app.features.ciclo.domain.entities.ciclo import Ciclo
from src.app.features.ciclo.infrastructure.models.ciclo_model import CicloDB
from src.app.features.ciclo.infrastructure.mappers.ciclo_mapper import CicloMapper

class CicloRepositoryImpl(CicloRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Ciclo]:
        try:
            statement = select(CicloDB)
            ciclos_db = self.session.exec(statement).all()
            return [CicloMapper.to_domain(ciclo_db) for ciclo_db in ciclos_db]
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, id_ciclo: int) -> Optional[Ciclo]:
        try:
            ciclo_db = self.session.get(CicloDB, id_ciclo)
            return CicloMapper.to_domain(ciclo_db) if ciclo_db else None
        except Exception as e:
            raise e

    def get_by_nombre(self, nombre_ciclo: str) -> Optional[Ciclo]:
        try:
            statement = select(CicloDB).where(CicloDB.ciclo == nombre_ciclo)
            ciclo_db = self.session.exec(statement).first()
            return CicloMapper.to_domain(ciclo_db) if ciclo_db else None
        except Exception as e:
            raise e

    def get_ciclos_activos(self) -> List[Ciclo]:
        try:
            today = date.today()
            statement = select(CicloDB).where(
                CicloDB.fecha_inicio <= today,
                CicloDB.fecha_final >= today
            )
            ciclos_db = self.session.exec(statement).all()
            return [CicloMapper.to_domain(ciclo_db) for ciclo_db in ciclos_db]
        except Exception as e:
            raise e

    def get_ciclos_por_fecha(self, fecha: date) -> List[Ciclo]:
        try:
            statement = select(CicloDB).where(
                CicloDB.fecha_inicio <= fecha,
                CicloDB.fecha_final >= fecha
            )
            ciclos_db = self.session.exec(statement).all()
            return [CicloMapper.to_domain(ciclo_db) for ciclo_db in ciclos_db]
        except Exception as e:
            raise e

    def create(self, ciclo: Ciclo) -> Ciclo:
        try:
            ciclo_db = CicloMapper.to_db(ciclo)
            self.session.add(ciclo_db)
            self.session.commit()
            self.session.refresh(ciclo_db)
            return CicloMapper.to_domain(ciclo_db)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, id_ciclo: int, ciclo: Ciclo) -> Optional[Ciclo]:
        try:
            ciclo_db = self.session.get(CicloDB, id_ciclo)
            if ciclo_db:
                ciclo_db.ciclo = ciclo.ciclo.valor
                ciclo_db.fecha_inicio = ciclo.rango_fechas.fecha_inicio
                ciclo_db.fecha_final = ciclo.rango_fechas.fecha_final
                self.session.add(ciclo_db)
                self.session.commit()
                self.session.refresh(ciclo_db)
                return CicloMapper.to_domain(ciclo_db)
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_ciclo: int) -> bool:
        try:
            ciclo_db = self.session.get(CicloDB, id_ciclo)
            if ciclo_db:
                self.session.delete(ciclo_db)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def exists_by_nombre(self, nombre_ciclo: str) -> bool:
        try:
            statement = select(CicloDB).where(CicloDB.ciclo == nombre_ciclo)
            ciclo_db = self.session.exec(statement).first()
            return ciclo_db is not None
        except Exception as e:
            raise e
        
    def get_last_cycle_id(self) -> Optional[int]:
        try:
            statement = select(CicloDB.id_ciclo).order_by(CicloDB.fecha_inicio.desc()).limit(1)
            result_id = self.session.exec(statement).first()
            return result_id
        except Exception as e:
            raise e