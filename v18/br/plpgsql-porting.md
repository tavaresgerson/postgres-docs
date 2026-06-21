## 41.13. Portando de Oracle PL/SQL [#](#PLPGSQL-PORTING)

* [41.13.1. Exemplos de Portando][(plpgsql-porting.md#PLPGSQL-PORTING-EXAMPLES)
* [41.13.2. Outras Coisas a Observar][(plpgsql-porting.md#PLPGSQL-PORTING-OTHER)
* [41.13.3. Apêndice][(plpgsql-porting.md#PLPGSQL-PORTING-APPENDIX)

Esta seção explica as diferenças entre o PL/pgSQL do PostgreSQL e o PL/SQL do Oracle, para ajudar os desenvolvedores que transportam aplicativos do Oracle® para o PostgreSQL.

O PL/pgSQL é semelhante ao PL/SQL em muitos aspectos. É uma linguagem estruturada em blocos, imperativa, e todas as variáveis devem ser declaradas. As atribuições, os loops e os condicionais são semelhantes. As principais diferenças que você deve manter em mente ao migrar do PL/SQL para o PL/pgSQL são:

* Se um nome usado em um comando SQL puder ser tanto o nome de uma coluna de uma tabela usada no comando quanto uma referência a uma variável da função, o PL/SQL o trata como o nome de uma coluna. Por padrão, o PL/pgSQL lançará um erro que reclama que o nome é ambíguo. Você pode especificar `plpgsql.variable_conflict` = `use_column` para mudar esse comportamento para corresponder ao PL/SQL, conforme explicado em [Seção 41.11.1](plpgsql-implementation.md#PLPGSQL-VAR-SUBST "41.11.1. Variable Substitution"). É frequentemente melhor evitar tais ambiguidades no primeiro lugar, mas se você precisa portar uma grande quantidade de código que depende desse comportamento, definir `variable_conflict` pode ser a melhor solução.
* No PostgreSQL, o corpo da função deve ser escrito como uma literal de string. Portanto, você precisa usar citação de dólar ou escapar de aspas simples no corpo da função. (Veja [Seção 41.12.1](plpgsql-development-tips.md#PLPGSQL-QUOTE-TIPS "41.12.1. Handling of Quotation Marks")).
* Os nomes dos tipos de dados muitas vezes precisam de tradução. Por exemplo, nos valores de string do Oracle são comumente declarados como sendo do tipo `varchar2`, que é um tipo não padrão do SQL. No PostgreSQL, use o tipo `varchar` ou `text`. Da mesma forma, substitua o tipo `number` com `numeric`, ou use algum outro tipo de dados numérico se houver um mais apropriado.
* Em vez de pacotes, use esquemas para organizar suas funções em grupos.
* Como não há pacotes, também não há variáveis em nível de pacote. Isso é um pouco irritante. Você pode manter o estado por sessão em tabelas temporárias.
* Loops de inteiros `FOR` com `REVERSE` funcionam de maneira diferente: o PL/SQL conta de volta do segundo número para o primeiro, enquanto o PL/pgSQL conta de volta do primeiro número para o segundo, exigindo que os limites do loop sejam trocados ao portar. Essa incompatibilidade é infeliz, mas é improvável que seja alterada. (Veja [Seção 41.6.5.5](plpgsql-control-structures.md#PLPGSQL-INTEGER-FOR "41.6.5.5. FOR (Integer Variant)).
* Loops de `FOR` sobre consultas (além de cursors) também funcionam de maneira diferente: a(s) variável(eis) alvo(s) deve(m) ter sido declarada(s), enquanto o PL/SQL sempre as declara implicitamente. Uma vantagem disso é que os valores das variáveis ainda são acessíveis após a saída do loop.
* Há várias diferenças de notação para o uso de variáveis de cursor.

### 41.13.1. Exemplos de portação [#](#PLPGSQL-PORTING-EXAMPLES)

[Exemplo 41.9][(plpgsql-porting.md#PGSQL-PORTING-EX1 "Example 41.9. Porting a Simple Function from PL/SQL to PL/pgSQL")] mostra como portar uma função simples do PL/SQL para o PL/pgSQL.

**Exemplo 41.9. Portando uma função simples de PL/SQL para PL/pgSQL**

Aqui está uma função Oracle PL/SQL:

```
CREATE OR REPLACE FUNCTION cs_fmt_browser_version(v_name varchar2,
                                                  v_version varchar2)
RETURN varchar2 IS
BEGIN
    IF v_version IS NULL THEN
        RETURN v_name;
    END IF;
    RETURN v_name || '/' || v_version;
END;
/
show errors;
```

Vamos analisar essa função e ver as diferenças em comparação com PL/pgSQL:

* O nome do tipo `varchar2` precisa ser alterado para `varchar` ou `text`. Nos exemplos desta seção, usaremos `varchar`, mas `text` é frequentemente uma escolha melhor se você não precisar de limites específicos de comprimento de string.
* A palavra-chave `RETURN` no protótipo da função (não no corpo da função) se torna `RETURNS` no PostgreSQL. Além disso, `IS` se torna `AS`, e você precisa adicionar uma cláusula `LANGUAGE` porque o PL/pgSQL não é o único idioma de função possível.
* No PostgreSQL, o corpo da função é considerado um literal de string, então você precisa usar aspas ou dólares ao seu redor. Isso substitui o `/` finalizado na abordagem Oracle.
* O comando `show errors` não existe no PostgreSQL e não é necessário, uma vez que os erros são relatados automaticamente.

É assim que essa função seria quando transportada para o PostgreSQL:

```
CREATE OR REPLACE FUNCTION cs_fmt_browser_version(v_name varchar,
                                                  v_version varchar)
RETURNS varchar AS $$
BEGIN
    IF v_version IS NULL THEN
        RETURN v_name;
    END IF;
    RETURN v_name || '/' || v_version;
END;
$$ LANGUAGE plpgsql;
```

  

[Exemplo 41.10][(plpgsql-porting.md#PLPGSQL-PORTING-EX2 "Example 41.10. Porting a Function that Creates Another Function from PL/SQL to PL/pgSQL")] mostra como portar uma função que cria outra função e como lidar com os problemas de citação que surgem.

**Exemplo 41.10. Portando uma função que cria outra função a partir de PL/SQL para PL/pgSQL**

O procedimento a seguir extrai linhas de uma declaração `SELECT` e constrói uma grande função com os resultados em declarações `IF`, por questões de eficiência.

Esta é a versão Oracle:

```
CREATE OR REPLACE PROCEDURE cs_update_referrer_type_proc IS
    CURSOR referrer_keys IS
        SELECT * FROM cs_referrer_keys
        ORDER BY try_order;
    func_cmd VARCHAR(4000);
BEGIN
    func_cmd := 'CREATE OR REPLACE FUNCTION cs_find_referrer_type(v_host IN VARCHAR2,
                 v_domain IN VARCHAR2, v_url IN VARCHAR2) RETURN VARCHAR2 IS BEGIN';

    FOR referrer_key IN referrer_keys LOOP
        func_cmd := func_cmd ||
          ' IF v_' || referrer_key.kind
          || ' LIKE ''' || referrer_key.key_string
          || ''' THEN RETURN ''' || referrer_key.referrer_type
          || '''; END IF;';
    END LOOP;

    func_cmd := func_cmd || ' RETURN NULL; END;';

    EXECUTE IMMEDIATE func_cmd;
END;
/
show errors;
```

Veja como essa função acabaria no PostgreSQL:

```
CREATE OR REPLACE PROCEDURE cs_update_referrer_type_proc() AS $func$
DECLARE
    referrer_keys CURSOR IS
        SELECT * FROM cs_referrer_keys
        ORDER BY try_order;
    func_body text;
    func_cmd text;
BEGIN
    func_body := 'BEGIN';

    FOR referrer_key IN referrer_keys LOOP
        func_body := func_body ||
          ' IF v_' || referrer_key.kind
          || ' LIKE ' || quote_literal(referrer_key.key_string)
          || ' THEN RETURN ' || quote_literal(referrer_key.referrer_type)
          || '; END IF;' ;
    END LOOP;

    func_body := func_body || ' RETURN NULL; END;';

    func_cmd :=
      'CREATE OR REPLACE FUNCTION cs_find_referrer_type(v_host varchar,
                                                        v_domain varchar,
                                                        v_url varchar)
        RETURNS varchar AS '
      || quote_literal(func_body)
      || ' LANGUAGE plpgsql;' ;

    EXECUTE func_cmd;
END;
$func$ LANGUAGE plpgsql;
```

Observe como o corpo da função é construído separadamente e passado por `quote_literal` para duplicar quaisquer aspas nele. Essa técnica é necessária porque não podemos usar com segurança a citação em dólar para definir a nova função: não sabemos com certeza quais strings serão interpoladas do campo `referrer_key.key_string`. (Estamos assumindo aqui que `referrer_key.kind` pode ser confiável para sempre ser `host`, `domain` ou `url`, mas `referrer_key.key_string` pode ser qualquer coisa, em particular, pode conter sinais de dólar.) Esta função é, na verdade, uma melhoria em relação ao original da Oracle, porque não gerará código quebrado quando `referrer_key.key_string` ou `referrer_key.referrer_type` contêm aspas.

  

[Exemplo 41.11][(plpgsql-porting.md#PLPGSQL-PORTING-EX3 "Example 41.11. Porting a Procedure With String Manipulation and OUT Parameters from PL/SQL to PL/pgSQL")] mostra como portar uma função com parâmetros `OUT` e manipulação de strings. O PostgreSQL não tem uma função embutida `instr`, mas você pode criar uma usando uma combinação de outras funções. Na [Seção 41.13.3][(plpgsql-porting.md#PLPGSQL-PORTING-APPENDIX "41.13.3. Appendix")] há uma implementação PL/pgSQL de `instr` que você pode usar para facilitar sua portar.

**Exemplo 41.11. Portagem de um procedimento com manipulação de strings e parâmetros `OUT` de PL/SQL para PL/pgSQL**

O seguinte procedimento Oracle PL/SQL é usado para analisar uma URL e retornar vários elementos (host, caminho e consulta).

Esta é a versão Oracle:

```
CREATE OR REPLACE PROCEDURE cs_parse_url(
    v_url IN VARCHAR2,
    v_host OUT VARCHAR2,  -- This will be passed back
    v_path OUT VARCHAR2,  -- This one too
    v_query OUT VARCHAR2) -- And this one
IS
    a_pos1 INTEGER;
    a_pos2 INTEGER;
BEGIN
    v_host := NULL;
    v_path := NULL;
    v_query := NULL;
    a_pos1 := instr(v_url, '//');

    IF a_pos1 = 0 THEN
        RETURN;
    END IF;
    a_pos2 := instr(v_url, '/', a_pos1 + 2);
    IF a_pos2 = 0 THEN
        v_host := substr(v_url, a_pos1 + 2);
        v_path := '/';
        RETURN;
    END IF;

    v_host := substr(v_url, a_pos1 + 2, a_pos2 - a_pos1 - 2);
    a_pos1 := instr(v_url, '?', a_pos2 + 1);

    IF a_pos1 = 0 THEN
        v_path := substr(v_url, a_pos2);
        RETURN;
    END IF;

    v_path := substr(v_url, a_pos2, a_pos1 - a_pos2);
    v_query := substr(v_url, a_pos1 + 1);
END;
/
show errors;
```

Aqui está uma possível tradução para PL/pgSQL:

```
CREATE OR REPLACE FUNCTION cs_parse_url(
    v_url IN VARCHAR,
    v_host OUT VARCHAR,  -- This will be passed back
    v_path OUT VARCHAR,  -- This one too
    v_query OUT VARCHAR) -- And this one
AS $$
DECLARE
    a_pos1 INTEGER;
    a_pos2 INTEGER;
BEGIN
    v_host := NULL;
    v_path := NULL;
    v_query := NULL;
    a_pos1 := instr(v_url, '//');

    IF a_pos1 = 0 THEN
        RETURN;
    END IF;
    a_pos2 := instr(v_url, '/', a_pos1 + 2);
    IF a_pos2 = 0 THEN
        v_host := substr(v_url, a_pos1 + 2);
        v_path := '/';
        RETURN;
    END IF;

    v_host := substr(v_url, a_pos1 + 2, a_pos2 - a_pos1 - 2);
    a_pos1 := instr(v_url, '?', a_pos2 + 1);

    IF a_pos1 = 0 THEN
        v_path := substr(v_url, a_pos2);
        RETURN;
    END IF;

    v_path := substr(v_url, a_pos2, a_pos1 - a_pos2);
    v_query := substr(v_url, a_pos1 + 1);
END;
$$ LANGUAGE plpgsql;
```

Essa função pode ser usada da seguinte forma:

```
SELECT * FROM cs_parse_url('http://foobar.com/query.cgi?baz');
```

  

[Exemplo 41.12][(plpgsql-porting.md#PLPGSQL-PORTING-EX4 "Example 41.12. Porting a Procedure from PL/SQL to PL/pgSQL")] mostra como portar um procedimento que utiliza várias características específicas da Oracle.

**Exemplo 41.12. Portando um procedimento de PL/SQL para PL/pgSQL**

A versão do Oracle:

```
CREATE OR REPLACE PROCEDURE cs_create_job(v_job_id IN INTEGER) IS
    a_running_job_count INTEGER;
BEGIN
    LOCK TABLE cs_jobs IN EXCLUSIVE MODE;

    SELECT count(*) INTO a_running_job_count FROM cs_jobs WHERE end_stamp IS NULL;

    IF a_running_job_count > 0 THEN
        COMMIT; -- free lock
        raise_application_error(-20000,
                 'Unable to create a new job: a job is currently running.');
    END IF;

    DELETE FROM cs_active_job;
    INSERT INTO cs_active_job(job_id) VALUES (v_job_id);

    BEGIN
        INSERT INTO cs_jobs (job_id, start_stamp) VALUES (v_job_id, now());
    EXCEPTION
        WHEN dup_val_on_index THEN NULL; -- don't worry if it already exists
    END;
    COMMIT;
END;
/
show errors
```

É assim que poderíamos portar esse procedimento para PL/pgSQL:

```
CREATE OR REPLACE PROCEDURE cs_create_job(v_job_id integer) AS $$
DECLARE
    a_running_job_count integer;
BEGIN
    LOCK TABLE cs_jobs IN EXCLUSIVE MODE;

    SELECT count(*) INTO a_running_job_count FROM cs_jobs WHERE end_stamp IS NULL;

    IF a_running_job_count > 0 THEN
        COMMIT; -- free lock
        RAISE EXCEPTION 'Unable to create a new job: a job is currently running'; -- (1)
    END IF;

    DELETE FROM cs_active_job;
    INSERT INTO cs_active_job(job_id) VALUES (v_job_id);

    BEGIN
        INSERT INTO cs_jobs (job_id, start_stamp) VALUES (v_job_id, now());
    EXCEPTION
        WHEN unique_violation THEN -- (2)
            -- don't worry if it already exists
    END;
    COMMIT;
END;
$$ LANGUAGE plpgsql;
```



<table border="0" summary="Callout list">
<tr>
<td align="left" valign="top" width="5%">
<p>
<a href="#co.plpgsql-porting-raise">
     (1)
    </a>
</p>
</td>
<td align="left" valign="top">
<p>
    The syntax of
    <code class="literal">
     RAISE
    </code>
    is considerably different from Oracle's statement, although the basic case
    <code class="literal">
     RAISE
    </code>
<em class="replaceable">
<code>
      exception_name
     </code>
</em>
    works
       similarly.
   </p>
</td>
</tr>
<tr>
<td align="left" valign="top" width="5%">
<p>
<a href="#co.plpgsql-porting-exception">
     (2)
    </a>
</p>
</td>
<td align="left" valign="top">
<p>
    The exception names supported by
    <span class="application">
     PL/pgSQL
    </span>
    are different from Oracle's.  The set of built-in exception names is much larger (see
    <a class="xref" href="errcodes-appendix.md" title="Appendix A. PostgreSQL Error Codes">
     Appendix A
    </a>
    ).  There is not currently a way to declare user-defined exception names, although you can throw user-chosen SQLSTATE values instead.
   </p>
</td>
</tr>
</table>



### 41.13.2. Outras coisas a observar [#](#PLPGSQL-PORTING-OTHER)

Esta seção explica algumas outras coisas a serem observadas ao migrar funções Oracle PL/SQL para PostgreSQL.

#### 41.13.2.1. Retorno implícito após exceções [#](#PLPGSQL-PORTING-EXCEPTIONS)

Em PL/pgSQL, quando uma exceção é capturada por uma cláusula `EXCEPTION`, todas as alterações no banco de dados desde o `BEGIN` do bloco são automaticamente revertidas. Ou seja, o comportamento é equivalente ao que você obteria no Oracle com:

```
BEGIN
    SAVEPOINT s1;
    ... code here ...
EXCEPTION
    WHEN ... THEN
        ROLLBACK TO s1;
        ... code here ...
    WHEN ... THEN
        ROLLBACK TO s1;
        ... code here ...
END;
```

Se você está traduzindo um procedimento Oracle que usa `SAVEPOINT` e `ROLLBACK TO` neste estilo, sua tarefa é fácil: basta omitir o `SAVEPOINT` e `ROLLBACK TO`. Se você tem um procedimento que usa `SAVEPOINT` e `ROLLBACK TO` de uma maneira diferente, então será necessário algum pensamento real.

#### 41.13.2.2. `EXECUTE` [#](#PLPGSQL-PORTING-OTHER-EXECUTE)

A versão PL/pgSQL do `EXECUTE` funciona de maneira semelhante à versão PL/SQL, mas você deve lembrar-se de usar `quote_literal` e `quote_ident` conforme descrito em [Seção 41.5.4](plpgsql-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN "41.5.4. Executing Dynamic Commands"). Os construtos do tipo `EXECUTE 'SELECT * FROM $1';` não funcionarão de forma confiável, a menos que você use essas funções.

#### 41.13.2.3. Otimizando funções PL/pgSQL [#](#PLPGSQL-PORTING-OPTIMIZATION)

O PostgreSQL oferece dois modificadores de criação de função para otimizar a execução: “volatilidade” (se a função sempre retorna o mesmo resultado quando recebe os mesmos argumentos) e “strictness” (se a função retorna null se qualquer argumento for nulo). Consulte a página de referência [CREATE FUNCTION][(sql-createfunction.md "CREATE FUNCTION")] para obter detalhes.

Ao utilizar esses atributos de otimização, sua declaração `CREATE FUNCTION` pode parecer algo assim:

```
CREATE FUNCTION foo(...) RETURNS integer AS $$
...
$$ LANGUAGE plpgsql STRICT IMMUTABLE;
```

### 41.13.3. Anexo [#](#PLPGSQL-PORTING-APPENDIX)

Esta seção contém o código para um conjunto de funções `instr` compatíveis com o Oracle que você pode usar para simplificar seus esforços de porting.

```
--
-- instr functions that mimic Oracle's counterpart
-- Syntax: instr(string1, string2 [, n [, m]])
-- where [] denotes optional parameters.
--
-- Search string1, beginning at the nth character, for the mth occurrence
-- of string2.  If n is negative, search backwards, starting at the abs(n)'th
-- character from the end of string1.
-- If n is not passed, assume 1 (search starts at first character).
-- If m is not passed, assume 1 (find first occurrence).
-- Returns starting index of string2 in string1, or 0 if string2 is not found.
--

CREATE FUNCTION instr(varchar, varchar) RETURNS integer AS $$
BEGIN
    RETURN instr($1, $2, 1);
END;
$$ LANGUAGE plpgsql STRICT IMMUTABLE;


CREATE FUNCTION instr(string varchar, string_to_search_for varchar,
                      beg_index integer)
RETURNS integer AS $$
DECLARE
    pos integer NOT NULL DEFAULT 0;
    temp_str varchar;
    beg integer;
    length integer;
    ss_length integer;
BEGIN
    IF beg_index > 0 THEN
        temp_str := substring(string FROM beg_index);
        pos := position(string_to_search_for IN temp_str);

        IF pos = 0 THEN
            RETURN 0;
        ELSE
            RETURN pos + beg_index - 1;
        END IF;
    ELSIF beg_index < 0 THEN
        ss_length := char_length(string_to_search_for);
        length := char_length(string);
        beg := length + 1 + beg_index;

        WHILE beg > 0 LOOP
            temp_str := substring(string FROM beg FOR ss_length);
            IF string_to_search_for = temp_str THEN
                RETURN beg;
            END IF;

            beg := beg - 1;
        END LOOP;

        RETURN 0;
    ELSE
        RETURN 0;
    END IF;
END;
$$ LANGUAGE plpgsql STRICT IMMUTABLE;


CREATE FUNCTION instr(string varchar, string_to_search_for varchar,
                      beg_index integer, occur_index integer)
RETURNS integer AS $$
DECLARE
    pos integer NOT NULL DEFAULT 0;
    occur_number integer NOT NULL DEFAULT 0;
    temp_str varchar;
    beg integer;
    i integer;
    length integer;
    ss_length integer;
BEGIN
    IF occur_index <= 0 THEN
        RAISE 'argument ''%'' is out of range', occur_index
          USING ERRCODE = '22003';
    END IF;

    IF beg_index > 0 THEN
        beg := beg_index - 1;
        FOR i IN 1..occur_index LOOP
            temp_str := substring(string FROM beg + 1);
            pos := position(string_to_search_for IN temp_str);
            IF pos = 0 THEN
                RETURN 0;
            END IF;
            beg := beg + pos;
        END LOOP;

        RETURN beg;
    ELSIF beg_index < 0 THEN
        ss_length := char_length(string_to_search_for);
        length := char_length(string);
        beg := length + 1 + beg_index;

        WHILE beg > 0 LOOP
            temp_str := substring(string FROM beg FOR ss_length);
            IF string_to_search_for = temp_str THEN
                occur_number := occur_number + 1;
                IF occur_number = occur_index THEN
                    RETURN beg;
                END IF;
            END IF;

            beg := beg - 1;
        END LOOP;

        RETURN 0;
    ELSE
        RETURN 0;
    END IF;
END;
$$ LANGUAGE plpgsql STRICT IMMUTABLE;
```
