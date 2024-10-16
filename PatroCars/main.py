from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlmodel import SQLModel

from models import ModeloVeiculo, Montadora, Veiculo
from persistence.modelo_veiculo import ModeloVeiculoRepository
from persistence.montadora import MontadoraRepository
from persistence.utils import get_engine
from persistence.veiculo import VeiculoRepository

app = FastAPI()
templates = Jinja2Templates(directory="templates")
SQLModel.metadata.create_all(get_engine())

montadoras = MontadoraRepository()
modelos_veiculos = ModeloVeiculoRepository()
veiculos = VeiculoRepository()


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
        name="montadora_list.html",
        context={"montadoras": montadoras_list},
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


@app.get("/modelo_veiculo_list")
def listar_modelos(request: Request, ordenar_por: str = None, ordem: str = "asc"):
    modelos_list = modelos_veiculos.get_all()
    if ordenar_por:
        modelos_list = sorted(
            modelos_list,
            key=lambda x: getattr(x, ordenar_por),
            reverse=(ordem == "desc"),
        )

    return templates.TemplateResponse(
        request=request,
        name="modelo_veiculo_list.html",
        context={"modelos": modelos_list},
    )


@app.get("/modelo_veiculo_form")
def modelo_veiculo_form(request: Request):
    montadoras_list = montadoras.get_all()
    return templates.TemplateResponse(
        "modelo_veiculo_form.html", {"request": request, "montadoras": montadoras_list}
    )


@app.post("/modelo_veiculo_form")
def criar_modelo_veiculo(
    nome: str = Form(...),
    montadora_id: str = Form(...),
    valor_referencia: float = Form(...),
    motorizacao: int = Form(...),
    turbo: bool = Form(...),
    automatico: bool = Form(...),
):
    novo_modelo = ModeloVeiculo(
        nome=nome,
        montadora_id=montadora_id,
        valor_referencia=valor_referencia,
        motorizacao=motorizacao,
        turbo=turbo,
        automatico=automatico,
    )
    modelos_veiculos.save(novo_modelo)
    return {"message": "Modelo de Veículo criado com sucesso!"}


@app.put("/modelo_veiculo_update/{id}")
def atualizar_modelo_veiculo(
    id: str,
    nome: str = Form(...),
    montadora_id: str = Form(...),
    valor_referencia: float = Form(...),
    motorizacao: int = Form(...),
    turbo: bool = Form(...),
    automatico: bool = Form(...),
):
    modelo = ModeloVeiculo(
        id=id,
        nome=nome,
        montadora_id=montadora_id,
        valor_referencia=valor_referencia,
        motorizacao=motorizacao,
        turbo=turbo,
        automatico=automatico,
    )
    atualizado = modelos_veiculos.update(modelo)
    if atualizado:
        return {"message": "Modelo de Veículo atualizado com sucesso!"}
    return {"error": "Modelo de Veículo não encontrado"}


@app.delete("/modelo_veiculo_delete/{id}")
def remover_modelo_veiculo(id: str):
    removido = modelos_veiculos.delete(id)
    if removido:
        return {"message": "Modelo de Veículo removido com sucesso!"}
    return {"error": "Modelo de Veículo não encontrado"}


@app.get("/veiculo_list")
def listar_veiculos(request: Request, ordenar_por: str = None, ordem: str = "asc"):
    veiculos_list = veiculos.get_all()
    if ordenar_por:
        veiculos_list = sorted(
            veiculos_list,
            key=lambda x: getattr(x, ordenar_por),
            reverse=(ordem == "desc"),
        )

    return templates.TemplateResponse(
        request=request, name="veiculo_list.html", context={"veiculos": veiculos_list}
    )


@app.get("/veiculo_form")
def veiculo_form(request: Request):
    modelos_list = modelos_veiculos.get_all()
    return templates.TemplateResponse(
        "veiculo_form.html", {"request": request, "modelos": modelos_list}
    )


@app.post("/veiculo_form")
def criar_veiculo(
    modelo_id: str = Form(...),
    cor: str = Form(...),
    ano_fabricacao: int = Form(...),
    ano_modelo: int = Form(...),
    valor: float = Form(...),
    placa: str = Form(...),
):
    novo_veiculo = Veiculo(
        modelo_id=modelo_id,
        cor=cor,
        ano_fabricacao=ano_fabricacao,
        ano_modelo=ano_modelo,
        valor=valor,
        placa=placa,
        vendido=False,  # Inicializado como não vendido
    )
    veiculos.save(novo_veiculo)
    return {"message": "Veículo cadastrado com sucesso!"}


@app.put("/veiculo_update/{id}")
def atualizar_veiculo(
    id: str,
    cor: str = Form(...),
    ano_fabricacao: int = Form(...),
    ano_modelo: int = Form(...),
    valor: float = Form(...),
    placa: str = Form(...),
    vendido: bool = Form(...),
):
    veiculo = Veiculo(
        id=id,
        cor=cor,
        ano_fabricacao=ano_fabricacao,
        ano_modelo=ano_modelo,
        valor=valor,
        placa=placa,
        vendido=vendido,
    )
    atualizado = veiculos.update(veiculo)
    if atualizado:
        return {"message": "Veículo atualizado com sucesso!"}
    return {"error": "Veículo não encontrado"}


@app.delete("/veiculo_delete/{id}")
def remover_veiculo(id: str):
    removido = veiculos.delete(id)
    if removido:
        return {"message": "Veículo removido com sucesso!"}
    return {"error": "Veículo não encontrado"}


@app.post("/vender_veiculo/{id}")
def vender_veiculo(id: str):
    vendido = veiculos.marcar_vendido(id)
    if vendido:
        return {"message": "Veículo marcado como vendido!"}
    return {"error": "Veículo não encontrado"}


@app.get("/buscar_veiculo")
def buscar_veiculo(request: Request, placa: str = None):
    veiculo = veiculos.buscar_por_placa(placa)
    return {"veiculo": veiculo} if veiculo else {"error": "Veículo não encontrado"}
