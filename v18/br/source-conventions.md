## 55.4. Convenções de codificação variadas [#](#SOURCE-CONVENTIONS)

### C Padrão [#](#SOURCE-CONVENTIONS-C-STANDARD)

O código no PostgreSQL só deve confiar nas funcionalidades de linguagem disponíveis no padrão C99. Isso significa que um compilador C99 conforme deve ser capaz de compilar o postgres, pelo menos, à parte de algumas peças dependentes da plataforma.

Algumas características incluídas no padrão C99, atualmente, não são permitidas para serem usadas no código principal do PostgreSQL. Isso inclui, atualmente, matrizes de comprimento variável, declarações e códigos interligados, comentários `//`, nomes de caracteres universais. As razões para isso incluem portabilidade e práticas históricas.

As características de revisões posteriores da norma C ou características específicas do compilador podem ser usadas, se houver um fallback.

Por exemplo, `_Static_assert()` e `__builtin_constant_p` são atualmente utilizados, embora sejam de revisões mais recentes do padrão C e, respetivamente, uma extensão do GCC. Se não estiverem disponíveis, respectivamente, fazemos o uso de um substituto compatível com C99 que realiza os mesmos verificações, mas emite mensagens bastante crípticas e não utilizamos `__builtin_constant_p`.

### Macros semelhantes a funções e funções inline [#](#SOURCE-CONVENTIONS-MACROS-INLINE)

Ambas as macros com argumentos e as funções `static inline` podem ser usadas. As últimas são preferíveis se houver riscos de múltiplas avaliações quando escritas como uma macro, como, por exemplo, o caso com

```
#define Max(x, y)       ((x) > (y) ? (x) : (y))
```

ou quando a macro seria muito longa. Em outros casos, é apenas possível usar macros, ou pelo menos é mais fácil. Por exemplo, porque expressões de vários tipos precisam ser passadas para a macro.

Quando a definição de uma função inline faz referência a símbolos (ou seja, variáveis e funções) que estão disponíveis apenas como parte do backend, a função pode não ser visível quando incluída a partir de código do frontend.

```
#ifndef FRONTEND
static inline MemoryContext
MemoryContextSwitchTo(MemoryContext context)
{
    MemoryContext old = CurrentMemoryContext;

    CurrentMemoryContext = context;
    return old;
}
#endif   /* FRONTEND */
```

Neste exemplo `CurrentMemoryContext`, que está disponível apenas no backend, é feita referência e, assim, a função é ocultada com um `#ifndef FRONTEND`. Esta regra existe porque alguns compiladores emitem referências a símbolos contidos em funções internas, mesmo que a função não seja usada.

### Manipuladores de Sinal de Escrita [#](#SOURCE-CONVENTIONS-SIGNAL-HANDLERS)

Para ser adequado para ser executado dentro de um código de manipulador de sinal, ele precisa ser escrito com muito cuidado. O problema fundamental é que, a menos que bloqueado, um manipulador de sinal pode interromper o código a qualquer momento. Se o código dentro do manipulador de sinal usar o mesmo estado que o código externo, pode ocorrer caos. Como exemplo, considere o que acontece se um manipulador de sinal tenta adquirir uma chave que já está sendo mantida no código interrompido.

Salvo acordos especiais, os códigos de manipulação de sinal podem chamar apenas funções seguras para sinal asíncrono (conforme definido no POSIX) e acessar variáveis do tipo `volatile sig_atomic_t`. Algumas funções em `postgres` também são consideradas seguras para sinal, importante `SetLatch()`.

Na maioria dos casos, os manipuladores de sinal devem apenas anotar que um sinal chegou e acordar o código que está sendo executado fora do manipulador usando um gatilho. Um exemplo de tal manipulador é o seguinte:

```
static void
handle_sighup(SIGNAL_ARGS)
{
    got_SIGHUP = true;
    SetLatch(MyLatch);
}
```

### Chamando Pontos de Função [#](#SOURCE-CONVENTIONS-FUNCTION-POINTERS)

Para maior clareza, é preferível desfazer explicitamente uma ponteiro de função ao chamar a função apontada, se o ponteiro for uma variável simples, por exemplo:

```
(*emit_log_hook) (edata);
```

(mesmo que `emit_log_hook(edata)` também funcione). Quando o ponteiro de função faz parte de uma estrutura, então a pontuação extra pode e geralmente deve ser omitida, por exemplo:

```
paramInfo->paramFetch(paramInfo, paramId);
```
