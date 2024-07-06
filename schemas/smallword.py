from pydantic import BaseModel
from typing import Optional, List
from models.smallword import Smallword


class SmallwordSchema(BaseModel):
    name: str = "Paulo Simao"
    type: str = "pf"
    description: str = "Quero um sistema de contabilidade, onde possa analizar e verificar os dados de um arquivo."


class SmallwordViewSchema(BaseModel):
    name: str = "Escola tecnica da Maria"
    type: str = "pj"
    description: str = "Quero um sistema que vai gerenciar um escola."


class SmallwordBuscaPorNomeSchema(BaseModel):
    termo: str = "Paulo Simao"


class SmallwordBuscaPorIDSchema(BaseModel):
    id: int = 2


class ListagemSmallwordsSchema(BaseModel):
    smallword:List[SmallwordViewSchema]


def apresenta_smallwords(smallwords: List[Smallword]):
    result = []
    for smallword in smallwords:
        result.append({
            "id": smallword.id,
            "name": smallword.name,
            "type": smallword.type,
            "description": smallword.description
        })

    return {"minimundos": result}

class SmallwordDelSchema(BaseModel):
    mesage: str
    id: int


def apresenta_smallword(smallword: Smallword):
    return {
        "id": smallword.id,
        "name": smallword.name,
        "type": smallword.type,
        "description": smallword.description
    }
