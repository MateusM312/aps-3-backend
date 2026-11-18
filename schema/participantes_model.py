from pydantic import BaseModel

# ●  id 
# ●  nome 
# ●  email 
# ●  curso 

class Participante(BaseModel):
    # id: int | None = None # nao vai precisar
    nome: str
    email: str
    curso: str