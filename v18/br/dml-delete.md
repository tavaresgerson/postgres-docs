## 6.3. Excluindo Dados [#](#DML-DELETE)

Até agora, explicamos como adicionar dados às tabelas e como alterar os dados. O que resta é discutir como remover dados que não são mais necessários. Assim como adicionar dados é possível apenas em linhas inteiras, você só pode remover linhas inteiras de uma tabela. Na seção anterior, explicamos que o SQL não fornece uma maneira de abordar diretamente linhas individuais. Portanto, a remoção de linhas só pode ser feita especificando condições que as linhas a serem removidas devem corresponder. Se você tiver uma chave primária na tabela, você pode especificar a linha exata. Mas você também pode remover grupos de linhas que correspondem a uma condição, ou você pode remover todas as linhas da tabela de uma vez.

Você usa o comando [DELETE][(sql-delete.md "DELETE")] para remover linhas; a sintaxe é muito semelhante ao comando [UPDATE][(sql-update.md "UPDATE")]. Por exemplo, para remover todas as linhas da tabela de produtos que têm um preço de 10, use:

```
DELETE FROM products WHERE price = 10;
```

Se você simplesmente escrever:

```
DELETE FROM products;
```

então todas as linhas da tabela serão excluídas! Atenção ao programador.