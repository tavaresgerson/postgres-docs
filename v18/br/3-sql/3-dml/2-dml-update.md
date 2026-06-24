### 6.2. Atualização de Dados [#](#DML-UPDATE)

A modificação de dados que já estão no banco de dados é conhecida como atualização. Você pode atualizar linhas individuais, todas as linhas de uma tabela ou um subconjunto de todas as linhas. Cada coluna pode ser atualizada separadamente; as outras colunas não são afetadas.

Para atualizar linhas existentes, use o comando [UPDATE](sql-update.md). Isso requer três informações:

1. O nome da tabela e da coluna a serem atualizados. 2. O novo valor da coluna. 3. Quais linhas (s) a serem atualizadas.

Lembre-se de que, de forma geral, o SQL não fornece um identificador único para as linhas. Portanto, nem sempre é possível especificar diretamente qual linha deve ser atualizada. Em vez disso, você especifica quais condições uma linha deve atender para ser atualizada. Somente se você tiver uma chave primária na tabela (independentemente de a ter declarado ou não) você pode endereçar de forma confiável as linhas individuais, escolhendo uma condição que corresponda à chave primária. As ferramentas de acesso gráfico ao banco de dados dependem desse fato para permitir que você atualize as linhas individualmente.

Por exemplo, este comando atualiza todos os produtos que têm um preço de 5 para ter um preço de 10:

```
UPDATE products SET price = 10 WHERE price = 5;
```

Isso pode causar a atualização de zero, uma ou várias linhas. Não é um erro tentar uma atualização que não corresponda a nenhuma linha.

Vamos analisar esse comando em detalhes. Primeiro está a palavra-chave `UPDATE`, seguida pelo nome da tabela. Como de costume, o nome da tabela pode ser qualificado pelo esquema, caso contrário, é buscado no caminho. Em seguida, está a palavra-chave `SET`, seguida pelo nome da coluna, um sinal de igual e o novo valor da coluna. O novo valor da coluna pode ser qualquer expressão escalar, não apenas uma constante. Por exemplo, se você quiser aumentar o preço de todos os produtos em 10%, você poderia usar:

```
UPDATE products SET price = price * 1.10;
```

Como você pode ver, a expressão para o novo valor pode se referir aos(s) valor(es) existente(s) na(s) linha(s). Também excluímos a cláusula `WHERE`. Se ela for omitida, isso significa que todas as linhas da tabela são atualizadas. Se ela estiver presente, apenas as linhas que correspondem à condição `WHERE` são atualizadas. Note que o sinal de igual na cláusula `SET` é uma atribuição, enquanto o da cláusula `WHERE` é uma comparação, mas isso não cria nenhuma ambiguidade. Claro, a condição `WHERE` não precisa ser um teste de igualdade. Muitos outros operadores estão disponíveis (consulte [Capítulo 9](functions.md)). Mas a expressão precisa avaliar a um resultado booleano.

Você pode atualizar mais de uma coluna em um comando `UPDATE` listando mais de uma atribuição na cláusula `SET`. Por exemplo:

```
UPDATE mytable SET a = 5, b = 3, c = 1 WHERE a > 0;
```
