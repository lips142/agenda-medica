# Agenda Médica

Aplicação web simples para login de usuário e consulta de agendamentos médicos, desenvolvida como desafio técnico. Após autenticação, o sistema busca os agendamentos em uma API simulada e os exibe em uma tabela interativa, com suporte a busca por paciente, CPF ou médico.

## Tecnologias utilizadas

- **Python 3.11**
- **Flask** — framework web
- **Flask-SQLAlchemy** — ORM
- **Flask-Login** — gerenciamento de sessão/autenticação
- **SQLite** — banco de dados
- **Tabulator.js** — exibição interativa da tabela de agendamentos (via CDN)
- **Docker / Docker Compose** — containerização
- **Pytest** — testes automatizados

## Estrutura do projeto
```
agenda-medica/ 
├── app/ 
│ ├── init.py # application factory 
│ ├── config.py # configurações via variáveis de ambiente 
│ ├── extensions.py # instância do SQLAlchemy 
│ ├── models.py # modelo User 
│ ├── auth/ # login/logout 
│ ├── agenda/ # tela principal + lógica de busca/tratamento de falhas 
│ ├── api_mock/ # API simulada de agendamentos 
│ ├── templates/ 
│ └── static/ 
├── tests/ # testes automatizados 
├── seed.py # cria o banco e o usuário de teste 
├── run.py # entrypoint da aplicação 
├── requirements.txt
├── Dockerfile 
├── docker-compose.yml 
└── .env.example

## Como executar com Docker

Pré-requisitos: Docker e Docker Compose instalados.

```bash
docker compose up --build
```

Isso vai:
1. Construir a imagem da aplicação
2. Criar o banco SQLite e o usuário de teste automaticamente (via `seed.py`)
3. Subir a aplicação em `http://localhost:5000`

Acesse: **http://localhost:5000/login**

## Credenciais do usuário de teste

- **Usuário:** `admin`
- **Senha:** `admin123`

## Exemplos de uso

1. Acesse `http://localhost:5000/login` e entre com as credenciais acima.
2. Você será redirecionado para a tela principal, com a agenda carregada automaticamente.
3. Use o campo de busca para filtrar agendamentos por **paciente**, **CPF** ou **médico** (busca parcial, sem diferenciar maiúsculas/minúsculas).
4. Também é possível buscar os agendamentos diretamente pelo terminal, sem abrir o navegador:

```bash
docker compose exec web flask fetch-agenda
```

## Rodando os testes

Localmente (fora do Docker), com um ambiente virtual Python configurado:

```bash
pip install -r requirements.txt
pytest tests/
```

Ou dentro do container já em execução:

```bash
docker compose exec web pytest tests/
```

## Decisões técnicas

- **Camada de serviço separada da rota** (`agenda/services.py`): toda a lógica de busca, tratamento de erros de rede e validação de schema fica isolada da camada HTTP, facilitando testes unitários sem precisar de um cliente Flask completo.
- **Endpoint intermediário próprio** (`/api/agenda/dados`): o frontend (Tabulator) nunca chama a API mockada diretamente — ele passa pelo backend Flask, que trata erros, filtra e só então devolve os dados já validados. Isso evita expor detalhes da API externa ao navegador e centraliza o tratamento de falhas em um único lugar.
- **Validação de schema por item, não em bloco**: se um agendamento individual da API vier sem algum campo obrigatório, apenas ele é descartado (e logado como warning) — os demais continuam sendo exibidos normalmente, em vez de toda a listagem falhar por causa de um único registro malformado.
- **SQLite como arquivo único**, sem serviço de banco separado no Docker Compose, já que o requisito do desafio pede SQLite e essa abordagem elimina complexidade desnecessária de orquestração.
- **Persistência do banco via volume Docker** (`agenda_data:/app/instance`), garantindo que os dados não se percam entre reinícios do container.

## Cenários de falha tratados

| Cenário | Tratamento |
|---|---|
| Credenciais de login inválidas | Mensagem clara na tela de login, sem expor qual campo está incorreto |
| Nenhum agendamento encontrado | Mensagem "Nenhum agendamento encontrado" na tabela |
| Resposta vazia ou inválida da API | Tratado como lista vazia ou erro amigável, conforme o caso |
| Indisponibilidade temporária da API | Timeout e erro de conexão capturados, mensagem amigável exibida, erro completo registrado em log |
| Erro de conexão com o banco de dados | Erros do SQLAlchemy tratados nos handlers de erro globais da aplicação |
| Campos obrigatórios ausentes na resposta | Cada agendamento é validado individualmente; registros incompletos são descartados e logados, sem quebrar a listagem |

## Limitações conhecidas

- O comando `flask fetch-agenda` (entrega via terminal) foi interpretado como um comando CLI do Flask que imprime os agendamentos formatados no console, já que o requisito original é aberto quanto à forma de entrega via terminal.
- A API mockada retorna sempre o mesmo conjunto fixo de dados (não simula alterações reais de estado).
- Testes cobrem os principais fluxos (login válido/inválido, API indisponível, busca), mas não têm cobertura de 100% do código.
