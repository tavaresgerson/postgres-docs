## 22.5. Destruindo um banco de dados [#](#MANAGE-AG-DROPDB)

Os bancos de dados são destruídos com o comando [DROP DATABASE](sql-dropdatabase.md "DROP DATABASE"):

```
DROP DATABASE name;
```

Apenas o proprietário do banco de dados ou um superusuário pode descartar um banco de dados. O descarte de um banco de dados remove todos os objetos que estavam contidos dentro do banco de dados. A destruição de um banco de dados não pode ser desfeito.

Você não pode executar o comando `DROP DATABASE` enquanto estiver conectado ao banco de dados da vítima. No entanto, você pode estar conectado a qualquer outro banco de dados, incluindo o banco de dados `template1`. `template1` seria a única opção para descartar o último banco de dados do usuário de um determinado clúster.

Para conveniência, também há um programa de linha de comando para descartar bancos de dados, [dropdb][(app-dropdb.md "dropdb")]:

```
dropdb dbname
```

(Ao contrário de `createdb`, não é a ação padrão descartar o banco de dados com o nome do usuário atual.)