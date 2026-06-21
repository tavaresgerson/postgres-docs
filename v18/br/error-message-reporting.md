## 55.2. Relatar erros dentro do servidor [#](#ERROR-MESSAGE-REPORTING)

Mensagens de erro, aviso e log geradas dentro do código do servidor devem ser criadas usando `ereport`, ou seu parente mais velho `elog`. O uso dessa função é complexo o suficiente para exigir alguma explicação.

Existem dois elementos obrigatórios para cada mensagem: um nível de gravidade (variando de `DEBUG` a `PANIC`, definido em `src/include/utils/elog.h`) e um texto principal da mensagem. Além disso, existem elementos opcionais, dos quais o mais comum é um código de identificador de erro que segue as convenções da especificação SQL do SQLSTATE. O próprio `ereport` é apenas um macro de concha que existe principalmente para a conveniência sintática de fazer com que a geração de mensagens pareça uma única chamada de função no código-fonte em C. O único parâmetro aceito diretamente pelo `ereport` é o nível de gravidade. O texto principal da mensagem e quaisquer elementos de mensagem opcionais são gerados chamando funções auxiliares, como `errmsg`, dentro da chamada do `ereport`.

Uma chamada típica para `ereport` pode parecer assim:

```
ereport(ERROR,
        errcode(ERRCODE_DIVISION_BY_ZERO),
        errmsg("division by zero"));
```

Isso especifica o nível de gravidade do erro `ERROR` (um erro comum). A chamada `errcode` especifica o código de erro SQLSTATE usando uma macro definida em `src/include/utils/errcodes.h`. A chamada `errmsg` fornece o texto da mensagem principal.

Você também verá frequentemente esse estilo mais antigo, com um conjunto extra de parênteses ao redor das chamadas de função auxiliar:

```
ereport(ERROR,
        (errcode(ERRCODE_DIVISION_BY_ZERO),
         errmsg("division by zero")));
```

As chaves adicionais eram necessárias antes da versão 12 do PostgreSQL, mas agora são opcionais.

Aqui está um exemplo mais complexo:

```
ereport(ERROR,
        errcode(ERRCODE_AMBIGUOUS_FUNCTION),
        errmsg("function %s is not unique",
               func_signature_string(funcname, nargs,
                                     NIL, actual_arg_types)),
        errhint("Unable to choose a best candidate function. "
                "You might need to add explicit typecasts."));
```

Isso ilustra o uso de códigos de formato para incorporar valores de tempo de execução em um texto de mensagem. Além disso, uma mensagem opcional de "sinalização" é fornecida. As chamadas de função auxiliar podem ser escritas em qualquer ordem, mas convencionalmente `errcode` e `errmsg` aparecem primeiro.

Se o nível de gravidade for `ERROR` ou superior, o `ereport` interrompe a execução da consulta atual e não retorna ao chamador. Se o nível de gravidade for inferior a `ERROR`, o `ereport` retorna normalmente.

As rotinas auxiliares disponíveis para `ereport` são:

