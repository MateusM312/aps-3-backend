# Gerenciamento de Eventos Acadêmicos

### Santana & Mendes

API REST para gerenciar eventos acadêmicos, participantes e inscrições, com os dados guardados em um banco SQLite e relatórios consolidados.

---

## 1. Descrição do Projeto

API desenvolvida com **FastAPI** que substitui o armazenamento em memória por um banco de dados relacional (SQLite), acessado com **SQLAlchemy ORM**. Os dados continuam disponíveis depois que a aplicação é encerrada e iniciada de novo.

### Funcionalidades

- CRUD completo de eventos: título, descrição, data, horário, local, capacidade e categoria.
- CRUD completo de participantes: nome, e-mail e curso.
- Inscrição de participantes em eventos, com validações:
  - o evento precisa existir;
  - o participante precisa existir;
  - o participante não pode se inscrever duas vezes no mesmo evento;
  - o evento precisa ter vagas disponíveis.
- Listagem dos participantes inscritos em cada evento.
- Três relatórios consolidados, calculados diretamente a partir do banco.

### Tecnologias utilizadas

Python, FastAPI, SQLAlchemy, Pydantic, SQLite e Uvicorn.

---

## 2. Instruções para Instalação

### Requisitos

- Python 3.10 ou superior.
- Git (para baixar o projeto).

### Passo 1 — Baixar o projeto

```bash
git clone https://github.com/MateusM312/aps-3-backend.git
cd aps-3-backend
```

Dentro dessa pasta ficam o `main.py` e o `requirements.txt`.

### Passo 2 — Criar o ambiente virtual

```bash
python -m venv venv
```

### Passo 3 — Ativar o ambiente virtual

**Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```bash
venv\Scripts\activate.bat
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

Quando o ambiente estiver ativo, aparece `(venv)` no começo da linha do terminal.

### Passo 4 — Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## 3. Instruções para Execução

Com o ambiente virtual ativado, execute dentro da pasta do projeto (onde está o `main.py`):

```bash
uvicorn main:app --reload
```

Deixe esse terminal aberto enquanto usa a API. Para parar o servidor, use `Ctrl + C`.

A API fica disponível em:

```text
http://127.0.0.1:8000
```

Documentação interativa (Swagger UI), onde é possível testar todas as rotas:

```text
http://127.0.0.1:8000/docs
```

Documentação alternativa (ReDoc):

```text
http://127.0.0.1:8000/redoc
```

As tabelas do banco são criadas automaticamente na primeira execução, por meio de `Base.metadata.create_all` no arquivo `main.py`.

---

## 4. Estrutura do Projeto

```text
aps-3-backend/
│
├── main.py
├── database.py
├── eventos-academicos.db
├── requirements.txt
├── README.md
│
├── models/
│   └── model.py
│
├── schema/
│   ├── eventos_schema.py
│   ├── participantes_schema.py
│   └── relatorio_schema.py
│
├── repositories/
│   ├── eventos_repository.py
│   ├── participantes_repository.py
│   └── relatorios_repository.py
│
├── services/
│   ├── eventos_services.py
│   ├── participantes_service.py
│   └── relatorios_service.py
│
└── routers/
    ├── eventos_router.py
    ├── participantes_routers.py
    └── relatorios_router.py
