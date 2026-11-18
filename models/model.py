from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint, DateTime
from sqlalchemy.sql import func # datetime e func servem para colocar automaticamente o horario
from sqlalchemy.orm import relationship

from database import Base

class ParticipantesModel(Base):
    __tablename__ ="participantes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    curso = Column(String, nullable=False)

class EventoModel(Base):
    __tablename__ ="eventos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data = Column(String, nullable=False)
    horario = Column(String, nullable=False)
    local = Column(String, nullable=False)
    capacidade = Column(Integer, nullable=False)
    categoria = Column(String, nullable=False)

    inscricoes = relationship("InscricaoModel", backref="evento", cascade="all, delete-orphan")

class InscricaoModel(Base):
    __tablename__ ="inscricoes"
    __table_args__ = (UniqueConstraint("evento_id", "participante_id"),)

    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    participante_id = Column(Integer, ForeignKey("participantes.id"), nullable=False)
    data_inscricao = Column(DateTime, server_default=func.now(), nullable=False)

# class Participante(BaseModel):
#     # id: int | None = None # nao vai precisar
#     nome: str
#     email: str
#     curso: str

# class Evento(BaseModel):
#     # id: int | None = None # acho q nn precisa por causa do banco de dados
#     titulo: str
#     descricao: str
#     data: str
#     horario: str
#     local: str
#     capacidade: int
#     categoria: str
