from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph
from pathlib import Path
import re

root = Path(r'D:/Usuários/Berk_/Desktop/atividade_fs')
doc_path = root / 'documentos/Questionario_Investigativo_Projeto_Full_Stack.docx'
doc = Document(doc_path)

answers = {
1: [
    'Executei `python -m uvicorn backend.app.main:app --port 8001`; o terminal informou “Uvicorn running on http://127.0.0.1:8001” e “Application startup complete”.',
    'Servidor respondeu em 200 na interface e no /docs. A instância já existente ocupava 8000; esta cópia foi executada em 8001 para isolar o exercício.',
    '`backend/app/main.py`: objeto `app` (FastAPI) e `lifespan`; comando Uvicorn: módulo `backend.app.main`, objeto `app` (`modulo:objeto`).',
    'O Uvicorn importa `backend.app.main:app` e passa a servir o objeto FastAPI. O `lifespan` executa `criar_tabela()` antes do `yield`; saída textual registrada no log de comandos.'
],
2: [
    'Abri a interface e a documentação Swagger no navegador local.',
    'Interface: http://127.0.0.1:8001/ (200). Swagger: http://127.0.0.1:8001/docs (200).',
    '`backend/app/main.py`: `abrir_interface()` serve `frontend/index.html`; `app = FastAPI(...)` fornece as rotas e a documentação `/docs`.',
    'São caminhos da mesma instância `app`: `/` entrega o HTML e `/docs` gera a documentação interativa automaticamente a partir das rotas registradas.'
],
3: [
    'Inspecionei `lifespan` e `criar_tabela` e reiniciei o servidor com uma reserva criada.',
    '`main.py`, linhas 14–17: `criar_tabela()` antes do `yield`. `database.py`, `CAMINHO_BANCO = .../dados/reservas.db` e SQL `CREATE TABLE IF NOT EXISTS`. Registro id 1 permaneceu após reinício.',
    '`backend/app/main.py`: `lifespan`; `backend/app/database.py`: `conectar()` e `criar_tabela()`; `backend/app/services.py`: `criar_reserva()`.',
    'A inicialização garante que a tabela exista. Os dados ficam no arquivo SQLite persistente `dados/reservas.db`; `CREATE TABLE IF NOT EXISTS` não recria nem apaga a tabela quando ela já existe. O SQL `INSERT INTO reservas` grava a reserva.'
],
4: [
    'Acompanhei o envio pela interface e localizei cada etapa no código.',
    'Fluxo executado com POST 201 e JSON contendo id 2 na criação pela interface.',
    '`frontend/index.html` (formulário); `frontend/app.js`: listener `submit`; `main.py`: `criar_reserva`; `schemas.py`: `ReservaEntrada`; `services.py`: `criar_reserva`; `database.py`: `conectar`.',
    'Clique em Salvar → evento `submit` → `fetch` POST `/api/reservas` com JSON → FastAPI valida `ReservaEntrada` → endpoint chama serviço → serviço verifica conflito e executa `INSERT INTO reservas` via SQLite → endpoint responde 201 e `lerResposta` atualiza mensagem, lista e resumo.'
],
5: [
    'Consultei no Swagger a operação `POST /api/reservas` e seu corpo/resposta documentados.',
    'Método POST; URL `/api/reservas`; corpo JSON: {"laboratorio":"Laboratório Evidência 6","data_reserva":"2026-11-05","turno":"noite","responsavel":"Matheus Prates Gaspar Silva","quantidade_pessoas":6,"finalidade":"Atividade investigativa Full Stack"}. Resposta observada: 201 e objeto equivalente com `id: 1`.',
    '`backend/app/main.py`: decoração de `criar_reserva`; `schemas.py`: `ReservaEntrada` (entrada) e `ReservaSaida` (saída).',
    'O método e a URL identificam a operação; o corpo define os campos aceitos; `ReservaEntrada` valida o formato e limites; `ReservaSaida` acrescenta o id; 201 informa que um recurso foi criado. Esses elementos formam o contrato que cliente e servidor seguem.'
],
6: [
    'Preenchi o formulário da interface com Laboratório Interface, data 05/11/2026, turno noite, responsável Matheus Prates Gaspar Silva, quantidade 6 e finalidade de evidência; cliquei Salvar.',
    'A interface mostrou “Sucesso: reserva 2 salva.”; resumo passou a total 2, noite 2 (registro id 2 na base de exercício). A rota retornou 201.',
    '`frontend/app.js`: handler `submit` monta `dadosDoFormulario()` e envia `fetch`; `backend/app/main.py`: `criar_reserva`; `backend/app/schemas.py`: `ReservaEntrada`.',
    'O handler envia JSON para POST `/api/reservas`; o FastAPI converte o corpo no modelo Pydantic, valida os campos e entrega os dados ao serviço. A resposta 201 é processada pelo frontend, que exibe sucesso e chama `listar()` para atualizar tabela e resumo.'
],
7: [
    'Conferi o status e a asserção do teste de criação.',
    'Criação válida retornou HTTP 201; `test_fluxo_criar_consultar_atualizar_excluir` verifica `criada.status_code == 201`.',
    '`backend/app/main.py`, decorator de `criar_reserva`: `status_code=status.HTTP_201_CREATED`; `tests/test_api.py`: `test_fluxo_criar_consultar_atualizar_excluir`.',
    '201 expressa criação concluída de um novo recurso. O backend configura esse status na rota POST e o teste protege o contrato verificando o código recebido pelo cliente.'
],
8: [
    'Enviei POST com `quantidade_pessoas: 0` e os demais campos válidos.',
    'Resposta 422; erro `greater_than_equal`, localização `body.quantidade_pessoas`, mensagem “Input should be greater than or equal to 1”, valor recebido 0 e contexto `ge: 1`.',
    '`backend/app/schemas.py`: campo `ReservaEntrada.quantidade_pessoas = Field(ge=1, le=40)`; `tests/test_api.py`: `test_rejeitar_quantidade_invalida`.',
    'O Pydantic rejeita o corpo antes de executar a rota porque zero fica abaixo do mínimo 1. O FastAPI converte a falha de validação em 422, com localização e regra violada no detalhe.'
],
9: [
    'Consultei `GET /api/reservas/999999`.',
    'Resposta 404 com detalhe “Reserva não encontrada”.',
    '`backend/app/main.py`: endpoint `consultar_reserva`; `backend/app/services.py`: `buscar_reserva`; teste `test_recurso_inexistente` em `tests/test_api.py`.',
    'O serviço consulta SQLite e devolve `None` se não encontrar linha. O endpoint decide a representação HTTP e transforma esse resultado em `HTTPException(404)`. A consulta é executada no serviço, mas o recurso inexistente é traduzido para o contrato HTTP pela API.'
],
10: [
    'Criei a reserva id 1, encerrei e reiniciei o processo Uvicorn na porta 8001 e consultei `GET /api/reservas/1`.',
    'Após o reinício, GET retornou 200 e os mesmos dados do registro id 1. O registro foi excluído ao final do exercício (DELETE 204).',
    '`backend/app/services.py`: `criar_reserva` contém `INSERT INTO reservas`; `backend/app/database.py`: `CAMINHO_BANCO` aponta para `dados/reservas.db`.',
    'A tabela e os registros ficam no arquivo persistente, não na memória do processo web. Reiniciar executa novamente `CREATE TABLE IF NOT EXISTS`, sem apagar linhas. O GET após reinício confirmou a permanência.'
],
11: [
    'Enviei duas criações com o mesmo laboratório, data e turno.',
    'Primeira tentativa: 201. Segunda tentativa: 409 com detalhe “Conflito: laboratório já reservado nessa data e turno”.',
    '`backend/app/services.py`: `existe_conflito` e `criar_reserva`; `backend/app/main.py`: `criar_reserva` captura `ValueError` e lança 409; `tests/test_api.py`: `test_rejeitar_conflito`.',
    'A consulta SQL procura combinação já existente. O serviço lança `ValueError`; o endpoint converte a regra de negócio em HTTP 409. O teste automatizado verifica o status e a mensagem de conflito.'
],
12: [
    'Enviei PUT para `/api/reservas/1`, mantendo todos os campos e alterando apenas `responsavel` para “Responsável Atualizado”.',
    'Resposta 200 com JSON da reserva id 1 e o responsável atualizado; os demais campos permaneceram iguais.',
    '`frontend/app.js`: modo edição no handler `submit` escolhe PUT; `backend/app/main.py`: `atualizar_reserva`; `backend/app/services.py`: `atualizar_reserva` executa `UPDATE`; teste CRUD em `tests/test_api.py`.',
    'O frontend seleciona PUT quando há id de edição e envia o JSON completo. O endpoint chama o serviço, que atualiza as colunas e busca o registro atualizado. A rota devolve 200 e o frontend mostra sucesso e atualiza a lista.'
],
13: [
    'Excluí a reserva id 1 e consultei o mesmo id em seguida.',
    'DELETE retornou 204 com corpo vazio; GET posterior retornou 404. A reserva de teste da interface também foi limpa após o exercício.',
    '`backend/app/main.py`: `excluir_reserva`; `backend/app/services.py`: `excluir_reserva`; `frontend/app.js`: `lerResposta` e `excluirReserva`; `tests/test_api.py`: teste do fluxo CRUD.',
    '204 indica sucesso sem conteúdo de resposta. `lerResposta` detecta `status === 204` e retorna `null` antes de tentar ler JSON; assim não tenta interpretar um corpo inexistente. A consulta posterior confirma que o registro foi removido.'
],
14: [
    'Consultei a lista com o filtro de turno noite.',
    'URL `GET /api/reservas?turno=noite`; resposta 200 com a reserva noturna id 1 antes da limpeza.',
    '`frontend/app.js`: `listar()` monta `URLSearchParams`; `backend/app/main.py`: `listar_reservas`; `backend/app/services.py`: `listar_reservas`.',
    'O frontend adiciona o parâmetro escolhido à query string. O endpoint encaminha `turno` ao serviço, que acrescenta `AND turno = ?` e o parâmetro correspondente à consulta SQL, evitando concatenar o valor diretamente no SQL.'
],
15: [
    'Consultei o resumo antes e depois de criar uma reserva noturna.',
    'Antes: total 0, noite 0. Depois: total 1, noite 1. Após excluir o registro, a base voltou ao total 0.',
    '`backend/app/services.py`: `obter_resumo`; `backend/app/main.py`: `obter_resumo`; `frontend/app.js`: `listar()` busca `/api/reservas/resumo` e atualiza `#resumo`.',
    'O serviço lista registros, inicializa contadores dos três turnos e soma cada reserva, retornando `total` e `por_turno`. O frontend renderiza esses valores; a inclusão de uma reserva noturna elevou ambos os contadores correspondentes em um.'
],
16: [
    'Executei `python -m pytest -v` na cópia atividade_fs usando o Python do ambiente virtual.',
    '7 testes passaram: 5 em `test_api.py` e 2 em `test_services.py`. Na execução final após restaurar a asserção, tempo 0,37 s; foi exibido um aviso de depreciação Starlette/httpx.',
    '`pytest.ini`: `testpaths = tests`; arquivos `tests/test_api.py` e `tests/test_services.py`; funções começam com `test_`.',
    'O pytest lê a configuração, busca arquivos `test_*.py` em `tests` e coleta funções `test_*`. O resultado nomeia cada teste e indica PASSED; o tempo e o aviso constam no terminal.'
],
17: [
    'Separei Arrange, Act e Assert no teste CRUD sem alterar o arquivo.',
    'Arrange: fixture `reserva_valida` recebida pelo teste. Act: `client.post`, `client.get`, `client.put`, `client.delete` e nova consulta. Assert: verificações de status 201/200/204/404 e campos retornados.',
    '`tests/test_api.py`: `test_fluxo_criar_consultar_atualizar_excluir`; fixture em `tests/conftest.py`: `reserva_valida`.',
    'Arrange prepara dados; Act executa operações; Assert compara resposta real ao contrato esperado. A sequência cobre criação, consulta, atualização e exclusão em uma única função.'
],
18: [
    '`TestClient` executa uma chamada de teste contra a aplicação ASGI em processo, sem abrir um servidor de rede.',
    'A suíte chamou `client.post` dentro de `with TestClient(app) as cliente`; FastAPI validou a entrada, executou endpoint e serviço, e devolveu resposta verificada pelo teste.',
    '`tests/conftest.py`: fixture `client`; `backend/app/main.py`: `app` e `criar_reserva`; `backend/app/services.py`: `criar_reserva`.',
    'A chamada atravessa o transporte ASGI de teste diretamente para `app`, passa pelo roteamento FastAPI e Pydantic, endpoint e serviço, grava no SQLite temporário e volta como objeto Response. Uvicorn só é necessário para escutar requisições externas; não participa do caminho em processo do TestClient.'
],
20: [
    'Troquei temporariamente a expectativa `201` por `202` em `tests/test_api.py`, executei apenas o teste CRUD e restaurei o arquivo original a partir de cópia de segurança.',
    'Falha provocada: `assert 201 == 202`; valor obtido 201, esperado 202. Depois da restauração, os 7 testes passaram (0,37 s).',
    '`tests/test_api.py`: `test_fluxo_criar_consultar_atualizar_excluir`; a linha original voltou a verificar `criada.status_code == 201`.',
    'A falha mostra que pytest apresenta o valor real e a expectativa divergente. A restauração foi confirmada pela execução completa subsequente, que terminou com 7 passed.'
],
21: [
    'Executei `python -m pytest --cov=backend.app --cov-report=term-missing`.',
    'Cobertura total: 94%. `services.py` teve 93%; linhas não cobertas incluem 16–17 (ramo de filtro por laboratório) e 71 (atualização de id inexistente). `main.py`: 92%.',
    '`backend/app/services.py`: `listar_reservas` e `atualizar_reserva`; `backend/app/main.py`: `abrir_interface` e ramo 404 de atualização.',
    'Dois cenários que elevariam cobertura: chamar GET com `?laboratorio=101` para percorrer a montagem LIKE (linhas 16–17); chamar PUT `/api/reservas/999999` para exercitar retorno None do serviço (linha 71) e 404 do endpoint. Também faltou GET `/` no teste para cobrir `abrir_interface`.'
],
22: [
    'Comparei o teste via cliente HTTP e o teste direto do serviço.',
    '`test_rejeitar_conflito` verifica POST 201 seguido de POST 409 e detalhe HTTP; `test_servico_impede_conflito` chama `services.criar_reserva` duas vezes e espera `ValueError`.',
    '`tests/test_api.py`: `test_rejeitar_conflito`; `tests/test_services.py`: `test_servico_impede_conflito`; regra em `backend/app/services.py`: `criar_reserva`.',
    'O primeiro integra validação, endpoint, tradução da exceção e resposta HTTP. O segundo isola a regra de negócio e seu erro, sem testar roteamento, JSON ou status HTTP. São camadas complementares.'
],
23: [
    'Completei a cadeia com identificadores encontrados no código.',
    'Evento `submit` → POST `/api/reservas` → resposta 201 → mensagem de sucesso e chamada `listar()` no frontend.',
    '`frontend/app.js`: listener `submit`, `dadosDoFormulario`, `lerResposta`, `listar`; `backend/app/main.py`: `criar_reserva`; `schemas.py`: `ReservaEntrada`; `services.py`: `criar_reserva`; `database.py`: `conectar`.',
    'Clique em Salvar → evento submit → `fetch` → POST `/api/reservas` → endpoint `criar_reserva(dados: ReservaEntrada)` → serviço `criar_reserva` → SQL `INSERT INTO reservas` → HTTP 201 com `ReservaSaida` → JavaScript mostra sucesso, limpa o formulário e atualiza tabela e resumo.'
],
24: [
    'Escolhi como defeito a API aceitar duas reservas para o mesmo laboratório, data e turno.',
    'A evidência seria duas tentativas idênticas recebendo 201, quando a segunda deveria retornar 409. No exercício observado, a primeira foi 201 e a segunda 409.',
    'Camada: regra de negócio em `backend/app/services.py`, funções `existe_conflito` e `criar_reserva`; proteção existente: `test_rejeitar_conflito` e `test_servico_impede_conflito`.',
    'A regressão poderia surgir se a verificação de conflito fosse removida. O teste de serviço protege a regra diretamente e o teste da API garante que a exceção seja apresentada como HTTP 409.'
]
}

