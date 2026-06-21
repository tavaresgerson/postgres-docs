## 5.7. Modificando tabelas [#](#DDL-ALTER)

* [5.7.1. Adicionar uma Coluna][(ddl-alter.md#DDL-ALTER-ADDING-A-COLUMN)]
* [5.7.2. Remover uma Coluna][(ddl-alter.md#DDL-ALTER-REMOVING-A-COLUMN)]
* [5.7.3. Adicionar uma Restrição][(ddl-alter.md#DDL-ALTER-ADDING-A-CONSTRAINT)]
* [5.7.4. Remover uma Restrição][(ddl-alter.md#DDL-ALTER-REMOVING-A-CONSTRAINT)]
* [5.7.5. Alterar o Valor Padrão de uma Coluna][(ddl-alter.md#DDL-ALTER-COLUMN-DEFAULT)]
* [5.7.6. Alterar o Tipo de Dados de uma Coluna][(ddl-alter.md#DDL-ALTER-COLUMN-TYPE)]
* [5.7.7. Renomear uma Coluna][(ddl-alter.md#DDL-ALTER-RENAMING-COLUMN)]
* [5.7.8. Renomear uma Tabela][(ddl-alter.md#DDL-ALTER-RENAMING-TABLE)]

Quando você cria uma tabela e percebe que cometeu um erro ou os requisitos da aplicação mudam, pode descartar a tabela e criá-la novamente. Mas essa não é uma opção conveniente se a tabela já estiver preenchida com dados ou se a tabela for referenciada por outros objetos do banco de dados (por exemplo, uma restrição de chave estrangeira). Portanto, o PostgreSQL fornece uma família de comandos para fazer modificações em tabelas existentes. Observe que isso é conceitualmente distinto de alterar os dados contidos na tabela: aqui estamos interessados em alterar a definição ou a estrutura da tabela.

Você pode:

* Adicionar colunas
* Remover colunas
* Adicionar restrições
* Remover restrições
* Alterar valores padrão
* Alterar tipos de dados das colunas
* Renomear colunas
* Renomear tabelas

Todas essas ações são realizadas usando o comando [ALTER TABLE][(sql-altertable.md "ALTER TABLE")], cuja página de referência contém detalhes além dos dados fornecidos aqui.

### 5.7.1. Adicionar uma coluna [#](#DDL-ALTER-ADDING-A-COLUMN)

Para adicionar uma coluna, use um comando como:

```
ALTER TABLE products ADD COLUMN description text;
```

A nova coluna é preenchida inicialmente com qualquer valor padrão fornecido (nulo se você não especificar uma cláusula `DEFAULT`).

### DICA

Adicionar uma coluna com um valor padrão constante não exige que cada linha da tabela seja atualizada quando a instrução `ALTER TABLE` for executada. Em vez disso, o valor padrão será retornado na próxima vez que a linha for acessada e aplicado quando a tabela for reescrita, tornando o `ALTER TABLE` muito rápido, mesmo em tabelas grandes.

Se o valor padrão for volátil (por exemplo, `clock_timestamp()`) cada linha precisará ser atualizada com o valor calculado no momento em que `ALTER TABLE` é executado. Para evitar uma operação de atualização potencialmente longa, especialmente se você pretende preencher a coluna com valores que não sejam padrão, pode ser preferível adicionar a coluna sem valor padrão, inserir os valores corretos usando `UPDATE` e, em seguida, adicionar qualquer valor padrão desejado, conforme descrito abaixo.

Você também pode definir restrições na coluna ao mesmo tempo, usando a sintaxe usual:

```
ALTER TABLE products ADD COLUMN description text CHECK (description <> '');
```

De fato, todas as opções que podem ser aplicadas a uma descrição de coluna em `CREATE TABLE` podem ser usadas aqui. No entanto, tenha em mente que o valor padrão deve satisfazer as restrições dadas, ou o `ADD` falhará. Alternativamente, você pode adicionar restrições mais tarde (veja abaixo) depois de preencher a nova coluna corretamente.

### 5.7.2. Remoção de uma coluna [#](#DDL-ALTER-REMOVING-A-COLUMN)

Para remover uma coluna, use um comando como:

```
ALTER TABLE products DROP COLUMN description;
```

Qualquer dado que estivesse na coluna desaparecerá. As restrições da tabela que envolvem a coluna também serão eliminadas. No entanto, se a coluna for referenciada por uma restrição de chave estrangeira de outra tabela, o PostgreSQL não eliminará silenciosamente essa restrição. Você pode autorizar a eliminação de tudo o que depende da coluna, adicionando `CASCADE`:

```
ALTER TABLE products DROP COLUMN description CASCADE;
```

Veja [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")] para uma descrição do mecanismo geral por trás disso.

### 5.7.3. Adicionar uma restrição [#](#DDL-ALTER-ADDING-A-CONSTRAINT)

Para adicionar uma restrição, é usada a sintaxe de restrição de tabela. Por exemplo:

```
ALTER TABLE products ADD CHECK (name <> '');
ALTER TABLE products ADD CONSTRAINT some_name UNIQUE (product_no);
ALTER TABLE products ADD FOREIGN KEY (product_group_id) REFERENCES product_groups;
```

Para adicionar uma restrição não nula, que normalmente não é escrita como uma restrição de tabela, esta sintaxe especial está disponível:

```
ALTER TABLE products ALTER COLUMN product_no SET NOT NULL;
```

Este comando não faz nada em silêncio se a coluna já tiver uma restrição de não nulo.

A restrição será verificada imediatamente, portanto, os dados da tabela devem satisfazer a restrição antes de poderem ser adicionados.

### 5.7.4. Remoção de uma Restrição [#](#DDL-ALTER-REMOVING-A-CONSTRAINT)

Para remover uma restrição, você precisa saber seu nome. Se você deu um nome, é fácil. Caso contrário, o sistema atribuiu um nome gerado, que você precisa descobrir. O comando psql `\d tablename` pode ser útil aqui; outras interfaces também podem fornecer uma maneira de inspecionar os detalhes da tabela. Então, o comando é:

```
ALTER TABLE products DROP CONSTRAINT some_name;
```

Assim como ao descartar uma coluna, você precisa adicionar `CASCADE` se quiser descartar uma restrição que algo mais dependa. Um exemplo é que uma restrição de chave estrangeira depende de uma restrição de chave única ou primária na(s) coluna(s) referenciada(s).

A sintaxe simplificada está disponível para descartar uma restrição não nula:

```
ALTER TABLE products ALTER COLUMN product_no DROP NOT NULL;
```

Isso reflete a sintaxe `SET NOT NULL` para adicionar uma restrição não nula. Este comando não fará nada em silêncio se a coluna não tiver uma restrição não nula. (Lembre-se de que uma coluna pode ter no máximo uma restrição não nula, então nunca é ambíguo qual restrição esse comando afeta.)

### 5.7.5. Alterar o valor padrão de uma coluna [#](#DDL-ALTER-COLUMN-DEFAULT)

Para definir um novo padrão para uma coluna, use um comando como:

```
ALTER TABLE products ALTER COLUMN price SET DEFAULT 7.77;
```

Observe que isso não afeta quaisquer linhas existentes na tabela, apenas altera o padrão para futuros comandos `INSERT`.

Para remover qualquer valor padrão, use:

```
ALTER TABLE products ALTER COLUMN price DROP DEFAULT;
```

Isso é efetivamente o mesmo que definir o padrão como nulo. Como consequência, não é um erro descartar um padrão onde não havia sido definido, porque o padrão é implicitamente o valor nulo.

### 5.7.6. Altering o Tipo de Dados de uma Coluna [#](#DDL-ALTER-COLUMN-TYPE)

Para converter uma coluna para um tipo de dados diferente, use um comando como:

```
ALTER TABLE products ALTER COLUMN price TYPE numeric(10,2);
```

Isso só será possível se cada entrada existente na coluna puder ser convertida para o novo tipo por meio de uma conversão implícita. Se for necessária uma conversão mais complexa, você pode adicionar uma cláusula `USING` que especifica como calcular os novos valores a partir dos antigos.

O PostgreSQL tentará converter o valor padrão da coluna (se houver) para o novo tipo, bem como quaisquer restrições que envolvam a coluna. Mas essas conversões podem falhar ou produzir resultados surpreendentes. É frequentemente melhor descartar quaisquer restrições na coluna antes de alterar seu tipo e, em seguida, adicionar restrições adequadamente modificadas posteriormente.

### 5.7.7. Renomear uma coluna [#](#DDL-ALTER-RENAMING-COLUMN)

Para renomear uma coluna:

```
ALTER TABLE products RENAME COLUMN product_no TO product_number;
```

### 5.7.8. Renomear uma tabela [#](#DDL-ALTER-RENAMING-TABLE)

Para renomear uma tabela:

```
ALTER TABLE products RENAME TO items;
```