```

### Organização das camadas

| Camada     | Pasta           | Responsabilidade                                                              |
| ---------- | --------------- | ----------------------------------------------------------------------------- |
| Router     | `routers/`      | Recebe as requisições HTTP e valida os dados de entrada.                      |
| Schema     | `schema/`       | Define os formatos de entrada e saída da API (Pydantic).                      |
| Service    | `services/`     | Aplica as regras de negócio e trata os erros HTTP.                            |
| Repository | `repositories/` | Faz as consultas e gravações no banco, incluindo as consultas dos relatórios. |
| Model      | `models/`       | Define as tabelas e os relacionamentos (SQLAlchemy).                          |
| Database   | `database.py`   | Configura a conexão e as sessões do banco.                                    |

Fluxo de funcionamento:

```text
Router → Service → Repository → Banco de Dados
```

---

## 5. Configuração do Banco de Dados

O projeto usa SQLite integrado ao SQLAlchemy.

### Localização

O arquivo do banco fica na raiz do projeto:

```text
eventos-academicos.db
```

A URL de conexão está no arquivo `database.py`:

```python
DATABASE_URL = "sqlite:///./eventos-academicos.db"
```

O caminho é relativo à pasta de onde o Uvicorn é executado. Por isso, inicie a API sempre dentro da pasta do projeto.

### Tabelas

**Participantes**

- id (chave primária)
- nome
- email (único)
- curso

**Eventos**

- id (chave primária)
- titulo
- descricao
- data
- horario
- local
- capacidade
- categoria

**Inscrições**

- id (chave primária)
- evento_id (chave estrangeira)
- participante_id (chave estrangeira)
- data_inscricao (preenchida automaticamente)

O par `evento_id` + `participante_id` tem restrição de unicidade, o que impede inscrições duplicadas.

### Exclusão e integridade dos dados

- **Evento:** ao excluir um evento, as inscrições dele são removidas em cascata.
- E-mails de participantes são únicos (restrição de unicidade no banco).

### Reinicialização do banco

Para começar com o banco vazio, pare a API e exclua o arquivo `eventos-academicos.db`. Ele será recriado na próxima execução.

---

## 6. Principais Rotas da API

### 6.1. Eventos

Prefixo: `/eventos`

| Método | Endpoint        | Funcionalidade   |
| ------ | --------------- | ---------------- |
| POST   | `/eventos/`     | Cadastrar evento |
| GET    | `/eventos/`     | Listar eventos   |
| GET    | `/eventos/{id}` | Consultar evento |
| PUT    | `/eventos/{id}` | Atualizar evento |
| DELETE | `/eventos/{id}` | Excluir evento   |

### 6.2. Inscrições

| Método | Endpoint                                            | Funcionalidade             |
| ------ | --------------------------------------------------- | -------------------------- |
| POST   | `/eventos/{evento_id}/inscricoes/{participante_id}` | Inscrever participante     |
| GET    | `/eventos/{evento_id}/inscricoes`                   | Listar inscritos do evento |

A inscrição retorna:

- 201: inscrição realizada.
- 404: evento ou participante não encontrado.
- 409: participante já inscrito ou evento sem vagas.

### 6.3. Participantes

Prefixo: `/participantes`

| Método | Endpoint              | Funcionalidade         |
| ------ | --------------------- | ---------------------- |
| POST   | `/participantes/`     | Cadastrar participante |
| GET    | `/participantes/`     | Listar participantes   |
| GET    | `/participantes/{id}` | Consultar participante |
| PUT    | `/participantes/{id}` | Atualizar participante |
| DELETE | `/participantes/{id}` | Excluir participante   |

### 6.4. Relatórios

Prefixo: `/relatorios`

| Método | Endpoint                           | Relatório              |
| ------ | ---------------------------------- | ---------------------- |
| GET    | `/relatorios/eventos/ocupacao`     | Ocupação dos eventos   |
| GET    | `/relatorios/eventos/categorias`   | Eventos por categoria  |
| GET    | `/relatorios/participantes/cursos` | Participação por curso |

Os detalhes de cada relatório estão na seção 7.

### 6.5. Outras rotas

| Método | Endpoint | Funcionalidade       |
| ------ | -------- | -------------------- |
| GET    | `/`      | Rota de teste da API |

### Códigos HTTP utilizados

- **200:** operação realizada com sucesso.
- **201:** recurso criado com sucesso.
- **404:** recurso não encontrado.
- **409:** conflito, como inscrição duplicada ou evento lotado.
- **422:** dados inválidos na validação do Pydantic.

### Validações de entrada

- Eventos: título com pelo menos um caractere e capacidade maior que zero.
- Participantes: nome com pelo menos um caractere e e-mail em formato válido.

---

## 7. Relatórios e Informações Consolidadas

Os relatórios são rotas GET que retornam JSON. Os valores são calculados a cada requisição, com consultas SQLAlchemy que usam agrupamento e agregação (`GROUP BY`, `COUNT` e `SUM`). Nada é definido manualmente no código: se os dados do banco mudam, o relatório muda.

### Como acessar os relatórios pela URL

1. Inicie a API (`uvicorn main:app --reload`) e deixe o terminal aberto.
2. Abra uma das URLs no navegador:

```text
http://127.0.0.1:8000/relatorios/eventos/ocupacao
http://127.0.0.1:8000/relatorios/eventos/categorias
http://127.0.0.1:8000/relatorios/participantes/cursos
```

3. Se o resultado for `[]`, ainda não há dados no banco. Cadastre eventos, participantes e inscrições (pelo `/docs` ou com `curl`) e atualize a página.

Os relatórios também podem ser executados no Swagger (`/docs`), com _Try it out_ e _Execute_.

### 7.1. Relatório de Ocupação dos Eventos

```http
GET /relatorios/eventos/ocupacao
```

Mostra a situação de cada evento: inscritos, vagas restantes e percentual de ocupação.

| Campo               | Descrição                             |
| ------------------- | ------------------------------------- |
| evento_id           | Identificador do evento               |
| titulo              | Nome do evento                        |
| capacidade          | Capacidade máxima de participantes    |
| total_inscritos     | Quantidade de participantes inscritos |
| vagas_disponiveis   | Quantidade de vagas restantes         |
| percentual_ocupacao | Percentual de ocupação do evento      |

Cálculos:

```text
Vagas disponíveis = Capacidade - Total de inscritos

