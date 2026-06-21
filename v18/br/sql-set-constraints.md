## CONSTRANGÊNTIOS DE DEFINIÇÃO

SET CONSTRAINTS — definir o horário de verificação de restrições para a transação atual

## Sinopse

```
SET CONSTRAINTS { ALL | name [, ...] } { DEFERRED | IMMEDIATE }
```

## Descrição

`SET CONSTRAINTS` define o comportamento da verificação de restrições dentro da transação atual. As restrições `IMMEDIATE` são verificadas no final de cada declaração. As restrições `DEFERRED` não são verificadas até o compromisso da transação. Cada restrição tem seu próprio modo `IMMEDIATE` ou `DEFERRED`.

Ao criar uma restrição, uma das três características é atribuída: `DEFERRABLE INITIALLY DEFERRED`, `DEFERRABLE INITIALLY IMMEDIATE` ou `NOT DEFERRABLE`. A terceira classe é sempre `IMMEDIATE` e não é afetada pelo comando `SET CONSTRAINTS`. As duas primeiras classes iniciam cada transação no modo indicado, mas seu comportamento pode ser alterado dentro de uma transação por `SET CONSTRAINTS`.

`SET CONSTRAINTS` com uma lista de nomes de restrições altera o modo apenas dessas restrições (que devem ser todas deferíveis). Cada nome de restrição pode ser qualificado pelo esquema. O caminho atual de pesquisa do esquema é usado para encontrar o primeiro nome correspondente se nenhum nome de esquema for especificado. `SET CONSTRAINTS ALL` altera o modo de todas as restrições deferíveis.

Quando o `SET CONSTRAINTS` altera o modo de uma restrição de `DEFERRED` para `IMMEDIATE`, o novo modo entra em vigor retroativamente: quaisquer modificações de dados pendentes que seriam verificadas no final da transação são verificadas, em vez disso, durante a execução do comando `SET CONSTRAINTS`. Se qualquer restrição desse tipo for violada, o `SET CONSTRAINTS` falha (e não altera o modo da restrição). Assim, o `SET CONSTRAINTS` pode ser usado para forçar a verificação de restrições em um ponto específico de uma transação.

Atualmente, apenas as restrições `UNIQUE`, `PRIMARY KEY`, `REFERENCES` (chave estrangeira) e `EXCLUDE` são afetadas por este ajuste. As restrições `NOT NULL` e `CHECK` são sempre verificadas imediatamente quando uma linha é inserida ou modificada (*não* no final da declaração). As restrições de unicidade e exclusão que não foram declaradas `DEFERRABLE` também são verificadas imediatamente.

O disparo de gatilhos que são declarados como "gatilhos de restrição" também é controlado por esta configuração — eles são disparados ao mesmo tempo que a restrição associada deve ser verificada.

## Notas

Como o PostgreSQL não exige que os nomes de restrição sejam únicos dentro de um esquema (mas apenas por tabela), é possível que haja mais de um jogo para um nome de restrição especificado. Neste caso, `SET CONSTRAINTS` atuará em todos os jogos. Para um nome não qualificado por esquema, uma vez que um jogo ou jogos foram encontrados em algum esquema no caminho de pesquisa, os esquemas que aparecem mais tarde no caminho não são pesquisados.

Este comando altera apenas o comportamento das restrições dentro da transação atual. Emitir este comando fora de um bloco de transação emite um aviso e, de outra forma, não tem efeito.

## Compatibilidade

Este comando cumpre o comportamento definido no padrão SQL, exceto pela limitação de que, no PostgreSQL, ele não se aplica às restrições `NOT NULL` e `CHECK`. Além disso, o PostgreSQL verifica as restrições de unicidade não diferíveis imediatamente, não no final da declaração, como o padrão sugere.