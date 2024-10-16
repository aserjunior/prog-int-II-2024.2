from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlmodel import SQLModel

from models import Montadora
from persistence.montadora import MontadoraRepository
from persistence.utils import get_engine

app = FastAPI()
templates = Jinja2Templates(directory="templates")
SQLModel.metadata.create_all(get_engine())

montadoras = MontadoraRepository()


@app.get("/montadora_list")
def listar_montadoras(request: Request, ordenar_por: str = None, ordem: str = "asc"):
    montadoras_list = montadoras.get_all()
    if ordenar_por:
        montadoras_list = sorted(
            montadoras_list,
            key=lambda x: getattr(x, ordenar_por),
            reverse=(ordem == "desc"),
        )

    return templates.TemplateResponse(
        request=request,
        name='montadora_list.html',
        context={'montadoras': montadoras_list}
    )


@app.get("/montadora_form")
def montadora_form(request: Request):
    return templates.TemplateResponse("montadora_form.html", {"request": request})


@app.post("/montadora_form")
def criar_montadora(
    nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...)
):
    nova_montadora = Montadora(nome=nome, pais=pais, ano_fundacao=ano_fundacao)
    montadoras.save(nova_montadora)
    return {"message": "Montadora criada com sucesso!"}


@app.put("/montadora_update/{id}")
def atualizar_montadora(
    id: str, nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...)
):
    montadora = Montadora(id=id, nome=nome, pais=pais, ano_fundacao=ano_fundacao)
    atualizado = montadoras.update(montadora)
    if atualizado:
        return {"message": "Montadora atualizada com sucesso!"}
    return {"error": "Montadora não encontrada"}


@app.delete("/montadora_delete/{id}")
def remover_montadora(id: str):
    removido = montadoras.delete(id)
    if removido:
        return {"message": "Montadora removida com sucesso!"}
    return {"error": "Montadora não encontrada"}
