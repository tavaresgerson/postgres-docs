## 44.9. Funções de Utilidade [#](#PLPYTHON-UTIL)

O módulo `plpy` também fornece as funções



<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <code class="literal">
    plpy.debug(
    <em class="replaceable">
     <code>
      msg, **kwargs
     </code>
    </em>
    )
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    plpy.log(
    <em class="replaceable">
     <code>
      msg, **kwargs
     </code>
    </em>
    )
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    plpy.info(
    <em class="replaceable">
     <code>
      msg, **kwargs
     </code>
    </em>
    )
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    plpy.notice(
    <em class="replaceable">
     <code>
      msg, **kwargs
     </code>
    </em>
    )
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    plpy.warning(
    <em class="replaceable">
     <code>
      msg, **kwargs
     </code>
    </em>
    )
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    plpy.error(
    <em class="replaceable">
     <code>
      msg, **kwargs
     </code>
    </em>
    )
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    plpy.fatal(
    <em class="replaceable">
     <code>
      msg, **kwargs
     </code>
    </em>
    )
   </code>
  </td>
 </tr>
</table>






`plpy.error` e `plpy.fatal` realmente levantam uma exceção do Python que, se não for detectada, se propaga para a consulta que a chamou, fazendo com que a transação ou subtransação atual seja abortada. `raise plpy.Error(msg)` e `raise plpy.Fatal(msg)` são equivalentes ao chamar `plpy.error(msg)` e `plpy.fatal(msg)`, respectivamente, mas o formulário `raise` não permite passar argumentos por palavra-chave. As outras funções geram apenas mensagens de diferentes níveis de prioridade. Se as mensagens de uma prioridade específica são relatadas ao cliente, escritas no log do servidor ou ambas, é controlado pelas variáveis de configuração [log_min_messages](runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) e [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES). Consulte [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") para mais informações.

O argumento *`msg`* é fornecido como um argumento posicional. Para compatibilidade reversa, pode ser fornecido mais de um argumento posicional. Nesse caso, a representação em cadeia da tupla de argumentos posicionais se torna a mensagem relatada ao cliente.

Os seguintes argumentos com palavras-chave são aceitos:



<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <code class="literal">
    detail
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    hint
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    sqlstate
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    schema_name
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    table_name
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    column_name
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    datatype_name
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    constraint_name
   </code>
  </td>
 </tr>
</table>






A representação em cadeia dos objetos passados como argumentos com palavras-chave é usada para enriquecer as mensagens relatadas ao cliente. Por exemplo:

```
CREATE FUNCTION raise_custom_exception() RETURNS void AS $$
plpy.error("custom exception message",
           detail="some info about exception",
           hint="hint for users")
$$ LANGUAGE plpython3u;

=# SELECT raise_custom_exception();
ERROR:  plpy.Error: custom exception message
DETAIL:  some info about exception
HINT:  hint for users
CONTEXT:  Traceback (most recent call last):
  PL/Python function "raise_custom_exception", line 4, in <module>
    hint="hint for users")
PL/Python function "raise_custom_exception"
```

Outro conjunto de funções utilitárias são `plpy.quote_literal(string)`, `plpy.quote_nullable(string)` e `plpy.quote_ident(string)`. Eles são equivalentes às funções de citação internas descritas em [Seção 9.4](functions-string.md "9.4. String Functions and Operators"). Eles são úteis ao construir consultas ad-hoc. Um equivalente PL/Python de SQL dinâmico de [Exemplo 41.1](plpgsql-statements.md#PLPGSQL-QUOTE-LITERAL-EXAMPLE "Example 41.1. Quoting Values in Dynamic Queries") seria:

```
plpy.execute("UPDATE tbl SET %s = %s WHERE key = %s" % (
    plpy.quote_ident(colname),
    plpy.quote_nullable(newvalue),
    plpy.quote_literal(keyvalue)))
```
