## 43.6. Gatilhos PL/Perl [#](#PLPERL-TRIGGERS)

O PL/Perl pode ser usado para escrever funções de gatilho. Em uma função de gatilho, a referência de hash `$_TD` contém informações sobre o evento de gatilho atual. `$_TD` é uma variável global, que recebe um valor local separado para cada invocação do gatilho. Os campos da referência de hash `$_TD` são:

`$_TD->{new}{foo}`: valor da coluna `NEW` do valor `foo`

`$_TD->{old}{foo}`: valor da coluna `OLD` do campo `foo`

`$_TD->{name}`: Nome do gatilho sendo chamado

`$_TD->{event}`: Evento desencadeante: `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE` ou `UNKNOWN`

`$_TD->{when}`: Quando o gatilho foi acionado: `BEFORE`, `AFTER`, `INSTEAD OF` ou `UNKNOWN`

`$_TD->{level}`: O nível de disparo: `ROW`, `STATEMENT` ou `UNKNOWN`

`$_TD->{relid}`: OID da tabela na qual o gatilho foi disparado

`$_TD->{table_name}`: Nome da tabela na qual o gatilho foi disparado

`$_TD->{relname}`: Nome da tabela na qual o gatilho foi disparado. Isso foi descontinuado e pode ser removido em uma versão futura. Por favor, use $_TD->{table_name} em vez disso.

`$_TD->{table_schema}`: Nome do esquema no qual a tabela em que o gatilho foi disparado está

`$_TD->{argc}`: Número de argumentos da função de gatilho

`@{$_TD->{args}}`: Argumentos da função de disparo. Não existe se `$_TD->{argc}` é 0.

Os gatilhos de nível de linha podem retornar um dos seguintes:

`return;`: Execute a operação

`"SKIP"`: Não execute a operação

`"MODIFY"`: Indica que a linha `NEW` foi modificada pela função de gatilho

Aqui está um exemplo de uma função de gatilho, que ilustra alguns dos pontos acima:

```
CREATE TABLE test (
    i int,
    v varchar
);

CREATE OR REPLACE FUNCTION valid_id() RETURNS trigger AS $$
    if (($_TD->{new}{i} >= 100) || ($_TD->{new}{i} <= 0)) {
        return "SKIP";    # skip INSERT/UPDATE command
    } elsif ($_TD->{new}{v} ne "immortal") {
        $_TD->{new}{v} .= "(modified by trigger)";
        return "MODIFY";  # modify row and execute INSERT/UPDATE command
    } else {
        return;           # execute INSERT/UPDATE command
    }
$$ LANGUAGE plperl;

CREATE TRIGGER test_valid_id_trig
    BEFORE INSERT OR UPDATE ON test
    FOR EACH ROW EXECUTE FUNCTION valid_id();
```
