from sqlmodel import Session, select
from .utils import get_engine
from models import ModeloVeiculo, Montadora


class ModeloVeiculoRepository:
    def __init__(self):
        self.session = Session(get_engine())

    def get_all(self):
        sttm = select(ModeloVeiculo)
        return self.session.exec(sttm).all()

    def save(self, modelo_veiculo: ModeloVeiculo):
        montadora = self.session.get(Montadora, modelo_veiculo.montadora_id)
        if not montadora:
            raise ValueError("Montadora não encontrada.")

        self.session.add(modelo_veiculo)
        self.session.commit()
        self.session.refresh(modelo_veiculo)
        return modelo_veiculo

    def update(self, modelo_veiculo: ModeloVeiculo):
        existing = self.session.get(ModeloVeiculo, modelo_veiculo.id)
        if existing:
            existing.nome = modelo_veiculo.nome
            existing.montadora_id = modelo_veiculo.montadora_id
            existing.valor_referencia = modelo_veiculo.valor_referencia
            existing.motorizacao = modelo_veiculo.motorizacao
            existing.turbo = modelo_veiculo.turbo
            existing.automatico = modelo_veiculo.automatico
            self.session.commit()
            return existing
        return None

    def delete(self, id: str):
        existing = self.session.get(ModeloVeiculo, id)
        if existing:
            self.session.delete(existing)
            self.session.commit()
            return True
        return False
