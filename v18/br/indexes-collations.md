## 11.11. Índices e Colagens [#](#INDEXES-COLLATIONS)

Um índice pode suportar apenas uma codificação por coluna de índice. Se várias codificações forem de interesse, podem ser necessários vários índices.

Considere essas declarações:

```
CREATE TABLE test1c (
    id integer,
    content varchar COLLATE "x"
);

CREATE INDEX test1c_content_index ON test1c (content);
```

O índice usa automaticamente a ordenação da coluna subjacente. Portanto, uma consulta do tipo

```
SELECT * FROM test1c WHERE content > constant;
```

pode usar o índice, porque a comparação usará, por padrão, a collation da coluna. No entanto, este índice não pode acelerar consultas que envolvam outra collation. Portanto, se as consultas do tipo, por exemplo,

```
SELECT * FROM test1c WHERE content > constant COLLATE "y";
```

também são de interesse, um índice adicional poderia ser criado que suporte a ordenação `"y"`, como este:

```
CREATE INDEX test1c_content_y_index ON test1c (content COLLATE "y");
```
