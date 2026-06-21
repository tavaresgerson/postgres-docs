## 36.9. Funções internas [#](#XFUNC-INTERNAL)

As funções internas são funções escritas em C que foram vinculadas estaticamente ao servidor PostgreSQL. O “corpo” da definição da função especifica o nome da função em linguagem C, que não precisa ser o mesmo que o nome declarado para uso SQL. (Por razões de compatibilidade reversa, um corpo vazio é aceito como significando que o nome da função em linguagem C é o mesmo que o nome SQL.)

Normalmente, todas as funções internas presentes no servidor são declaradas durante a inicialização do clúster de banco de dados (consulte [Seção 18.2][(creating-cluster.md "18.2. Creating a Database Cluster")]), mas um usuário pode usar `CREATE FUNCTION` para criar nomes de alias adicionais para uma função interna. As funções internas são declaradas em `CREATE FUNCTION` com o nome da linguagem `internal`. Por exemplo, para criar um alias para a função `sqrt`:

```
CREATE FUNCTION square_root(double precision) RETURNS double precision
    AS 'dsqrt'
    LANGUAGE internal
    STRICT;
```

(A maioria das funções internas espera ser declarada como “estricta”.

### Nota

Nem todas as funções "pré-definidas" são "internas" no sentido acima mencionado. Algumas funções pré-definidas são escritas em SQL.