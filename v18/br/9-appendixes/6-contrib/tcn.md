## F.44. tcn — uma função de gatilho para notificar os ouvintes sobre mudanças no conteúdo da tabela [#](#TCN)

O módulo `tcn` fornece uma função de gatilho que notifica os ouvintes sobre as alterações em qualquer tabela à qual está anexado. Deve ser usado como um gatilho de `AFTER` `FOR EACH ROW`.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

Apenas um parâmetro pode ser fornecido à função em uma declaração `CREATE TRIGGER`, e isso é opcional. Se fornecido, ele será usado para o nome do canal para as notificações. Se omitido, `tcn` será usado para o nome do canal.

O conteúdo das notificações consiste no nome da tabela, uma letra para indicar que tipo de operação foi realizada e pares de nome/valor de coluna para colunas da chave primária. Cada parte é separada da próxima por uma vírgula. Para facilitar a análise usando expressões regulares, os nomes da tabela e das colunas são sempre envolvidos em aspas duplas, e os valores dos dados são sempre envolvidos em aspas simples. As aspas embutidas são duplicadas.

Segue um breve exemplo de uso da extensão.

```
test=# create table tcndata
test-#   (
test(#     a int not null,
test(#     b date not null,
test(#     c text,
test(#     primary key (a, b)
test(#   );
CREATE TABLE
test=# create trigger tcndata_tcn_trigger
test-#   after insert or update or delete on tcndata
test-#   for each row execute function triggered_change_notification();
CREATE TRIGGER
test=# listen tcn;
LISTEN
test=# insert into tcndata values (1, date '2012-12-22', 'one'),
test-#                            (1, date '2012-12-23', 'another'),
test-#                            (2, date '2012-12-23', 'two');
INSERT 0 3
Asynchronous notification "tcn" with payload ""tcndata",I,"a"='1',"b"='2012-12-22'" received from server process with PID 22770.
Asynchronous notification "tcn" with payload ""tcndata",I,"a"='1',"b"='2012-12-23'" received from server process with PID 22770.
Asynchronous notification "tcn" with payload ""tcndata",I,"a"='2',"b"='2012-12-23'" received from server process with PID 22770.
test=# update tcndata set c = 'uno' where a = 1;
UPDATE 2
Asynchronous notification "tcn" with payload ""tcndata",U,"a"='1',"b"='2012-12-22'" received from server process with PID 22770.
Asynchronous notification "tcn" with payload ""tcndata",U,"a"='1',"b"='2012-12-23'" received from server process with PID 22770.
test=# delete from tcndata where a = 1 and b = date '2012-12-22';
DELETE 1
Asynchronous notification "tcn" with payload ""tcndata",D,"a"='1',"b"='2012-12-22'" received from server process with PID 22770.
```
