from sqlmodel import Session, select

from models import ModeloVeiculo, Veiculo

from .utils import get_engine


class VeiculoRepository:
    def __init__(self):
        self.session = Session(get_engine())

    def get_all(self):
        sttm = select(Veiculo)
        return self.session.exec(sttm).all()

    def save(self, veiculo: Veiculo):
        # Verificar se o modelo existe
        modelo = self.session.get(ModeloVeiculo, veiculo.modelo_id)
        if not modelo:
            raise ValueError("Modelo não encontrado.")

        self.session.add(veiculo)
        self.session.commit()
        self.session.refresh(veiculo)
        return veiculo

    def update(self, veiculo: Veiculo):
        existing = self.session.get(Veiculo, veiculo.id)
        if existing:
            existing.cor = veiculo.cor
            existing.ano_fabricacao = veiculo.ano_fabricacao
            existing.ano_modelo = veiculo.ano_modelo
            existing.valor = veiculo.valor
            existing.placa = veiculo.placa
            existing.vendido = veiculo.vendido
            self.session.commit()
            return existing
        return None

    def delete(self, id: str):
        existing = self.session.get(Veiculo, id)
        if existing:
            self.session.delete(existing)
            self.session.commit()
            return True
        return False

    def marcar_vendido(self, id: str):
        veiculo = self.session.get(Veiculo, id)
        if veiculo:
            veiculo.vendido = True
            self.session.commit()
            return veiculo
        return None

    def buscar_por_placa(self, placa: str):
        sttm = select(Veiculo).where(Veiculo.placa == placa)
        return self.session.exec(sttm).first()

    def buscar_por_filtros(
        self,
        modelo_id=None,
        ano_fabricacao_min=None,
        ano_fabricacao_max=None,
        ano_modelo_min=None,
        ano_modelo_max=None,
        valor_min=None,
        valor_max=None,
        vendido=None,
    ):
        sttm = select(Veiculo)

        if modelo_id:
            sttm = sttm.where(Veiculo.modelo_id == modelo_id)
        if ano_fabricacao_min:
            sttm = sttm.where(Veiculo.ano_fabricacao >= ano_fabricacao_min)
        if ano_fabricacao_max:
            sttm = sttm.where(Veiculo.ano_fabricacao <= ano_fabricacao_max)
        if ano_modelo_min:
            sttm = sttm.where(Veiculo.ano_modelo >= ano_modelo_min)
        if ano_modelo_max:
            sttm = sttm.where(Veiculo.ano_modelo <= ano_modelo_max)
        if valor_min:
            sttm = sttm.where(Veiculo.valor >= valor_min)
        if valor_max:
            sttm = sttm.where(Veiculo.valor <= valor_max)
        if vendido is not None:
            sttm = sttm.where(Veiculo.vendido == vendido)

        return self.session.exec(sttm).all()