# Identificação
for p in doc.paragraphs:
    if p.text.startswith('Data:'):
        p.text = 'Data: 05/11/2026    Turma: Engenharia de Software    Grupo: 6º Periodo'
        break
doc.tables[0].cell(1,0).text = 'Matheus Prates Gaspar Silva'
doc.tables[0].cell(1,1).text = '202411269'

# Preencher os campos da resposta sob cada questão numerada
question_re = re.compile(r'^(\d+)\.\s')
paras = doc.paragraphs
for i, p in enumerate(paras):
    m = question_re.match(p.text)
    if not m:
        continue
    n = int(m.group(1))
    if n not in answers:
        continue
    fields = {}
    for q in paras[i+1:]:
        if question_re.match(q.text):
            break
        if q.text.startswith('Ação executada:'):
            fields['acao'] = q
        elif q.text.startswith('Evidência:'):
            fields['evidencia'] = q
        elif q.text.startswith('Arquivo e função:'):
            fields['arquivo'] = q
        elif q.text.startswith('Explicação:'):
            fields['explicacao'] = q
        elif q.text.startswith('_'):
            q.text = ''
    if len(fields) == 4:
        for key, value in zip(('acao','evidencia','arquivo','explicacao'), answers[n]):
            label = {'acao':'Ação executada','evidencia':'Evidência','arquivo':'Arquivo e função','explicacao':'Explicação'}[key]
            fields[key].text = f'{label}: {value}'

