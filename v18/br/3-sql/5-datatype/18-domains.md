## 8.18. Tipos de domínio [#](#DOMAINS)

Um *domínio* é um tipo de dados definido pelo usuário que é baseado em outro *tipo subjacente*. Opcionalmente, ele pode ter restrições que restringem seus valores válidos a um subconjunto do que o tipo subjacente permitiria. Caso contrário, ele se comporta como o tipo subjacente — por exemplo, qualquer operador ou função que pode ser aplicada ao tipo subjacente funcionará no tipo de domínio. O tipo subjacente pode ser qualquer tipo de base embutido ou definido pelo usuário, tipo enum, tipo de matriz, tipo composto, tipo de intervalo ou outro domínio.

Por exemplo, poderíamos criar um domínio sobre inteiros que aceita apenas inteiros positivos:

```
CREATE DOMAIN posint AS integer CHECK (VALUE > 0);
CREATE TABLE mytable (id posint);
INSERT INTO mytable VALUES(1);   -- works
INSERT INTO mytable VALUES(-1);  -- fails
```

Quando um operador ou função do tipo subjacente é aplicada a um valor de domínio, o domínio é automaticamente convertido para o tipo subjacente. Assim, por exemplo, o resultado de `mytable.id - 1` é considerado do tipo `integer` e não `posint`. Podíamos escrever `(mytable.id - 1)::posint` para converter o resultado de volta para `posint`, causando a revalidação das restrições do domínio. Neste caso, isso resultaria em um erro se a expressão tivesse sido aplicada a um valor de `id` de

Para informações adicionais, consulte [CREATE DOMAIN](sql-createdomain.md "CREATE DOMAIN").