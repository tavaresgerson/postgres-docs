## 21.4. Desfazer papéis [#](#ROLE-REMOVAL)

Como os papéis podem possuir objetos de banco de dados e podem ter privilégios para acessar outros objetos, a eliminação de um papel muitas vezes não é apenas uma questão de uma `DROP ROLE` rápida. Qualquer objeto possuído pelo papel deve ser eliminado ou reatribuído a outros proprietários; e quaisquer permissões concedidas ao papel devem ser revogadas.

A propriedade de objetos pode ser transferida uma de cada vez usando comandos `ALTER`, por exemplo:

```
ALTER TABLE bobs_table OWNER TO alice;
```

Como alternativa, o comando `REASSIGN OWNED`(sql-reassign-owned.md "REASSIGN OWNED") pode ser usado para reatribuir a propriedade de todos os objetos detidos pelo papel que será removido para um único outro papel. Como o `REASSIGN OWNED` não pode acessar objetos em outros bancos de dados, é necessário executá-lo em cada banco de dados que contém objetos detidos pelo papel. (Observe que o primeiro `REASSIGN OWNED` mudará a propriedade de quaisquer objetos compartilhados entre bancos de dados, ou seja, bancos de dados ou espaços de tabela, que são detidos pelo papel que será removido.)

Uma vez que quaisquer objetos valiosos tenham sido transferidos para novos proprietários, quaisquer objetos restantes detidos pelo papel que será descartado podem ser descartados com o comando `DROP OWNED`(sql-drop-owned.md "DROP OWNED"). Novamente, este comando não pode acessar objetos em outros bancos de dados, portanto, é necessário executá-lo em cada banco de dados que contenha objetos detidos pelo papel. Além disso, `DROP OWNED` não descartará bancos de dados ou espaços de tabelas inteiros, portanto, é necessário fazer isso manualmente se o papel possuir quaisquer bancos de dados ou espaços de tabelas que não tenham sido transferidos para novos proprietários.

`DROP OWNED` também cuida da remoção de quaisquer privilégios concedidos ao papel alvo para objetos que não lhe pertencem. Como `REASSIGN OWNED` não toca em tais objetos, é tipicamente necessário executar ambos `REASSIGN OWNED` e `DROP OWNED` (naquela ordem!) para remover completamente as dependências de um papel que será descartado.

Em suma, então, a receita mais geral para remover um papel que foi usado para possuir objetos é:

```
REASSIGN OWNED BY doomed_role TO successor_role;
DROP OWNED BY doomed_role;
-- repeat the above commands in each database of the cluster
DROP ROLE doomed_role;
```

Quando nem todos os objetos de propriedade devem ser transferidos para o mesmo proprietário sucessor, é melhor lidar com as exceções manualmente e, em seguida, realizar as etapas acima para limpar.

Se `DROP ROLE` for tentada enquanto objetos dependentes ainda permanecem, ela emitirá mensagens identificando quais objetos precisam ser realocados ou descartados.