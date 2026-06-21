## 41.10. Funções de disparo [#](#PLPGSQL-TRIGGER)

* [41.10.1. Descodificadores em Mudanças de Dados](plpgsql-trigger.md#PLPGSQL-DML-TRIGGER)
* [41.10.2. Descodificadores em Eventos](plpgsql-trigger.md#PLPGSQL-EVENT-TRIGGER)

O PL/pgSQL pode ser usado para definir funções de gatilho em mudanças de dados ou eventos de banco de dados. Uma função de gatilho é criada com o comando `CREATE FUNCTION`, declarando-a como uma função sem argumentos e com um tipo de retorno de `trigger` (para gatilhos de mudança de dados) ou `event_trigger` (para gatilhos de eventos de banco de dados). Variáveis locais especiais nomeadas `TG_something` são definidas automaticamente para descrever a condição que desencadeou a chamada.

### 41.10.1. Gatilhos em Mudanças de Dados [#](#PLPGSQL-DML-TRIGGER)

Um [elemento de mudança de dados][(triggers.md "Chapter 37. Triggers")] é declarado como uma função sem argumentos e com um tipo de retorno de `trigger`. Observe que a função deve ser declarada sem argumentos, mesmo que ela espere receber alguns argumentos especificados em `CREATE TRIGGER` — tais argumentos são passados via `TG_ARGV`, conforme descrito abaixo.

Quando uma função PL/pgSQL é chamada como um gatilho, várias variáveis especiais são criadas automaticamente no bloco de nível superior. Elas são:

`NEW` `record` [#](#PLPGSQL-DML-TRIGGER-NEW): nova linha de banco de dados para operações de `INSERT`/`UPDATE` em gatilhos de nível de linha. Esta variável é nula em gatilhos de nível de declaração e para operações de `DELETE`.

`OLD` `record` [#](#PLPGSQL-DML-TRIGGER-OLD): linha antiga do banco de dados para operações de `UPDATE`/`DELETE` em gatilhos de nível de linha. Esta variável é nula em gatilhos de nível de declaração e para operações de `INSERT`.

`TG_NAME` `name` [#](#PLPGSQL-DML-TRIGGER-TG-NAME): nome do gatilho que disparou.

`TG_WHEN` `text` [#](#PLPGSQL-DML-TRIGGER-TG-WHEN): `BEFORE`, `AFTER`, ou `INSTEAD OF`, dependendo da definição do gatilho.

`TG_LEVEL` `text` [#](#PLPGSQL-DML-TRIGGER-TG-LEVEL): `ROW` ou `STATEMENT`, dependendo da definição do gatilho.

`TG_OP` `text` [#](#PLPGSQL-DML-TRIGGER-TG-OP): operação para a qual o gatilho foi disparado: `INSERT`, `UPDATE`, `DELETE` ou `TRUNCATE`.

`TG_RELID` `oid` (referências [`pg_class`](catalog-pg-class.md "52.11. pg_class").`oid`) [#](#PLPGSQL-DML-TRIGGER-TG-RELID): ID do objeto da tabela que causou a invocação do gatilho.

`TG_RELNAME` `name` [#](#PLPGSQL-DML-TRIGGER-TG-RELNAME): tabela que causou a invocação do gatilho. Isso já está desatualizado e pode desaparecer em uma versão futura. Use `TG_TABLE_NAME` em vez disso.

`TG_TABLE_NAME` `name` [#](#PLPGSQL-DML-TRIGGER-TG-TABLE-NAME): tabela que causou a invocação do gatilho.

`TG_TABLE_SCHEMA` `name` [#](#PLPGSQL-DML-TRIGGER-TG-TABLE-SCHEMA): esquema da tabela que causou a invocação do gatilho.

`TG_NARGS` `integer` [#](#PLPGSQL-DML-TRIGGER-TG-NARGS): número de argumentos fornecidos à função de gatilho na declaração `CREATE TRIGGER`.

`TG_ARGV` `text[]` [#](#PLPGSQL-DML-TRIGGER-TG-ARGV): argumentos da declaração `CREATE TRIGGER`. O índice conta a partir de 0. Índices inválidos (menos de 0 ou igual ou maior que `tg_nargs`) resultam em um valor nulo.

Uma função de gatilho deve retornar ou `NULL` ou um valor de registro/linha com exatamente a estrutura da tabela para a qual o gatilho foi acionado.

Os gatilhos de nível de linha que retornam `BEFORE` podem retornar nulo para sinalizar ao gerente de gatilho que ignore o resto da operação para essa linha (ou seja, os gatilhos subsequentes não são acionados, e o `INSERT`/`UPDATE`/`DELETE` não ocorre para essa linha). Se um valor não nulo for retornado, então a operação prossegue com esse valor da linha. Retornar um valor de linha diferente do valor original de `NEW` altera a linha que será inserida ou atualizada. Assim, se a função de gatilho deseja que a ação de gatilho seja realizada normalmente sem alterar o valor da linha, `NEW` (ou um valor equivalente) deve ser retornado. Para alterar a linha que será armazenada, é possível substituir valores individuais diretamente em `NEW` e retornar o `NEW` modificado, ou construir um novo registro/linha completa para retornar. No caso de um antes do gatilho em `DELETE`, o valor retornado não tem efeito direto, mas deve ser nulo para permitir que a ação de gatilho prossiga. Note que `NEW` é nulo em gatilhos de `DELETE`, então retornar isso geralmente não é sensível. O idiom comum em gatilhos de `DELETE` é retornar `OLD`.

Os gatilhos `INSTEAD OF` (que são sempre gatilhos de nível de linha e podem ser usados apenas em visualizações) podem retornar nulo para sinalizar que não realizaram nenhuma atualização e que o restante da operação para essa linha deve ser ignorado (ou seja, os gatilhos subsequentes não são acionados e a linha não é contada no status de linhas afetadas para as `INSERT`/`UPDATE`/`DELETE` circundantes). Caso contrário, deve ser retornado um valor não nulo, para sinalizar que o gatilho realizou a operação solicitada. Para as operações `INSERT` e `UPDATE`, o valor de retorno deve ser `NEW`, que a função de gatilho pode modificar para suportar `INSERT RETURNING` e `UPDATE RETURNING` (isso também afetará o valor da linha passado para quaisquer gatilhos subsequentes, ou passado para uma referência especial de alias `EXCLUDED` dentro de uma declaração `INSERT` com uma cláusula `ON CONFLICT DO UPDATE`). Para operações `DELETE`, o valor de retorno deve ser `OLD`.

O valor de retorno de um gatilho de nível de linha disparado `AFTER` ou um gatilho de nível de declaração disparado `BEFORE` ou `AFTER` é sempre ignorado; ele pode ser nulo. No entanto, qualquer um desses tipos de gatilhos ainda pode abortar toda a operação ao levantar um erro.

[Exemplo 41.3][(plpgsql-trigger.md#PLPGSQL-TRIGGER-EXAMPLE "Example 41.3. A PL/pgSQL Trigger Function")] mostra um exemplo de uma função de gatilho no PL/pgSQL.

**Exemplo 41.3. Uma função de gatilho PL/pgSQL**

Este exemplo de gatilho garante que, sempre que uma linha é inserida ou atualizada na tabela, o nome atual do usuário e a hora são marcados na linha. E verifica que o nome de um funcionário é fornecido e que o salário é um valor positivo.

```
CREATE TABLE emp (
    empname           text,
    salary            integer,
    last_date         timestamp,
    last_user         text
);

CREATE FUNCTION emp_stamp() RETURNS trigger AS $emp_stamp$
    BEGIN
        -- Check that empname and salary are given
        IF NEW.empname IS NULL THEN
            RAISE EXCEPTION 'empname cannot be null';
        END IF;
        IF NEW.salary IS NULL THEN
            RAISE EXCEPTION '% cannot have null salary', NEW.empname;
        END IF;

        -- Who works for us when they must pay for it?
        IF NEW.salary < 0 THEN
            RAISE EXCEPTION '% cannot have a negative salary', NEW.empname;
        END IF;

        -- Remember who changed the payroll when
        NEW.last_date := current_timestamp;
        NEW.last_user := current_user;
        RETURN NEW;
    END;
$emp_stamp$ LANGUAGE plpgsql;

CREATE TRIGGER emp_stamp BEFORE INSERT OR UPDATE ON emp
    FOR EACH ROW EXECUTE FUNCTION emp_stamp();
```

  

Outra maneira de registrar as alterações em uma tabela é criar uma nova tabela que retém uma linha para cada inserção, atualização ou exclusão que ocorre. Essa abordagem pode ser considerada como auditoria de alterações em uma tabela. [Exemplo 41.4][(plpgsql-trigger.md#PLPGSQL-TRIGGER-AUDIT-EXAMPLE "Example 41.4. A PL/pgSQL Trigger Function for Auditing")] mostra um exemplo de uma função de gatilho de auditoria em PL/pgSQL.

**Exemplo 41.4. Uma função de gatilho PL/pgSQL para auditoria**

Este gatilho de exemplo garante que qualquer inserção, atualização ou exclusão de uma linha na tabela `emp` seja registrada (ou seja, auditada) na tabela `emp_audit`. O horário atual e o nome do usuário são impressos na linha, juntamente com o tipo de operação realizada nela.

```
CREATE TABLE emp (
    empname           text NOT NULL,
    salary            integer
);

CREATE TABLE emp_audit(
    operation         char(1)   NOT NULL,
    stamp             timestamp NOT NULL,
    userid            text      NOT NULL,
    empname           text      NOT NULL,
    salary            integer
);

CREATE OR REPLACE FUNCTION process_emp_audit() RETURNS TRIGGER AS $emp_audit$
    BEGIN
        --
        -- Create a row in emp_audit to reflect the operation performed on emp,
        -- making use of the special variable TG_OP to work out the operation.
        --
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO emp_audit SELECT 'D', now(), current_user, OLD.*;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO emp_audit SELECT 'U', now(), current_user, NEW.*;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO emp_audit SELECT 'I', now(), current_user, NEW.*;
        END IF;
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$emp_audit$ LANGUAGE plpgsql;

CREATE TRIGGER emp_audit
AFTER INSERT OR UPDATE OR DELETE ON emp
    FOR EACH ROW EXECUTE FUNCTION process_emp_audit();
```

  

Uma variação do exemplo anterior usa uma visão que une a tabela principal à tabela de auditoria, para mostrar quando cada entrada foi modificada pela última vez. Essa abordagem ainda registra o rastreamento completo do rastreamento de alterações na tabela, mas também apresenta uma visão simplificada do rastreamento, mostrando apenas o último timestamp modificado derivado do rastreamento de auditoria para cada entrada. [Exemplo 41.5][(plpgsql-trigger.md#PLPGSQL-VIEW-TRIGGER-AUDIT-EXAMPLE "Example 41.5. A PL/pgSQL View Trigger Function for Auditing")] mostra um exemplo de um gatilho de auditoria em uma visão em PL/pgSQL.

**Exemplo 41.5. Uma função de gatilho de visão PL/pgSQL para auditoria**

Este exemplo utiliza um gatilho na visualização para torná-la atualizável e garantir que qualquer inserção, atualização ou exclusão de uma linha na visualização seja registrada (ou seja, auditada) na tabela `emp_audit`. O horário atual e o nome do usuário são registrados, juntamente com o tipo de operação realizada, e a visualização exibe o horário da última modificação de cada linha.

```
CREATE TABLE emp (
    empname           text PRIMARY KEY,
    salary            integer
);

CREATE TABLE emp_audit(
    operation         char(1)   NOT NULL,
    userid            text      NOT NULL,
    empname           text      NOT NULL,
    salary            integer,
    stamp             timestamp NOT NULL
);

CREATE VIEW emp_view AS
    SELECT e.empname,
           e.salary,
           max(ea.stamp) AS last_updated
      FROM emp e
      LEFT JOIN emp_audit ea ON ea.empname = e.empname
     GROUP BY 1, 2;

CREATE OR REPLACE FUNCTION update_emp_view() RETURNS TRIGGER AS $$
    BEGIN
        --
        -- Perform the required operation on emp, and create a row in emp_audit
        -- to reflect the change made to emp.
        --
        IF (TG_OP = 'DELETE') THEN
            DELETE FROM emp WHERE empname = OLD.empname;
            IF NOT FOUND THEN RETURN NULL; END IF;

            OLD.last_updated = now();
            INSERT INTO emp_audit VALUES('D', current_user, OLD.*);
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            UPDATE emp SET salary = NEW.salary WHERE empname = OLD.empname;
            IF NOT FOUND THEN RETURN NULL; END IF;

            NEW.last_updated = now();
            INSERT INTO emp_audit VALUES('U', current_user, NEW.*);
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO emp VALUES(NEW.empname, NEW.salary);

            NEW.last_updated = now();
            INSERT INTO emp_audit VALUES('I', current_user, NEW.*);
            RETURN NEW;
        END IF;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER emp_audit
INSTEAD OF INSERT OR UPDATE OR DELETE ON emp_view
    FOR EACH ROW EXECUTE FUNCTION update_emp_view();
```

  

Uma utilização dos gatilhos é manter uma tabela resumida de outra tabela. O resumo resultante pode ser usado no lugar da tabela original para certas consultas — muitas vezes com tempos de execução muito reduzidos. Essa técnica é comumente usada em Data Warehousing, onde as tabelas de dados medidos ou observados (chamadas de tabelas de fato) podem ser extremamente grandes. [Exemplo 41.6][(plpgsql-trigger.md#PLPGSQL-TRIGGER-SUMMARY-EXAMPLE "Example 41.6. A PL/pgSQL Trigger Function for Maintaining a Summary Table")] mostra um exemplo de uma função de gatilho em PL/pgSQL que mantém uma tabela resumida para uma tabela de fato em um data warehouse.

**Exemplo 41.6. Uma função de gatilho PL/pgSQL para manutenção de uma tabela de resumo**

O esquema detalhado aqui é, em parte, baseado no exemplo de *Loja de supermercado* do *The Data Warehouse Toolkit* de Ralph Kimball.

```
--
-- Main tables - time dimension and sales fact.
--
CREATE TABLE time_dimension (
    time_key                    integer NOT NULL,
    day_of_week                 integer NOT NULL,
    day_of_month                integer NOT NULL,
    month                       integer NOT NULL,
    quarter                     integer NOT NULL,
    year                        integer NOT NULL
);
CREATE UNIQUE INDEX time_dimension_key ON time_dimension(time_key);

CREATE TABLE sales_fact (
    time_key                    integer NOT NULL,
    product_key                 integer NOT NULL,
    store_key                   integer NOT NULL,
    amount_sold                 numeric(12,2) NOT NULL,
    units_sold                  integer NOT NULL,
    amount_cost                 numeric(12,2) NOT NULL
);
CREATE INDEX sales_fact_time ON sales_fact(time_key);

--
-- Summary table - sales by time.
--
CREATE TABLE sales_summary_bytime (
    time_key                    integer NOT NULL,
    amount_sold                 numeric(15,2) NOT NULL,
    units_sold                  numeric(12) NOT NULL,
    amount_cost                 numeric(15,2) NOT NULL
);
CREATE UNIQUE INDEX sales_summary_bytime_key ON sales_summary_bytime(time_key);

--
-- Function and trigger to amend summarized column(s) on UPDATE, INSERT, DELETE.
--
CREATE OR REPLACE FUNCTION maint_sales_summary_bytime() RETURNS TRIGGER
AS $maint_sales_summary_bytime$
    DECLARE
        delta_time_key          integer;
        delta_amount_sold       numeric(15,2);
        delta_units_sold        numeric(12);
        delta_amount_cost       numeric(15,2);
    BEGIN

        -- Work out the increment/decrement amount(s).
        IF (TG_OP = 'DELETE') THEN

            delta_time_key = OLD.time_key;
            delta_amount_sold = -1 * OLD.amount_sold;
            delta_units_sold = -1 * OLD.units_sold;
            delta_amount_cost = -1 * OLD.amount_cost;

        ELSIF (TG_OP = 'UPDATE') THEN

            -- forbid updates that change the time_key -
            -- (probably not too onerous, as DELETE + INSERT is how most
            -- changes will be made).
            IF ( OLD.time_key != NEW.time_key) THEN
                RAISE EXCEPTION 'Update of time_key : % -> % not allowed',
                                                      OLD.time_key, NEW.time_key;
            END IF;

            delta_time_key = OLD.time_key;
            delta_amount_sold = NEW.amount_sold - OLD.amount_sold;
            delta_units_sold = NEW.units_sold - OLD.units_sold;
            delta_amount_cost = NEW.amount_cost - OLD.amount_cost;

        ELSIF (TG_OP = 'INSERT') THEN

            delta_time_key = NEW.time_key;
            delta_amount_sold = NEW.amount_sold;
            delta_units_sold = NEW.units_sold;
            delta_amount_cost = NEW.amount_cost;

        END IF;


        -- Insert or update the summary row with the new values.
        <<insert_update>>
        LOOP
            UPDATE sales_summary_bytime
                SET amount_sold = amount_sold + delta_amount_sold,
                    units_sold = units_sold + delta_units_sold,
                    amount_cost = amount_cost + delta_amount_cost
                WHERE time_key = delta_time_key;

            EXIT insert_update WHEN found;

            BEGIN
                INSERT INTO sales_summary_bytime (
                            time_key,
                            amount_sold,
                            units_sold,
                            amount_cost)
                    VALUES (
                            delta_time_key,
                            delta_amount_sold,
                            delta_units_sold,
                            delta_amount_cost
                           );

                EXIT insert_update;

            EXCEPTION
                WHEN UNIQUE_VIOLATION THEN
                    -- do nothing
            END;
        END LOOP insert_update;

        RETURN NULL;

    END;
$maint_sales_summary_bytime$ LANGUAGE plpgsql;

CREATE TRIGGER maint_sales_summary_bytime
AFTER INSERT OR UPDATE OR DELETE ON sales_fact
    FOR EACH ROW EXECUTE FUNCTION maint_sales_summary_bytime();

INSERT INTO sales_fact VALUES(1,1,1,10,3,15);
INSERT INTO sales_fact VALUES(1,2,1,20,5,35);
INSERT INTO sales_fact VALUES(2,2,1,40,15,135);
INSERT INTO sales_fact VALUES(2,3,1,10,1,13);
SELECT * FROM sales_summary_bytime;
DELETE FROM sales_fact WHERE product_key = 1;
SELECT * FROM sales_summary_bytime;
UPDATE sales_fact SET units_sold = units_sold * 2;
SELECT * FROM sales_summary_bytime;
```

  

Os gatilhos `AFTER` também podem utilizar *tabelas de transição* para inspecionar todo o conjunto de linhas alteradas pela declaração de gatilho. O comando `CREATE TRIGGER` atribui nomes a uma ou ambas as tabelas de transição, e, em seguida, a função pode referir-se a esses nomes como se fossem tabelas temporárias somente de leitura. [Exemplo 41.7](plpgsql-trigger.md#PLPGSQL-TRIGGER-AUDIT-TRANSITION-EXAMPLE "Example 41.7. Auditing with Transition Tables") mostra um exemplo.

**Exemplo 41.7. Auditoria com tabelas de transição**

Este exemplo produz os mesmos resultados que o [Exemplo 41.4][(plpgsql-trigger.md#PLPGSQL-TRIGGER-AUDIT-EXAMPLE "Example 41.4. A PL/pgSQL Trigger Function for Auditing")], mas, em vez de usar um gatilho que dispara para cada linha, ele usa um gatilho que dispara uma vez por declaração, após coletar as informações relevantes em uma tabela de transição. Isso pode ser significativamente mais rápido do que a abordagem de gatilho de linha quando a declaração que está invocando modificou muitas linhas. Observe que devemos fazer uma declaração de gatilho separada para cada tipo de evento, pois as cláusulas `REFERENCING` devem ser diferentes para cada caso. Mas isso não nos impede de usar uma única função de gatilho se escolhermos. (Na prática, pode ser melhor usar três funções separadas e evitar os testes de execução em `TG_OP`).

```
CREATE TABLE emp (
    empname           text NOT NULL,
    salary            integer
);

CREATE TABLE emp_audit(
    operation         char(1)   NOT NULL,
    stamp             timestamp NOT NULL,
    userid            text      NOT NULL,
    empname           text      NOT NULL,
    salary            integer
);

CREATE OR REPLACE FUNCTION process_emp_audit() RETURNS TRIGGER AS $emp_audit$
    BEGIN
        --
        -- Create rows in emp_audit to reflect the operations performed on emp,
        -- making use of the special variable TG_OP to work out the operation.
        --
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO emp_audit
                SELECT 'D', now(), current_user, o.* FROM old_table o;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO emp_audit
                SELECT 'U', now(), current_user, n.* FROM new_table n;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO emp_audit
                SELECT 'I', now(), current_user, n.* FROM new_table n;
        END IF;
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$emp_audit$ LANGUAGE plpgsql;

CREATE TRIGGER emp_audit_ins
    AFTER INSERT ON emp
    REFERENCING NEW TABLE AS new_table
    FOR EACH STATEMENT EXECUTE FUNCTION process_emp_audit();
CREATE TRIGGER emp_audit_upd
    AFTER UPDATE ON emp
    REFERENCING OLD TABLE AS old_table NEW TABLE AS new_table
    FOR EACH STATEMENT EXECUTE FUNCTION process_emp_audit();
CREATE TRIGGER emp_audit_del
    AFTER DELETE ON emp
    REFERENCING OLD TABLE AS old_table
    FOR EACH STATEMENT EXECUTE FUNCTION process_emp_audit();
```

### 41.10.2. Gatilhos em Eventos [#](#PLPGSQL-EVENT-TRIGGER)

O PL/pgSQL pode ser usado para definir [eventos de gatilho][(event-triggers.md "Chapter 38. Event Triggers")]. O PostgreSQL exige que uma função que deve ser chamada como um gatilho de evento seja declarada como uma função sem argumentos e com um tipo de retorno de `event_trigger`.

Quando uma função PL/pgSQL é chamada como um gatilho de evento, várias variáveis especiais são criadas automaticamente no bloco de nível superior. Elas são:

`TG_EVENT` `text` [#](#PLPGSQL-EVENT-TRIGGER-TG-EVENT): o evento que é disparado.

`TG_TAG` `text` [#](#PLPGSQL-EVENT-TRIGGER-TG-TAG): etiqueta de comando para a qual o gatilho é disparado.

[Exemplo 41.8][(plpgsql-trigger.md#PLPGSQL-EVENT-TRIGGER-EXAMPLE "Example 41.8. A PL/pgSQL Event Trigger Function")] mostra um exemplo de uma função de gatilho de evento no PL/pgSQL.

**Exemplo 41.8. Uma função de gatilho de evento PL/pgSQL**

Este exemplo de gatilho simplesmente gera uma mensagem `NOTICE` toda vez que um comando compatível é executado.

```
CREATE OR REPLACE FUNCTION snitch() RETURNS event_trigger AS $$
BEGIN
    RAISE NOTICE 'snitch: % %', tg_event, tg_tag;
END;
$$ LANGUAGE plpgsql;

CREATE EVENT TRIGGER snitch ON ddl_command_start EXECUTE FUNCTION snitch();
```
