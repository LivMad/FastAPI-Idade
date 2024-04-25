from pydantic import BaseModel, Field

import ulid
from time import time
from fastapi import FastAPI,HTTPException, status

dicionario = {}


class Contato(BaseModel):
    id: str
    nome: str
    idade: int
    data_criacao: float
    data_atualizacao: float


class NovoContato(BaseModel):
    id: str | None = Field(default_factory=lambda: str(ulid.new()))
    nome: str
    idade: int = Field(ge = 0, lt = 120 )
    data_criacao: float | None = Field(default_factory=time)
    data_atualizacao: float | None = Field(default_factory=time)


class EditarContato(BaseModel):
    nome: str | None = None
    idade: int | None = Field(default = None, ge = 0, lt = 120)

app = FastAPI()

@app.post("/cadastros/")
async def novo_cadastro(novo: NovoContato):
    dicionario[novo.id] = novo                                  # Método de adicionar em dicionário 
    return novo 

@app.get("/cadastros/{cadastro_id}")
async def get_cadastro(cadastro_id: str):
    if dicionario.get(cadastro_id) is not None:
        return dicionario.get(cadastro_id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id = {cadastro_id} não encontrado")    


@app.get("/cadastros/")
async def todos_cadastros():
    lista = []
    for chave, contato in dicionario.items():
        lista.append(Contato(**contato.model_dump()))
    return lista    

@app.patch("/cadastros/{cadastro_id}")
async def editar_contato(cadastro_id: str, contato_editado: EditarContato):
    if dicionario.get(cadastro_id) is not None:
        antigo_contato = dicionario[cadastro_id]
        if contato_editado.nome is not None:
            antigo_contato.nome = contato_editado.nome
        if contato_editado.idade is not None:
            antigo_contato.idade = contato_editado.idade
        antigo_contato.data_atualizacao = time()
        dicionario[cadastro_id] =  antigo_contato  
        return dicionario[cadastro_id] 
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id = {cadastro_id} não encontrado")    

@app.delete("/cadastros/{cadastro_id}")
async def deletar_cadastro(cadastro_id: str):
    if dicionario.get(cadastro_id) is not None:
        del dicionario[cadastro_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id = {cadastro_id} não encontrado")    
