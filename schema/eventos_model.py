# EVENTOS MODEL

from pydantic import BaseModel
class Evento(BaseModel):
    # id: int | None = None # acho q nn precisa por causa do banco de dados
    titulo: str
    descricao: str
    data: str
    horario: str
    local: str
    capacidade: int
    categoria: str


# ●  id 
# ●  titulo 
# ●  descricao 
# ●  data 
# ●  horario 
# ●  local 
# ●  capacidade 
# ●  categoria

# Exemplos de categorias: 
# ●  Palestra 
# ●  Workshop 
# ●  Minicurso 
# ●  Seminário 
# ●  Competição