* `errcode(sqlerrcode)` especifica o código de identificação do erro SQLSTATE para a condição. Se esta rotina não for chamada, o identificador de erro padrão é `ERRCODE_INTERNAL_ERROR` quando o nível de severidade do erro é `ERROR` ou superior, `ERRCODE_WARNING` quando o nível de erro é `WARNING`, caso contrário (para `NOTICE` e abaixo) `ERRCODE_SUCCESSFUL_COMPLETION`. Embora esses padrões sejam frequentemente convenientes, sempre pense se são apropriados antes de omitir a chamada de `errcode()`.
* `errmsg(const char *msg, ...)` especifica o texto da mensagem primária de erro, e possivelmente valores de execução para inseri-lo. As inserções são especificadas por códigos de formato estilo `sprintf`. Além dos códigos de formato padrão aceitos por `sprintf`, o código de formato `%m` pode ser usado para inserir a mensagem de erro retornada por `strerror` para o valor atual de `errno`. [[18]](#ftn.id-1.10.7.3.10.2.2.1.7) `%m` não requer nenhuma entrada correspondente na lista de parâmetros para `errmsg`. Note que a string de mensagem será processada por `gettext` para possível localização antes que os códigos de formato sejam processados.
* `errmsg_internal(const char *msg, ...)` é o mesmo que `errmsg`, exceto que a string de mensagem não será traduzida nem incluída no dicionário de mensagens de internacionalização. Isso deve ser usado para casos de “não pode acontecer” que provavelmente não valem a pena gastar esforço de tradução.
* `errmsg_plural(const char *fmt_singular, const char *fmt_plural, unsigned long n, ...)` é como `errmsg`, mas com suporte para várias formas plurais da mensagem. *`fmt_singular`* é o formato singular em inglês, *`fmt_plural`* é o formato plural em inglês, *`n`* é o valor inteiro que determina qual forma plural é necessária, e os argumentos restantes são formatados de acordo com a string de formato selecionada. Para mais informações, consulte [Seção 56.2.2](nls-programmer.md#NLS-GUIDELINES "56.2.2. Message-Writing Guidelines").
* `errdetail(const char *msg, ...)` fornece uma mensagem opcional “detalha”; isso deve ser usado quando há informações adicionais que parecem inadequadas para colocar na mensagem primária. A string de mensagem é processada da mesma maneira que para `errmsg`.
* `errdetail_internal(const char *msg, ...)` é o mesmo que `errdetail`, exceto que a string de mensagem não será traduzida nem incluída no dicionário de mensagens de internacionalização. Isso deve ser usado para mensagens de detalhes que não valem a pena gastar esforço de tradução, por exemplo, porque são técnicas demais para serem úteis para a maioria dos usuários.
* `errdetail_plural(const char *fmt_singular, const char *fmt_plural, unsigned long n, ...)` é como `errdetail`, mas com suporte para várias formas plurais da mensagem. Para mais informações, consulte [Seção 56.2.2](nls-programmer.md#NLS-GUIDELINES "56.2.2. Message-Writing Guidelines").
* `errdetail_log(const char *msg, ...)` é o mesmo que `errdetail` exceto que essa string vai apenas para o log do servidor, nunca para o cliente. Se `errdetail` (ou um dos seus equivalentes acima) e `errdetail_log` forem usados, então uma string vai para o cliente e a outra para o log. Isso é útil para detalhes de erro que são muito sensíveis à segurança ou muito volumosos para incluir no relatório enviado ao cliente.
* `errdetail_log_plural(const char *fmt_singular, const char *fmt_plural, unsigned long n, ...)` é como `errdetail_log`, mas com suporte para várias formas plurais da mensagem. Para mais informações, consulte [Seção 56.2.2](nls-programmer.md#NLS-GUIDELINES "56.2.2. Message-Writing Guidelines").
* `errhint(const char *msg, ...)` fornece uma mensagem opcional “sinal”; isso deve ser usado quando se oferecem sugestões sobre como corrigir o problema, em oposição a detalhes factuais sobre o que deu errado. A string de mensagem é processada da mesma maneira que para `errmsg`.
* `errhint_plural(const char *fmt_singular, const char *fmt_plural, unsigned long n, ...)` é como `errhint`, mas com suporte para várias formas plurais da mensagem. Para mais informações, consulte [Seção 56.2.2](nls-programmer.md#NLS-GUIDELINES "56.2.2. Message-Writing Guidelines").
* `errcontext(const char *msg, ...)` normalmente não é chamado diretamente de um site de mensagem `ereport`; em vez disso, é usado em funções de callback `error_context_stack` para fornecer informações sobre o contexto em que um erro ocorreu, como a localização atual em uma função PL. A string de mensagem é processada da mesma maneira que para `errmsg`. Ao contrário das outras funções auxiliares, esta pode ser chamada mais de uma vez por chamada de `ereport`; as sucessivas strings fornecidas são concatenadas com novas linhas de separação.
* `errposition(int cursorpos)` especifica a localização textual de um erro dentro de uma string de consulta. Atualmente, é útil apenas para erros detectados nas fases de análise lexical e sintática do processamento de consultas.
* `errtable(Relation rel)` especifica uma relação cujo nome e nome do esquema devem ser incluídos como campos auxiliares no relatório de erro.
* `errtablecol(Relation rel, int attnum)` pode ser chamado para especificar a supressão da parte `STATEMENT:` de uma mensagem no log do postmaster. Geralmente, isso é apropriado se o texto da mensagem inclui a declaração atual já.
* `errhidecontext(bool hide_ctx)` pode ser chamado para especificar a supressão da parte `CONTEXT:` de uma mensagem no log do postmaster. Isso deve ser usado apenas para mensagens de depuração verbose onde a inclusão repetida do contexto faria o log ficar muito grande.

### Nota

No máximo, uma das funções `errtable`, `errtablecol`, `errtableconstraint`, `errdatatype` ou `errdomainconstraint` deve ser usada em uma chamada `ereport`. Essas funções existem para permitir que as aplicações extraiam o nome de um objeto de banco de dados associado à condição de erro sem ter que examinar o texto do erro potencialmente localizado. Essas funções devem ser usadas em relatórios de erro para os quais é provável que as aplicações desejem ter tratamento automático de erros. A partir do PostgreSQL 9.3, a cobertura completa existe apenas para erros na classe SQLSTATE 23 (violação de restrição de integridade), mas isso provavelmente será expandido no futuro.

Existe uma função mais antiga `elog` que ainda é muito utilizada. Uma chamada `elog`:

```
elog(level, "format string", ...);
```

é exatamente equivalente a:

```
ereport(level, errmsg_internal("format string", ...));
```

Observe que o código de erro SQLSTATE é sempre predefinido e a string de mensagem não está sujeita à tradução. Portanto, `elog` deve ser usado apenas para erros internos e registro de depuração de baixo nível. Qualquer mensagem que provavelmente seja de interesse para usuários comuns deve passar por `ereport`. No entanto, há verificações de erro internas suficientes que não podem ocorrer no sistema que `elog` ainda é amplamente utilizado; é preferido para essas mensagens por sua simplicidade notarial.

Conselhos sobre como escrever boas mensagens de erro podem ser encontrados em [Seção 55.3](error-style-guide.md).

---

Ou seja, o valor que estava em vigor quando a chamada (#id-1.10.7.3.10.2.2.1.7) foi alcançada; as alterações de `errno` nas rotinas de relatórios auxiliares não a afetarão. Isso não seria verdade se você escrevesse `strerror(errno)` explicitamente na lista de parâmetros de `errmsg`; portanto, não faça isso.