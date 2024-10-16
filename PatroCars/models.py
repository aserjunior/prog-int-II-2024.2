import ulid
from sqlmodel import Field, SQLModel


class Montadora(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ulid.ULID()), primary_key=True)
    nome: str
    pais: str
    ano_fundacao: int


class ModeloVeiculo(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ulid.ULID()), primary_key=True)
    nome: str
    montadora_id: str = Field(foreign_key="montadora.id")
    valor_referencia: float
    motorizacao: int
    turbo: bool
    automatico: bool


class Veiculo(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ulid.ULID()), primary_key=True)
    modelo_id: str = Field(foreign_key="modeloveiculo.id")
    cor: str
    ano_fabricacao: int
    ano_modelo: int
    valor: float
    placa: str
    vendido: bool = False
