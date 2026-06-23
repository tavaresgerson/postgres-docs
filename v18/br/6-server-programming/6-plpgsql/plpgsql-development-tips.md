## 41.12. Dicas para o desenvolvimento em PL/pgSQL [#](#PLPGSQL-DEVELOPMENT-TIPS)

* [41.12.1. Tratamento de aspas](plpgsql-development-tips.md#PLPGSQL-QUOTE-TIPS)
* [41.12.2. Verificações adicionais de tempo de compilação e tempo de execução](plpgsql-development-tips.md#PLPGSQL-EXTRA-CHECKS)

Uma boa maneira de se desenvolver no PL/pgSQL é usar o editor de texto que você preferir para criar suas funções, e em outra janela, usar o psql para carregar e testar essas funções. Se você estiver fazendo isso dessa maneira, é uma boa ideia escrever a função usando `CREATE OR REPLACE FUNCTION`. Dessa forma, você pode simplesmente recarregar o arquivo para atualizar a definição da função. Por exemplo:

```
CREATE OR REPLACE FUNCTION testfunc(integer) RETURNS integer AS $$
          ....
$$ LANGUAGE plpgsql;
```

Ao executar o psql, você pode carregar ou recarregar um arquivo de definição de função com:

```
\i filename.sql
```

e, em seguida, emitir imediatamente comandos SQL para testar a função.

Outra boa maneira de se desenvolver em PL/pgSQL é com uma ferramenta de acesso a banco de dados com interface gráfica que facilita o desenvolvimento em uma linguagem procedural. Um exemplo de tal ferramenta é o pgAdmin, embora outras existam. Essas ferramentas geralmente oferecem recursos convenientes, como escapar de aspas simples e facilitar a recriação e depuração de funções.

### 41.12.1. Tratamento de aspas [#](#PLPGSQL-QUOTE-TIPS)

O código de uma função PL/pgSQL é especificado em `CREATE FUNCTION` como uma literal de string. Se você escrever a literal de string da maneira comum com aspas duplas ao redor, então quaisquer aspas dentro do corpo da função devem ser duplicadas; da mesma forma, quaisquer barras invertidas devem ser duplicadas (assumindo que a sintaxe de string de escape é usada). Duplicar aspas é, no máximo, tedioso, e em casos mais complicados, o código pode se tornar completamente incompreensível, porque você pode facilmente se encontrar precisando de meia dúzia ou mais aspas adjacentes. Recomenda-se que você escreva o corpo da função como uma literal de string "com aspas de dólar" (ver [Seção 4.1.2.4] (sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING "4.1.2.4. Dollar-Quoted String Constants")). Na abordagem de citação de dólar, você nunca duplica nenhuma aspas, mas, em vez disso, tome cuidado para escolher um delimitador de citação de dólar diferente para cada nível de aninhamento que você precisa. Por exemplo, você pode escrever o comando `CREATE FUNCTION` como:

```
CREATE OR REPLACE FUNCTION testfunc(integer) RETURNS integer AS $PROC$
          ....
$PROC$ LANGUAGE plpgsql;
```

Nesse contexto, você pode usar aspas para strings literais simples em comandos SQL e `$$` para delimitar fragmentos de comandos SQL que você está montando como strings. Se você precisar citar texto que inclui `$$`, você pode usar `$Q$`, e assim por diante.

O gráfico a seguir mostra o que você deve fazer ao escrever aspas sem citação em dólar. Isso pode ser útil ao traduzir código com citação pré-dólar em algo mais compreensível.

1. Para iniciar e finalizar o corpo da função, por exemplo: [#](#PLPGSQL-QUOTE-TIPS-1-QUOT)

```
CREATE FUNCTION foo() RETURNS integer AS ' .... ' LANGUAGE plpgsql;
```

Em qualquer parte do corpo de uma função com aspas simples, as aspas *devem* aparecer em pares.

2 aspas [#](#PLPGSQL-QUOTE-TIPS-2-QUOT): Para aspas de cadeia dentro do corpo da função, por exemplo:

```
a_output := ''Blah''; SELECT * FROM users WHERE f_name=''foobar'';
```

Na abordagem de citação em dólares, você apenas escreveria:

```
a_output := 'Blah'; SELECT * FROM users WHERE f_name='foobar';
```

que é exatamente o que o analisador PL/pgSQL veria em qualquer caso.

4 aspas [#](#PLPGSQL-QUOTE-TIPS-4-QUOT): Quando você precisa de uma única aspa em uma constante de string dentro do corpo da função, por exemplo:

```
a_output := a_output || '' AND name LIKE ''''foobar'''' AND xyz''
```

O valor que realmente será anexado a `a_output` seria: `AND name LIKE 'foobar' AND xyz`.

Na abordagem de citação em dólares, você escreveria:

```
a_output := a_output || $$ AND name LIKE 'foobar' AND xyz$$
```

atenção para que quaisquer delimitadores de citação em dólares ao redor disso não sejam apenas `$$`.

6 aspas [#](#PLPGSQL-QUOTE-TIPS-6-QUOT): Quando uma única aspa em uma string dentro do corpo da função está adjacente à extremidade dessa constante de string, por exemplo:

```
a_output := a_output || '' AND name LIKE ''''foobar''''''
```

O valor anexado a `a_output` seria então: `AND name LIKE 'foobar'`.

Na abordagem de cotação em dólares, isso se torna:

```
a_output := a_output || $$ AND name LIKE 'foobar'$$
```

10 aspas [#](#PLPGSQL-QUOTE-TIPS-10-QUOT): Quando você deseja duas aspas simples em uma constante de cadeia (que representa 8 aspas) e esta é adjacente ao final dessa constante de cadeia (mais 2). Você provavelmente só precisará disso se estiver escrevendo uma função que gera outras funções, como em [Exemplo 41.10](plpgsql-porting.md#PLPGSQL-PORTING-EX2). Por exemplo:

```
a_output := a_output || '' if v_'' || referrer_keys.kind || '' like ''''''''''
    || referrer_keys.key_string || ''''''''''
    then return ''''''  || referrer_keys.referrer_type
    || ''''''; end if;'';
```

O valor de `a_output` seria, então:

```
if v_... like ''...'' then return ''...''; end if;
```

Na abordagem de cotação em dólares, isso se torna:

```
a_output := a_output || $$ if v_$$ || referrer_keys.kind || $$ like '$$
    || referrer_keys.key_string || $$'
    then return '$$  || referrer_keys.referrer_type
    || $$'; end if;$$;
```

onde assumimos que só precisamos colocar aspas simples em `a_output`, porque será requote antes do uso.

### 41.12.2. Verificações adicionais de tempo de compilação e tempo de execução [#](#PLPGSQL-EXTRA-CHECKS)

Para ajudar o usuário a encontrar casos de problemas simples, mas comuns, antes que causem danos, o PL/pgSQL fornece informações adicionais *`checks`*. Quando habilitado, dependendo da configuração, eles podem ser usados para emitir `WARNING` ou `ERROR` durante a compilação de uma função. Uma função que recebeu um `WARNING` pode ser executada sem produzir mensagens adicionais, portanto, é aconselhável testar em um ambiente de desenvolvimento separado.

É recomendado definir `plpgsql.extra_warnings`, ou `plpgsql.extra_errors`, conforme apropriado, para `"all"` em ambientes de desenvolvimento e/ou teste.

Esses controles adicionais são habilitados através das variáveis de configuração `plpgsql.extra_warnings` para avisos e `plpgsql.extra_errors` para erros. Ambos podem ser definidos como uma lista de verificações separadas por vírgula, `"none"` ou `"all"`. O padrão é `"none"`. Atualmente, a lista de verificações disponíveis inclui:

`shadowed_variables` [#](#PLPGSQL-EXTRA-CHECKS-SHADOWED-VARIABLES) : Verifica se uma declaração sombreia uma variável previamente definida.

`strict_multi_assignment` [#](#PLPGSQL-EXTRA-CHECKS-STRICT-MULTI-ASSIGNMENT): Alguns comandos PL/pgSQL permitem atribuir valores a mais de uma variável de cada vez, como `SELECT INTO`. Normalmente, o número de variáveis alvo e o número de variáveis de origem devem correspondere, embora o PL/pgSQL use `NULL` para valores ausentes e variáveis extras são ignoradas. Habilitar esta verificação fará com que o PL/pgSQL lançe um `WARNING` ou `ERROR` sempre que o número de variáveis alvo e o número de variáveis de origem forem diferentes.

`too_many_rows` [#](#PLPGSQL-EXTRA-CHECKS-TOO-MANY-ROWS): Ativação desta verificação fará com que o PL/pgSQL verifique se uma consulta dada retorna mais de uma linha quando uma cláusula `INTO` é usada. Como um `INTO` está sendo usado apenas uma linha, ter uma consulta retornando várias linhas é geralmente ineficiente e/ou não determinístico e, portanto, é provável que seja um erro.

O exemplo a seguir mostra o efeito de `plpgsql.extra_warnings` definido como `shadowed_variables`:

```
SET plpgsql.extra_warnings TO 'shadowed_variables';

CREATE FUNCTION foo(f1 int) RETURNS int AS $$ DECLARE f1 int; BEGIN RETURN f1; END; $$ LANGUAGE plpgsql; WARNING:  variable "f1" shadows a previously defined variable LINE 3: f1 int; ^ CREATE FUNCTION
```

O exemplo abaixo mostra os efeitos de definir `plpgsql.extra_warnings` para `strict_multi_assignment`:

```
SET plpgsql.extra_warnings TO 'strict_multi_assignment';

CREATE OR REPLACE FUNCTION public.foo() RETURNS void LANGUAGE plpgsql AS $$ DECLARE x int; y int; BEGIN SELECT 1 INTO x, y; SELECT 1, 2 INTO x, y; SELECT 1, 2, 3 INTO x, y; END; $$;

SELECT foo(); WARNING:  number of source and target fields in assignment does not match DETAIL:  strict_multi_assignment check of extra_warnings is active. HINT:  Make sure the query returns the exact list of columns. WARNING:  number of source and target fields in assignment does not match DETAIL:  strict_multi_assignment check of extra_warnings is active. HINT:  Make sure the query returns the exact list of columns.

 foo -----

(1 row)
```