Percentual de ocupação = (Total de inscritos / Capacidade) × 100
```

O percentual tem duas casas decimais.

Regras:

- Eventos sem inscrições aparecem com zero inscritos e 0,0% de ocupação.
- A divisão por zero é evitada: se a capacidade for zero, o percentual é 0,0%.
- As vagas disponíveis nunca ficam negativas.

Exemplo de resposta:

```json
[
  {
    "evento_id": 1,
    "titulo": "Introdução à Inteligência Artificial",
    "capacidade": 100,
    "total_inscritos": 75,
    "vagas_disponiveis": 25,
    "percentual_ocupacao": 75.0
  }
]
```

### 7.2. Relatório de Eventos por Categoria

```http
GET /relatorios/eventos/categorias
```

Agrupa os eventos pela categoria e mostra, para cada uma, a quantidade de eventos, a soma das capacidades e o total de inscrições.

| Campo            | Descrição                                    |
| ---------------- | -------------------------------------------- |
| categoria        | Categoria dos eventos                        |
| total_eventos    | Quantidade de eventos naquela categoria      |
| capacidade_total | Soma das capacidades dos eventos             |
| total_inscricoes | Total de inscrições nos eventos da categoria |

Exemplo de resposta:

```json
[
  {
    "categoria": "Palestra",
    "total_eventos": 5,
    "capacidade_total": 500,
    "total_inscricoes": 320
  }
]
```

### 7.3. Relatório de Participação por Curso

```http
GET /relatorios/participantes/cursos
```

Agrupa os participantes pelo curso.

| Campo               | Descrição                                                          |
| ------------------- | ------------------------------------------------------------------ |
| curso               | Nome do curso                                                      |
| total_participantes | Quantidade de participantes cadastrados no curso                   |
| total_inscricoes    | Quantidade total de inscrições feitas pelos participantes do curso |

Regras de contagem:

- Cada participante é contado uma única vez em `total_participantes`, mesmo com várias inscrições.
- Todas as inscrições dos participantes do curso entram em `total_inscricoes`.
- Um participante inscrito em três eventos representa 1 participante e 3 inscrições.

Exemplo de resposta:

```json
[
  {
    "curso": "Engenharia de Software",
    "total_participantes": 80,
    "total_inscricoes": 150
  }
]
```

### 7.4. Informações complementares

Listagem dos participantes inscritos em um evento:

```http
GET /eventos/{evento_id}/inscricoes
```

Controle de vagas: ao tentar inscrever um participante em um evento lotado, a API retorna erro 409.

```http
POST /eventos/{evento_id}/inscricoes/{participante_id}
```

---

## 8. Exemplos de Utilização da API

Os exemplos podem ser executados com `curl` ou pelo Swagger (`http://127.0.0.1:8000/docs`).

### 8.1. Cadastrar um evento

```bash
curl -X POST http://127.0.0.1:8000/eventos/ \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Semana de Tecnologia",
    "descricao": "Palestras e oficinas sobre tecnologia",
    "data": "2026-12-10",
    "horario": "19:00:00",
    "local": "Auditório Principal",
    "capacidade": 50,
    "categoria": "Palestra"
  }'
```

Resposta esperada (201):

```json
{
  "titulo": "Semana de Tecnologia",
  "descricao": "Palestras e oficinas sobre tecnologia",
  "data": "2026-12-10",
  "horario": "19:00:00",
  "local": "Auditório Principal",
  "capacidade": 50,
  "categoria": "Palestra",
  "id": 1
}
```

### 8.2. Cadastrar um participante

```bash
curl -X POST http://127.0.0.1:8000/participantes/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Maria Silva",
    "email": "maria@email.com",
    "curso": "Engenharia de Software"
  }'
```

Resposta esperada (201):

```json
{
  "nome": "Maria Silva",
  "email": "maria@email.com",
  "curso": "Engenharia de Software",
  "id": 1
}
```

### 8.3. Inscrever participante em evento

```bash
curl -X POST http://127.0.0.1:8000/eventos/1/inscricoes/1
```

Resposta esperada (201):

```json
{
  "Alerta": "Inscrição realizada com sucesso"
}
```

### 8.4. Listar participantes inscritos

```bash
curl http://127.0.0.1:8000/eventos/1/inscricoes
```

Resposta esperada (200):

```json
[
  {
    "nome": "Maria Silva",
    "email": "maria@email.com",
    "curso": "Engenharia de Software",
    "id": 1
  }
]
```

### 8.5. Atualizar um participante

```bash
curl -X PUT http://127.0.0.1:8000/participantes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Maria Silva Souza",
    "email": "maria@email.com",
    "curso": "Ciência da Computação"
  }'
```

