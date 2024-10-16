from sqlmodel import Session, select
from .utils import get_engine
from models import Montadora


class MontadoraRepository:
    def __init__(self):
        self.session = Session(get_engine())

    def get_all(self):
        sttm = select(Montadora)
        return self.session.exec(sttm).all()

    def save(self, montadora: Montadora):
        self.session.add(montadora)
        self.session.commit()
        self.session.refresh(montadora)
        return montadora

    def update(self, montadora: Montadora):
        existing = self.session.get(Montadora, montadora.id)
        if existing:
            existing.nome = montadora.nome
            existing.pais = montadora.pais
            existing.ano_fundacao = montadora.ano_fundacao
            self.session.commit()
            return existing
        return None

    def delete(self, id: str):
        existing = self.session.get(Montadora, id)
        if existing:
            self.session.delete(existing)
            self.session.commit()
            return True
        return False
