## 41.9. Erros e Mensagens [#](#PLPGSQL-ERRORS-AND-MESSAGES)

* [41.9.1. Relatando Erros e Mensagens](plpgsql-errors-and-messages.md#PLPGSQL-STATEMENTS-RAISE)
* [41.9.2. Verificando Afirmações](plpgsql-errors-and-messages.md#PLPGSQL-STATEMENTS-ASSERT)

### 41.9.1. Relatar erros e mensagens [#](#PLPGSQL-STATEMENTS-RAISE)

Utilize a declaração `RAISE` para relatar mensagens e levantar erros.

```
RAISE [ level ] 'format' [, expression [, ... ]] [ USING option { = | := } expression [, ... ] ];
RAISE [ level ] condition_name [ USING option { = | := } expression [, ... ] ];
RAISE [ level ] SQLSTATE 'sqlstate' [ USING option { = | := } expression [, ... ] ];
RAISE [ level ] USING option { = | := } expression [, ... ];
RAISE ;
```

A opção *`level`* especifica a gravidade do erro. Os níveis permitidos são `DEBUG`, `LOG`, `INFO`, `NOTICE`, `WARNING` e `EXCEPTION`, sendo `EXCEPTION` o padrão. `EXCEPTION` gera um erro (que normalmente interrompe a transação atual); os outros níveis apenas geram mensagens de diferentes níveis de prioridade. Se as mensagens de uma prioridade específica são relatadas ao cliente, escritas no log do servidor ou ambas, é controlado pelas variáveis de configuração [log_min_messages](runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) e [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES). Consulte [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") para mais informações.

Na primeira variante de sintaxe, após o *`level`* (se houver), escreva uma *`format`* (que deve ser uma literal de string simples, não uma expressão). A string de formato especifica o texto da mensagem de erro a ser relatado. A string de formato pode ser seguida por expressões de argumento opcionais a serem inseridas na mensagem. Dentro da string de formato, `%` é substituído pela representação de string do valor do próximo argumento opcional. Escreva `%%` para emitir um literal `%`. O número de argumentos deve corresponder ao número de `%` marcadores de posição na string de formato, ou uma erro é levantado durante a compilação da função.

Neste exemplo, o valor de `v_job_id` substituirá o `%` na string:

```
RAISE NOTICE 'Calling cs_create_job(%)', v_job_id;
```

Nas segunda e terceira variantes de sintaxe, *`condition_name`* e *`sqlstate`* especificam um nome de condição de erro ou um código SQLSTATE de cinco caracteres, respectivamente. Consulte [Apêndice A](errcodes-appendix.md) para os nomes de condição de erro válidos e os códigos SQLSTATE predefinidos.

Aqui estão exemplos de uso de *`condition_name`* e *`sqlstate`*:

```
RAISE division_by_zero;
RAISE WARNING SQLSTATE '22012';
```

Em qualquer uma dessas variantes de sintaxe, você pode anexar informações adicionais ao relatório de erro escrevendo `USING` seguido por *`option`* = *`expression`* itens. Cada *`expression`* pode ser qualquer expressão com valor de cadeia. As palavras-chave permitidas para a chave *`option`* são:

`MESSAGE` [#](#RAISE-USING-OPTION-MESSAGE): Define o texto da mensagem de erro. Esta opção não pode ser usada na primeira variante de sintaxe, uma vez que a mensagem já está fornecida.

`DETAIL` [#](#RAISE-USING-OPTION-DETAIL): Fornece uma mensagem de detalhe de erro.

`HINT` [#](#RAISE-USING-OPTION-HINT): Fornece uma mensagem de dica.

`ERRCODE` [#](#RAISE-USING-OPTION-ERRCODE): Especifica o código de erro (SQLSTATE) a ser relatado, seja pelo nome da condição, conforme mostrado em [Apêndice A](errcodes-appendix.md "Appendix A. PostgreSQL Error Codes"), ou diretamente como um código SQLSTATE de cinco caracteres. Esta opção não pode ser usada na segunda ou terceira variante de sintaxe, uma vez que o código de erro já é fornecido.

`COLUMN` `CONSTRAINT` `DATATYPE` `TABLE` `SCHEMA` [#](#RAISE-USING-OPTION-COLUMN): Fornece o nome de um objeto relacionado.

Este exemplo abortará a transação com a mensagem de erro e o aviso fornecidos:

```
RAISE EXCEPTION 'Nonexistent ID --> %', user_id
      USING HINT = 'Please check your user ID';
```

Esses dois exemplos mostram formas equivalentes de definir o SQLSTATE:

```
RAISE 'Duplicate user ID: %', user_id USING ERRCODE = 'unique_violation';
RAISE 'Duplicate user ID: %', user_id USING ERRCODE = '23505';
```

Outra maneira de produzir o mesmo resultado é:

```
RAISE unique_violation USING MESSAGE = 'Duplicate user ID: ' || user_id;
```

Como mostrado na quarta variante de sintaxe, também é possível escrever `RAISE USING` ou `RAISE level USING` e colocar tudo o resto na lista `USING`.

A última variante de `RAISE` não tem nenhum parâmetro. Este formulário só pode ser usado dentro da cláusula `EXCEPTION` de um bloco `BEGIN`; ele faz com que o erro atualmente sendo tratado seja relançado.

### Nota

Antes do PostgreSQL 9.1, `RAISE` sem parâmetros era interpretado como relançar o erro do bloco que contém o manipulador de exceção ativo. Assim, uma cláusula `EXCEPTION` aninhada nesse manipulador não conseguia capturá-lo, mesmo que a `RAISE` estivesse dentro do bloco da cláusula aninhada `EXCEPTION`. Isso foi considerado surpreendente e incompatível com o PL/SQL da Oracle.

Se nenhum nome de condição ou SQLSTATE for especificado em um comando `RAISE EXCEPTION`, o padrão é usar `raise_exception` (`P0001`). Se nenhum texto de mensagem for especificado, o padrão é usar o nome da condição ou SQLSTATE como texto de mensagem.

### Nota

Ao especificar um código de erro pelo código SQLSTATE, você não está limitado aos códigos de erro predefinidos, mas pode selecionar qualquer código de erro composto por cinco dígitos e/ou letras maiúsculas ASCII, exceto `00000`. É recomendável que você evite lançar códigos de erro que terminem em três zeros, porque esses são códigos de categoria e só podem ser capturados ao capturar toda a categoria.

### 41.9.2. Verificação de Afirmações [#](#PLPGSQL-STATEMENTS-ASSERT)

A declaração `ASSERT` é uma abreviação conveniente para inserir verificações de depuração em funções PL/pgSQL.

```
ASSERT condition [ , message ];
```

O *`condition`* é uma expressão booleana que deve sempre ser avaliada como verdadeira; se for, a declaração `ASSERT` não faz nada a mais. Se o resultado for falso ou nulo, então uma exceção `ASSERT_FAILURE` é levantada. (Se um erro ocorrer ao avaliar o *`condition`*, ele é relatado como um erro normal.)

Se o opcional *`message`* for fornecido, é uma expressão cujo resultado (se não for nulo) substitui o texto da mensagem de erro padrão “afirmação falhou”, caso o *`condition`* falhe. A expressão *`message`* não é avaliada no caso normal em que a afirmação é bem-sucedida.

A verificação de afirmações pode ser habilitada ou desabilitada através do parâmetro de configuração `plpgsql.check_asserts`, que aceita um valor booleano; o padrão é `on`. Se este parâmetro for `off`, então as declarações `ASSERT` não fazem nada.

Observe que `ASSERT` é destinado a detectar erros de programa, não para relatar condições de erro comuns. Use a declaração `RAISE`, descrita acima, para isso.