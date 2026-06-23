## mensagem_de_erro_dblink

dblink_error_message — obtém a última mensagem de erro na conexão designada

## Sinopse

```
dblink_error_message(text connname) returns text
```

## Descrição

`dblink_error_message` obtém a mensagem de erro remota mais recente para uma conexão específica.

## Argumentos

*`connname`*: Nome da conexão a ser utilizada.

## Valor de retorno

Retorna a última mensagem de erro, ou `OK` se não houver havido nenhum erro nesta conexão.

## Notas

Quando as consultas assíncronas são iniciadas por `dblink_send_query`, a mensagem de erro associada à conexão pode não ser atualizada até que a mensagem de resposta do servidor seja consumida. Isso geralmente significa que `dblink_is_busy` ou `dblink_get_result` deve ser chamado antes de `dblink_error_message`, para que qualquer erro gerado pela consulta assíncrona seja visível.

## Exemplos

```
SELECT dblink_error_message('dtest1');
```
