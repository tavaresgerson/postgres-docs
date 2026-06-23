## Crie uma família de operadores

Crie uma família de operadores — defina uma nova família de operadores

## Sinopse

```
CREATE OPERATOR FAMILY name USING index_method
```

## Descrição

`CREATE OPERATOR FAMILY` cria uma nova família de operadores. Uma família de operadores define uma coleção de classes de operadores relacionadas, e talvez alguns operadores adicionais e funções de suporte que são compatíveis com essas classes de operadores, mas não essenciais para o funcionamento de qualquer índice. (Operadores e funções que são essenciais para índices devem ser agrupados dentro da classe de operador relevante, em vez de serem "soltos" na família de operadores. Tipicamente, os operadores de um único tipo de dado estão vinculados a classes de operadores, enquanto os operadores de vários tipos de dados podem ser soltos em uma família de operadores que contém classes de operadores para ambos os tipos de dados.)

A nova família de operadores é inicialmente vazia. Ela deve ser preenchida emitindo comandos subsequentes `CREATE OPERATOR CLASS` para adicionar classes de operadores contidas e, opcionalmente, comandos `ALTER OPERATOR FAMILY` para adicionar operadores "soltos" e suas funções de suporte correspondentes.

Se um nome de esquema for fornecido, a família de operadores é criada no esquema especificado. Caso contrário, ela é criada no esquema atual. Duas famílias de operadores no mesmo esquema podem ter o mesmo nome apenas se forem para métodos de índice diferentes.

O usuário que define uma família de operadores torna-se seu proprietário. Atualmente, o usuário que está criando deve ser um superusuário. (Essa restrição é feita porque uma definição errada de família de operadores pode confundir ou até mesmo fazer o servidor falhar.)

Consulte [Seção 36.16](xindex.md) para obter mais informações.

## Parâmetros

*`name`*: O nome da família de operadores a ser criada. O nome pode ser qualificado por esquema.

*`index_method`*: O nome do método de índice para o qual essa família de operadores é destinada.

## Compatibilidade

`CREATE OPERATOR FAMILY` é uma extensão do PostgreSQL. Não há uma declaração `CREATE OPERATOR FAMILY` no padrão SQL.

## Veja também

[ALTERAR FAMÍLIA DE OPERADORES](sql-alteropfamily.md "ALTER OPERATOR FAMILY"), [DROP FAMÍLIA DE OPERADORES](sql-dropopfamily.md "DROP OPERATOR FAMILY"), [CADASTRAR CLASSE DE OPERADORES](sql-createopclass.md "CREATE OPERATOR CLASS"), [ALTERAR CLASSE DE OPERADORES](sql-alteropclass.md "ALTER OPERATOR CLASS"), [DROP CLASSE DE OPERADORES](sql-dropopclass.md "DROP OPERATOR CLASS")