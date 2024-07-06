from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  models import Base


class Smallword(Base):

    __tablename__ = 'smallword'

    id = Column("id", Integer, primary_key=True)
    name = Column(String(140))
    type = Column(String(2))
    description = Column(String(2000))

    def __init__(self, name, type, description):
        """
        Cria um minimundo

        Arguments:
            name: nome do produto.
            type: tipo de pessoa (pf ou pj)
            description: descrição do minimundo fornecida pelo cliente
        """
        self.name = name
        self.type = type
        self.description = description

    def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Produto.
        """
        return{
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description
        }

    def __repr__(self):
        """
        Retorna uma representação do Produto em forma de texto.
        """
        return f"Product(id={self.id}, name='{self.name}', type={self.type}, description='{self.description}')"
