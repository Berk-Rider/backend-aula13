# Projeto Integrador Full Stack

Aplicação didática de reservas de laboratórios para observar, localizar e explicar o fluxo completo:

`interface → Fetch API → rota FastAPI → validação Pydantic → serviço → SQLite → resposta HTTP → interface`

## Requisitos

- Python 3.10 ou superior
- VS Code recomendado

## Execução no PowerShell

```powershell
cd Projeto_Integrador_Full_Stack
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload
```

Abra `http://127.0.0.1:8000` e, para examinar a API diretamente, `http://127.0.0.1:8000/docs`.

## Testes

```powershell
python -m pytest -v
python -m pytest --cov=backend.app --cov-report=term-missing
```

Os testes usam um banco temporário. O banco da execução normal permanece em `dados/reservas.db`.

## Estrutura

```text
backend/app/main.py       rotas HTTP e inicialização
backend/app/schemas.py    modelos e validação
backend/app/services.py   regras de negócio e CRUD
backend/app/database.py   conexão e criação da tabela
frontend/                 interface e chamadas fetch
tests/                    testes automatizados
documentos/               questionário, evidências e guia docente
```

## Objetivo didático

Não basta informar que uma função existe. O estudante deve executar uma ação, registrar a evidência, localizar o código responsável e explicar a relação entre o código e o comportamento observado.
