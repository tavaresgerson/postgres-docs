## 42.6. Funções de disparo no PL/Tcl [#](#PLTCL-TRIGGER)

As funções de disparo podem ser escritas em PL/Tcl. O PostgreSQL exige que uma função que deve ser chamada como um disparo seja declarada como uma função sem argumentos e com um tipo de retorno de `trigger`.

As informações do gerenciador de gatilho são passadas para o corpo da função nas seguintes variáveis:

`$TG_name`: O nome do gatilho da declaração `CREATE TRIGGER`.

`$TG_relid`: O ID do objeto da tabela que causou a invocação da função de gatilho.

`$TG_table_name`: O nome da tabela que causou a invocação da função de gatilho.

`$TG_table_schema`: O esquema da tabela que causou a invocação da função de gatilho.

`$TG_relatts`: Uma lista Tcl dos nomes dos colunas da tabela, prefixada com um elemento de lista vazio. Portanto, ao procurar um nome de coluna na lista com o comando `lsearch` do Tcl, o número do elemento começa com 1 para a primeira coluna, da mesma maneira que as colunas são numeradas de forma convencional no PostgreSQL. (Elementos de lista vazios também aparecem nas posições das colunas que foram excluídas, para que a numeração dos atributos seja correta para as colunas à direita.)

`$TG_when`: A string `BEFORE`, `AFTER` ou `INSTEAD OF`, dependendo do tipo de evento desencadeador.

`$TG_level`: A string `ROW` ou `STATEMENT`, dependendo do tipo de evento desencadeador.

`$TG_op`: A cadeia `INSERT`, `UPDATE`, `DELETE` ou `TRUNCATE`, dependendo do tipo de evento desencadeador.

`$NEW`: Um array associativo contendo os valores da nova linha da tabela para as ações de `INSERT` ou `UPDATE`, ou vazio para `DELETE`. O array é indexado pelo nome da coluna. As colunas que são nulos não aparecerão no array. Isso não é definido para gatilhos de nível de declaração.

`$OLD`: Um array associativo contendo os valores da linha da tabela antiga para ações de `UPDATE` ou `DELETE`, ou vazio para `INSERT`. O array é indexado pelo nome da coluna. As colunas que são nulos não aparecerão no array. Isso não é definido para gatilhos de nível de declaração.

`$args`: Uma lista Tcl dos argumentos da função conforme fornecida na declaração `CREATE TRIGGER`. Esses argumentos também são acessíveis como `$1`... `$n` no corpo da função.

O valor de retorno de uma função de gatilho pode ser uma das strings `OK` ou `SKIP`, ou uma lista de pares de nome de coluna/valor. Se o valor de retorno for `OK`, a operação (`INSERT`/`UPDATE`/`DELETE`) que acionou o gatilho prosseguirá normalmente. `SKIP` indica ao gerente de gatilho que deve silenciar a operação para essa linha. Se for retornada uma lista, ela indica ao PL/Tcl que deve retornar uma linha modificada ao gerente de gatilho; o conteúdo da linha modificada é especificado pelos nomes e valores das colunas na lista. Quaisquer colunas não mencionadas na lista são definidas como nulos. Retornar uma linha modificada é significativo apenas para gatilhos de nível de linha `BEFORE` `INSERT` ou `UPDATE`, para os quais a linha modificada será inserida em vez daquela dada em `$NEW`; ou para gatilhos de nível de linha `INSTEAD OF` `INSERT` ou `UPDATE` onde a linha retornada é usada como dados de origem para as cláusulas `INSERT RETURNING` ou `UPDATE RETURNING`. Em gatilhos de nível de linha `BEFORE` `DELETE` ou `INSTEAD OF` `DELETE`, retornar uma linha modificada tem o mesmo efeito que retornar `OK`, ou seja, a operação prossegue. O valor de retorno do gatilho é ignorado para todos os outros tipos de gatilhos.

DICA

A lista de resultados pode ser feita a partir de uma representação de matriz do tuplo modificado com o comando Tcl `array get`.

Aqui está um exemplo de função de gatilho que força um valor inteiro em uma tabela a manter um registro do número de atualizações que são realizadas na linha. Para novas linhas inseridas, o valor é inicializado em 0 e, em seguida, incrementado em cada operação de atualização.

```
CREATE FUNCTION trigfunc_modcount() RETURNS trigger AS $$
    switch $TG_op {
        INSERT {
            set NEW($1) 0
        }
        UPDATE {
            set NEW($1) $OLD($1)
            incr NEW($1)
        }
        default {
            return OK
        }
    }
    return [array get NEW]
$$ LANGUAGE pltcl;

CREATE TABLE mytab (num integer, description text, modcnt integer);

CREATE TRIGGER trig_mytab_modcount BEFORE INSERT OR UPDATE ON mytab
    FOR EACH ROW EXECUTE FUNCTION trigfunc_modcount('modcnt');
```

Observe que a própria função de gatilho não conhece o nome da coluna; isso é fornecido pelos argumentos da função de gatilho. Isso permite que a função de gatilho seja reutilizada com diferentes tabelas.