## 24.2. Reindexação rotineira [#](#ROUTINE-REINDEX)

Em algumas situações, vale a pena reconstruir os índices periodicamente com o comando [REINDEX][(sql-reindex.md "REINDEX")], ou uma série de etapas individuais de reconstrução.

As páginas de índice de árvore B que se tornaram completamente vazias são recuperadas para uso novamente. No entanto, ainda há uma possibilidade de uso ineficiente do espaço: se todas as chaves de índice, exceto algumas, tiverem sido excluídas de uma página, a página permanece alocada. Portanto, um padrão de uso em que a maioria, mas não todas, as chaves em cada intervalo sejam eventualmente excluídas verá um uso ruim do espaço. Para tais padrões de uso, é recomendado o reindexamento periódico.

O potencial de inchaço em índices não em forma de B não foi bem pesquisado. É uma boa ideia monitorar periodicamente o tamanho físico do índice ao usar qualquer tipo de índice não em forma de B.

Além disso, para índices de árvore B, um índice recém-construído é ligeiramente mais rápido para acessar do que um que foi atualizado muitas vezes, porque as páginas logicamente adjacentes geralmente também são fisicamente adjacentes em um índice recém-construído. (Esta consideração não se aplica a índices que não são de árvore B.) Pode valer a pena reindexar periodicamente apenas para melhorar a velocidade de acesso.

[REINDEX](sql-reindex.md "REINDEX") pode ser usado de forma segura e fácil em todos os casos. Esse comando requer um bloqueio `ACCESS EXCLUSIVE` por padrão, portanto, é frequentemente preferível executá-lo com sua opção `CONCURRENTLY`, que requer apenas um bloqueio `SHARE UPDATE EXCLUSIVE`.