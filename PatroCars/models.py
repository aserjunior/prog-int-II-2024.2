from sqlmodel import SQLModel, Field
import ulid


class Montadora(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ulid.ULID()), primary_key=True)
    nome: str
    pais: str
    ano_fundacao: int
