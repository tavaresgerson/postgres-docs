### Capítulo 4. Sintaxe SQL

**Índice**

* [4.1. Estrutura Lexical](sql-syntax-lexical.md)
  + [4.1.1. Identificadores e Palavras-chave](sql-syntax-lexical.md#SQL-SYNTAX-IDENTIFIERS)
  + [4.1.2. Constantes](sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS)
  + [4.1.3. Operadores](sql-syntax-lexical.md#SQL-SYNTAX-OPERATORS)
  + [4.1.4. Caracteres Especiais](sql-syntax-lexical.md#SQL-SYNTAX-SPECIAL-CHARS)
  + [4.1.5. Comentários](sql-syntax-lexical.md#SQL-SYNTAX-COMMENTS)
  + [4.1.6. Precedência do Operador](sql-syntax-lexical.md#SQL-PRECEDENCE)
* [4.2. Expressões de Valor](sql-expressions.md)
  + [4.2.1. Referências de Coluna](sql-expressions.md#SQL-EXPRESSIONS-COLUMN-REFS)
  + [4.2.2. Parâmetros Posicionais](sql-expressions.md#SQL-EXPRESSIONS-PARAMETERS-POSITIONAL)
  + [4.2.3. Subíndices](sql-expressions.md#SQL-EXPRESSIONS-SUBSCRIPTS)
  + [4.2.4. Seleção de Campo](sql-expressions.md#FIELD-SELECTION)
  + [4.2.5. Invocações de Operadores](sql-expressions.md#SQL-EXPRESSIONS-OPERATOR-CALLS)
  + [4.2.6. Chamadas de Função](sql-expressions.md#SQL-EXPRESSIONS-FUNCTION-CALLS)
  + [4.2.7. Expressões Agregadas](sql-expressions.md#SYNTAX-AGGREGATES)
  + [4.2.8. Chamadas de Função de Janela](sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)
  + [4.2.9. Casts de Tipo](sql-expressions.md#SQL-SYNTAX-TYPE-CASTS)
  + [4.2.10. Expressões de Colaboração](sql-expressions.md#SQL-SYNTAX-COLLATE-EXPRS)
  + [4.2.11. Subconsultas Escalares](sql-expressions.md#SQL-SYNTAX-SCALAR-SUBQUERIES)
  + [4.2.12. Construtores de Array](sql-expressions.md#SQL-SYNTAX-ARRAY-CONSTRUCTORS)
  + [4.2.13. Construtores de Linha](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)
  + [4.2.14. Regras de Avaliação de Expressões](sql-expressions.md#SYNTAX-EXPRESS-EVAL)
* [4.3. Chamadas de Funções](sql-syntax-calling-funcs.md)
  + [4.3.1. Usando notação posicional](sql-syntax-calling-funcs.md#SQL-SYNTAX-CALLING-FUNCS-POSITIONAL)
  + [4.3.2. Usando notação nomeada](sql-syntax-calling-funcs.md#SQL-SYNTAX-CALLING-FUNCS-NAMED)
  + [4.3.3. Usando notação mista](sql-syntax-calling-funcs.md#SQL-SYNTAX-CALLING-FUNCS-MIXED)

Este capítulo descreve a sintaxe do SQL. Ele forma a base para entender os capítulos seguintes, que detalharão como os comandos SQL são aplicados para definir e modificar dados.

Também recomendamos que os usuários que já estão familiarizados com SQL leiam este capítulo com atenção, pois ele contém várias regras e conceitos que são implementados de forma inconsistente entre as bases de dados SQL ou que são específicos para o PostgreSQL.