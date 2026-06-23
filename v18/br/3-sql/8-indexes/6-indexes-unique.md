## 11.6. Índices Únicos [#](#INDEXES-UNIQUE)

Os índices também podem ser usados para impor a unicidade do valor de uma coluna ou a unicidade dos valores combinados de mais de uma coluna.

```
CREATE UNIQUE INDEX name ON table (column [, ...]) [ NULLS [ NOT ] DISTINCT ];
```

Atualmente, apenas índices de árvore B podem ser declarados como únicos.

Quando um índice é declarado como único, não é permitido que múltiplas linhas de tabela com valores indexados iguais sejam permitidas. Por padrão, valores nulos em uma coluna única não são considerados iguais, permitindo múltiplos nulos na coluna. A opção `NULLS NOT DISTINCT` modifica isso e faz com que o índice trate os nulos como iguais. Um índice único de múltiplas colunas só rejeitará casos em que todas as colunas indexadas são iguais em múltiplas linhas.

O PostgreSQL cria automaticamente um índice exclusivo quando uma restrição exclusiva ou chave primária é definida para uma tabela. O índice cobre as colunas que compõem a chave primária ou restrição exclusiva (um índice multicoluna, se apropriado) e é o mecanismo que impõe a restrição.

Nota

Não há necessidade de criar manualmente índices em colunas únicas; fazer isso apenas duplicaria o índice criado automaticamente.