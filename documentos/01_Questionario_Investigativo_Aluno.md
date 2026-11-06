# Questionário investigativo do projeto integrador Full Stack

## Identificação

Disciplina: Laboratório de Programação Full Stack  
Data: ____/____/________  Turma: ____________________  Grupo: __________

| Integrante | Matrícula |
|---|---|
| 1. | |
| 2. | |
| 3. | |
| 4. | |

## Regra de resposta

Cada resposta deve apresentar: **ação executada**, **evidência coletada**, **arquivo e função localizados** e **explicação da relação entre o código e o resultado**. Respostas apenas conceituais não atendem à atividade.

## Parte 1 Inicialização e arquitetura

1. Inicie a aplicação e registre a mensagem do terminal que prova que o servidor está disponível. Localize no comando executado o módulo e o objeto carregados pelo Uvicorn.
2. Abra a interface e o Swagger. Registre os dois endereços e explique por que ambos pertencem à mesma aplicação.
3. Localize o `lifespan`. Que instrução ocorre antes do `yield`? Mostre no código onde a tabela é criada e explique por que reiniciar não apaga os registros.
4. Desenhe o fluxo de uma criação desde o clique em Salvar até a gravação no SQLite. Para cada etapa, informe o arquivo correspondente.

## Parte 2 Contrato da API

5. No Swagger, identifique método, URL, corpo JSON, resposta e código HTTP da criação. Relacione cada item ao conceito de contrato da API.
6. Crie uma reserva válida pela interface. Registre a requisição no painel Rede do navegador ou repita a operação no Swagger. Localize a chamada `fetch`, a rota FastAPI e o modelo Pydantic envolvidos.
7. Explique por que a API devolve `201` e não `200` na criação. Localize a configuração desse código no backend e o teste que o verifica.
8. Envie `quantidade_pessoas` igual a zero pelo Swagger. Registre o `422`, identifique a informação de erro e localize a restrição correspondente no modelo.
9. Consulte um identificador inexistente. Registre o `404`, localize a decisão no endpoint e explique por que essa situação pertence à API, embora a busca ocorra no serviço.

## Parte 3 Persistência e regras

10. Crie uma reserva, encerre o servidor, reinicie e consulte novamente. Registre a evidência de permanência e localize a instrução SQL responsável pela gravação.
11. Cadastre duas reservas com o mesmo laboratório, data e turno. Registre a primeira resposta e a segunda. Localize a verificação do conflito, a conversão da exceção em `409` e o teste automatizado correspondente.
12. Altere apenas o responsável de uma reserva. Registre o `PUT`, o JSON devolvido e as instruções do frontend, endpoint e serviço que participam do fluxo.
13. Exclua uma reserva e tente consultá-la. Registre `204` e depois `404`. Explique por que uma resposta `204` não possui corpo e localize o tratamento desse caso no JavaScript.
14. Use o filtro de turno. Registre a URL com query string, o resultado exibido e a montagem dinâmica da consulta SQL.
15. Abra o resumo antes e depois de criar uma reserva noturna. Registre a mudança e localize a função que calcula `total` e `por_turno`.

## Parte 4 Testes automatizados

16. Execute `python -m pytest -v`. Registre o total de testes, o tempo e os estados apresentados. Explique como o pytest descobriu os arquivos e as funções.
17. Escolha o teste do fluxo CRUD. Separe no código os trechos Arrange, Act e Assert, mesmo que não estejam comentados com esses nomes.
18. Explique por que `TestClient` não exige Uvicorn. Indique o caminho percorrido por uma chamada `client.post` até a resposta testada.
19. Localize `tmp_path`, `monkeypatch` e `with TestClient(app) as cliente`. Explique o papel de cada elemento e apresente uma evidência de que o banco normal não foi alterado pela suíte.
20. Modifique temporariamente uma asserção correta para provocar uma falha. Registre a mensagem do pytest, identifique valor obtido e esperado e depois restaure o teste.
21. Execute a cobertura. Informe o percentual total, escolha duas linhas não cobertas e proponha cenários de teste capazes de executá-las.
22. Compare o teste `test_rejeitar_conflito` com `test_servico_impede_conflito`. Explique a diferença entre testar pela API e testar diretamente a regra de negócio.

## Parte 5 Síntese do fluxo

23. Complete a cadeia com nomes reais do projeto: evento da interface → função JavaScript → método e rota HTTP → função do endpoint → modelo → função do serviço → SQL → código HTTP → atualização da interface.
24. Escolha um defeito possível. Informe em qual camada ele surgiria, qual evidência o revelaria e qual teste deveria impedir sua volta.

## Entrega

- Questionário preenchido.
- Capturas numeradas E01 a E12 conforme o roteiro de evidências.
- Arquivo de texto com comandos executados.
- Indicação de arquivo, função e trecho de código em todas as questões que solicitam localização.