# Questão 19 é apresentada em tabela no modelo
q19 = doc.tables[1]
q19vals = [
    'Localizei os três recursos na fixture e executei a suíte completa.',
    '`tmp_path` criou o diretório temporário; `monkeypatch` redirecionou `database.CAMINHO_BANCO` para `reservas_teste.db`; `with TestClient(app) as cliente` abriu e encerrou o contexto ASGI e o lifespan.',
    '`tests/conftest.py`: fixture `client`; `backend/app/database.py`: variável `CAMINHO_BANCO`. Banco normal `dados/reservas.db` permaneceu com 0 reservas antes/depois da suíte; os testes usam banco temporário.',
    'Cada teste recebe armazenamento isolado e descartável. `monkeypatch` restaura a variável ao fim do teste; TestClient inicia e finaliza a aplicação no contexto. A contagem zero no banco normal confirma que os testes não gravaram nele.'
]
for row, value in zip(q19.rows, q19vals):
    row.cells[1].text = value

# Registro de evidências de execução; a coluna de imagem permanece vazia conforme pedido.
anchor = next(p for p in doc.paragraphs if p.text == 'Registro de confronto entre execução e código')
heading = anchor.insert_paragraph_before('Resultados observados das evidências')
heading.style = 'Heading 1'
headers = ['Código', 'Registro de execução, código e teste associado', 'Captura']
t = doc.add_table(rows=1, cols=3)
t.style = 'Table Grid'
for c, text in zip(t.rows[0].cells, headers): c.text = text
rows = [
('E01','Uvicorn iniciou em http://127.0.0.1:8001; `main.py`, `app`/`lifespan`. Criar teste de inicialização se necessário.'),
('E02','Interface local retornou 200 e foi exibida; `main.py`, `abrir_interface`. Criar teste `client.get("/")`.'),
('E03','Swagger mostrou GET, POST, PUT e DELETE de `/api/reservas`; `app` gera OpenAPI. Criar verificação de `/openapi.json`.'),
('E04','POST de interface mostrou sucesso e POST válido retornou 201 + JSON; `app.js`, `criar_reserva`. `test_fluxo_criar_consultar_atualizar_excluir`.'),
('E05','Quantidade 0 retornou 422 e regra `ge=1`; `schemas.py`, `ReservaEntrada`. `test_rejeitar_quantidade_invalida`.'),
('E06','ID 999999 retornou 404; `main.py`, `consultar_reserva`. `test_recurso_inexistente`.'),
('E07','ID 1 foi encontrado após reiniciar; arquivo `dados/reservas.db`, `services.criar_reserva`. Propor teste de persistência separado.'),
('E08','Primeiro POST 201, segundo 409; `services.existe_conflito`, endpoint `criar_reserva`. `test_rejeitar_conflito` e `test_servico_impede_conflito`.'),
('E09','PUT retornou 200 e JSON com responsável atualizado; `atualizar_reserva` em endpoint/serviço. Coberto pelo teste CRUD.'),
('E10','DELETE retornou 204 sem corpo e GET seguinte 404; `excluir_reserva`, `lerResposta`. Coberto pelo teste CRUD.'),
('E11','Filtro noite trouxe o registro e resumo mudou de 0 para 1 à noite; `services.listar_reservas`/`obter_resumo`. `test_filtrar_e_resumir`.'),
('E12','7 testes passaram; cobertura total 94%; `tests/test_api.py` e `tests/test_services.py`. A suíte e pytest-cov registram esses comportamentos.')]
for code, detail in rows:
    cells = t.add_row().cells
    cells[0].text = code
    cells[1].text = detail
    cells[2].text = ''