### 8.6. Excluir um evento

```bash
curl -X DELETE http://127.0.0.1:8000/eventos/1
```

Resposta esperada (200):

```json
{
  "mensagem": "Evento removido"
}
```

### 8.7. Consultar um relatório

```bash
curl http://127.0.0.1:8000/relatorios/eventos/ocupacao
```

Resposta esperada (200), com um evento de capacidade 50 e uma inscrição:

```json
[
  {
    "evento_id": 1,
    "titulo": "Semana de Tecnologia",
    "capacidade": 50,
    "total_inscritos": 1,
    "vagas_disponiveis": 49,
    "percentual_ocupacao": 2.0
  }
]
```

### 8.8. Exemplos de erros

**Evento inexistente (404):**

```json
{
  "detail": "Evento não encontrado"
}
```

**Inscrição duplicada (409):**

```json
{
  "detail": "Participante já inscrito neste evento"
}
```

**Evento lotado (409):**

```json
{
  "detail": "Evento sem vagas disponíveis"
}
```

---

## 9. Instruções para Reproduzir os Testes

Os testes são manuais e podem ser feitos pelo Swagger (`/docs`) ou com `curl`. O projeto ainda não tem testes automatizados.

### 9.1. Preparação

Opcionalmente, exclua o arquivo `eventos-academicos.db` para começar com o banco vazio. Depois inicie a API:

```bash
uvicorn main:app --reload
```

### 9.2. Testes de eventos

- POST `/eventos/` com os dados do exemplo: esperado 201.
- GET `/eventos/`: o evento criado deve aparecer na lista.
- GET `/eventos/1`: esperado 200.
- GET `/eventos/999`: esperado 404.
- PUT `/eventos/1`: esperado 200 e dados atualizados.
- POST `/eventos/` com capacidade igual a zero: esperado 422.

### 9.3. Testes de participantes

- POST `/participantes/`: esperado 201.
- POST `/participantes/` com e-mail inválido: esperado 422.
- GET `/participantes/1`: esperado 200.
- GET `/participantes/999`: esperado 404.
- PUT `/participantes/1`: esperado 200 e dados atualizados.

### 9.4. Testes de inscrições

- POST `/eventos/1/inscricoes/1`: esperado 201.
- Repetir a mesma chamada: esperado 409 (inscrição duplicada).
- POST `/eventos/1/inscricoes/999`: esperado 404.
- POST `/eventos/999/inscricoes/1`: esperado 404.
- Criar um evento com capacidade 1, inscrever um participante e tentar inscrever um segundo: esperado 409 (sem vagas).
- GET `/eventos/1/inscricoes`: deve mostrar os participantes inscritos.

### 9.5. Teste de persistência (reinicialização)

1. Cadastre um evento e um participante.
2. Pare a API com `Ctrl + C`.
3. Inicie a API de novo (`uvicorn main:app --reload`).
4. Chame GET `/eventos/` e GET `/participantes/`: os registros devem continuar lá.

### 9.6. Testes dos relatórios

Faça estes testes depois de cadastrar eventos, participantes e inscrições.

**Ocupação** (`GET /relatorios/eventos/ocupacao`). Verificar:

- se existe um item para cada evento cadastrado;
- se eventos sem inscrições aparecem com zero inscritos e 0,0%;
- se eventos lotados aparecem com zero vagas e 100%;
- se o percentual corresponde aos inscritos e à capacidade.

**Categorias** (`GET /relatorios/eventos/categorias`). Verificar:

- se os eventos estão agrupados por categoria;
- se a quantidade de eventos corresponde aos registros;
- se a capacidade total é a soma das capacidades;
- se o total de inscrições corresponde às inscrições dos eventos da categoria.

**Cursos** (`GET /relatorios/participantes/cursos`). Verificar:

- se os participantes estão agrupados por curso;
- se cada participante é contado uma única vez;
- se todas as inscrições são contabilizadas;
- se um participante com duas inscrições resulta em 1 participante e 2 inscrições.

### 9.7. Os relatórios acompanham as mudanças nos dados

1. Consulte os três relatórios e anote os valores.
2. Faça uma nova inscrição e consulte de novo: `total_inscritos`, `vagas_disponiveis` e `total_inscricoes` devem aumentar.
3. Atualize o curso de um participante (PUT) e consulte `/relatorios/participantes/cursos`: os totais dos cursos devem mudar.
4. Exclua um evento (DELETE) e consulte os relatórios: o evento deve sumir da ocupação e os totais da categoria devem diminuir.

### 9.8. Testes de exclusão

- DELETE `/eventos/1`: esperado 200.
- As inscrições do evento devem ser removidas.
- GET `/eventos/1`: esperado 404.

---

## 10. Autores

**Santana & Mendes**
