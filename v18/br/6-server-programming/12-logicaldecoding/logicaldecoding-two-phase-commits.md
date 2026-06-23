## 47.10. Suporte a Compromisso de Dois Fases para Decodificação Lógica [#](#LOGICALDECODING-TWO-PHASE-COMMITS)

Com os callbacks dos plugins de saída básica (por exemplo, `begin_cb`, `change_cb`, `commit_cb` e `message_cb`) os comandos de commit de duas fases como `PREPARE TRANSACTION`, `COMMIT PREPARED` e `ROLLBACK PREPARED` não são decodificados. Enquanto o `PREPARE TRANSACTION` é ignorado, o `COMMIT PREPARED` é decodificado como um `COMMIT` e o `ROLLBACK PREPARED` é decodificado como um `ROLLBACK`.

Para suportar o streaming de comandos de duas fases, um plugin de saída precisa fornecer callbacks adicionais. Existem vários callbacks de commit de duas fases que são necessários, (`begin_prepare_cb`, `prepare_cb`, `commit_prepared_cb`, `rollback_prepared_cb` e `stream_prepare_cb`) e um callback opcional (`filter_prepare_cb`).

Se os callbacks dos plugins de saída para a decodificação de comandos de comprovante de dois estágios forem fornecidos, então, em `PREPARE TRANSACTION`, as alterações dessa transação são decodificadas, passadas para o plugin de saída e o callback `prepare_cb` é invocado. Isso difere da configuração básica de decodificação, onde as alterações são passadas apenas para o plugin de saída quando uma transação é comprometida. O início de uma transação preparada é indicado pelo callback `begin_prepare_cb`.

Quando uma transação preparada é desfeita usando o `ROLLBACK PREPARED`, então o callback `rollback_prepared_cb` é invocado e quando a transação preparada é confirmada usando o `COMMIT PREPARED`, então o callback `commit_prepared_cb` é invocado.

Opcionalmente, o plugin de saída pode definir regras de filtragem via `filter_prepare_cb` para decodificar apenas transações específicas em duas fases. Isso pode ser alcançado por correspondência de padrões no *`gid`* ou por meio de consultas usando o *`xid`*.

Os usuários que desejam decodificar transações preparadas precisam estar atentos aos pontos mencionados abaixo:

* Se a transação preparada tiver bloqueado as tabelas de catálogo do [usuário] exclusivamente, a decodificação da preparação pode bloquear até que a transação principal seja comprometida.
* A solução de replicação lógica que constrói um compromisso de duas fases usando este recurso pode entrar em deadlock se a transação preparada tiver bloqueado as tabelas de catálogo do [usuário] exclusivamente. Para evitar isso, os usuários devem abster-se de ter bloqueios em tabelas de catálogo (por exemplo, o comando explícito `LOCK`), em tais transações. Consulte [Seção 47.8.2](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-CAVEATS) para obter os detalhes.