# move newly appended table before the existing section anchor
t._tbl.addprevious(anchor._p)
# compact evidence table typography
for row in t.rows:
    for cell in row.cells:
        for p in cell.paragraphs:
            for r in p.runs: r.font.size = Pt(8)

# Save filled document

doc.save(doc_path)

log = '''ATIVIDADE FULL STACK — REGISTRO DE COMANDOS E RESULTADOS
Data de referência informada: 05/11/2026
Projeto: D:\\Usuários\\Berk_\\Desktop\\atividade_fs

AMBIENTE
python --version
Resultado: Python 3.12.5
python -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
Resultado: dependências instaladas (FastAPI, Uvicorn, Pydantic, pytest, pytest-cov e httpx).

SERVIDOR
.\\.venv\\Scripts\\python.exe -m uvicorn backend.app.main:app --port 8001
Resultado: Uvicorn running on http://127.0.0.1:8001; Application startup complete.
GET http://127.0.0.1:8001/
Resultado: 200 (interface)
GET http://127.0.0.1:8001/docs
Resultado: 200 (Swagger)

API EXERCITADA (base URL http://127.0.0.1:8001; script temporário work/exercicio_api.py)
POST /api/reservas com laboratório Laboratório Evidência 6, data 2026-11-05, turno noite, quantidade 6: 201, id 1.
POST /api/reservas com quantidade_pessoas=0: 422 (greater_than_equal, ge=1).
GET /api/reservas/999999: 404.
POST repetido para mesmo laboratório/data/turno: 409.
PUT /api/reservas/1 alterando apenas responsavel: 200.
GET /api/reservas?turno=noite: 200, reserva noturna encontrada.
Resumo antes/depois da criação: total 0/noite 0 → total 1/noite 1.
A interface também foi usada para criar a reserva id 2 e mostrou “Sucesso: reserva 2 salva.”

PERSISTÊNCIA E LIMPEZA
Servidor encerrado e iniciado novamente na porta 8001.
GET /api/reservas/1 após reinício: 200; registro permaneceu.
DELETE /api/reservas/1: 204; GET posterior: 404.
DELETE /api/reservas/2: 204. Banco de exercício terminou com lista vazia.
Banco normal dados/reservas.db permaneceu com 0 registros após a suíte.

TESTES
.\\.venv\\Scripts\\python.exe -m pytest -v
Resultado final após restauração do teste: 7 passed, 1 aviso, 0.37s.
.\\.venv\\Scripts\\python.exe -m pytest --cov=backend.app --cov-report=term-missing
Resultado: 7 passed; cobertura total 94%; main.py 92%; services.py 93%; schemas.py e database.py 100%.
Falha demonstrativa temporária: expectativa 202 para status da criação; obtido 201. O arquivo tests/test_api.py foi restaurado da cópia de segurança work/test_api.py.backup e a suíte completa foi executada novamente com sucesso.

OBSERVAÇÃO DE PORTA
A porta 8000 já estava ocupada por uma instância preexistente de outro diretório do mesmo projeto. A cópia solicitada em atividade_fs foi executada isoladamente na porta 8001. O registro id 7 criado durante a primeira verificação de disponibilidade na instância 8000 foi conferido pelos seus campos e removido (DELETE 204); nenhum outro registro foi alterado.
'''
(root / 'documentos/comandos_executados.txt').write_text(log, encoding='utf-8')
print(doc_path)
print(root / 'documentos/comandos_executados.txt')

