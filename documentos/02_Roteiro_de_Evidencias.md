# Roteiro de evidências

As evidências devem mostrar somente a área necessária para comprovar o resultado. Cada imagem deve conter uma legenda curta informando ação, resultado e questão relacionada.

| Código | Evidência mínima | Questões |
|---|---|---|
| E01 | Terminal com Uvicorn iniciado | 1 |
| E02 | Interface e endereço no navegador | 2 |
| E03 | Swagger com as rotas disponíveis | 2 e 5 |
| E04 | Criação válida com resposta 201 e JSON | 6 e 7 |
| E05 | Validação rejeitada com 422 | 8 |
| E06 | Consulta inexistente com 404 | 9 |
| E07 | Registro existente após reiniciar | 10 |
| E08 | Duas tentativas e resposta 409 | 11 |
| E09 | Atualização por PUT | 12 |
| E10 | Exclusão 204 e consulta 404 | 13 |
| E11 | Filtro e resumo alterado | 14 e 15 |
| E12 | pytest e relatório de cobertura | 16 a 22 |

## Registro de confronto entre execução e código

Para cada evidência, informe:

1. O que foi executado.
2. O que foi observado.
3. Qual arquivo e função explicam o resultado.
4. Qual trecho confirma a explicação.
5. Qual teste protege esse comportamento ou qual teste deveria ser criado.
