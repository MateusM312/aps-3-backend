# REPOSITORIO PARTICIPANTES

from sqlalchemy.orm import Session
from models import ParticipantesModel, EventoModel, InscricaoModel

def salvar(db: Session, participante: ParticipantesModel) -> ParticipantesModel:
    db.add(participante)
    db.commit()
    db.refresh(participante)
    return participante

def listar_participantes(db: Session, participante: ParticipantesModel):
    return db.query(participante).all()

def buscar_por_id(db: Session, participante: ParticipantesModel, id: int) -> ParticipantesModel | None:
    db.query(ParticipantesModel).filter(ParticipantesModel.id == id).first()
    return None

def excluir(db: Session, participante: ParticipantesModel, id: int) -> None:
    db.delete(participante)
    db.commit()

def atualizar(db: Session, participante: ParticipantesModel, id: int, dados) -> ParticipantesModel:
    participante.nome = dados.nome
    participante.email = dados.email
    participante.curso = dados.curso
    db.commit()
    db.refresh(participante)
    return participante


# Cadastrar participante: (CHECK)
# POST /participantes

# Listar participantes: (CHECK)
# GET /participantes

# Consultar participante: (CHECK)
# GET /participantes/{id}

# Atualizar participante: (CHECK)
# PUT /participantes/{id}

# Excluir participante: (CHECK)
# DELETE /participantes/{id}