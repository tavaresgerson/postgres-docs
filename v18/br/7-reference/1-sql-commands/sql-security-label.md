## ETIQUETA DE SEGURANÇA

Etiqueta de segurança — definir ou alterar uma etiqueta de segurança aplicada a um objeto

## Sinopse

```
SECURITY LABEL [ FOR provider ] ON
{
  TABLE object_name |
  COLUMN table_name.column_name |
  AGGREGATE aggregate_name ( aggregate_signature ) |
  DATABASE object_name |
  DOMAIN object_name |
  EVENT TRIGGER object_name |
  FOREIGN TABLE object_name |
  FUNCTION function_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  LARGE OBJECT large_object_oid |
  MATERIALIZED VIEW object_name |
  [ PROCEDURAL ] LANGUAGE object_name |
  PROCEDURE procedure_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  PUBLICATION object_name |
  ROLE object_name |
  ROUTINE routine_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  SCHEMA object_name |
  SEQUENCE object_name |
  SUBSCRIPTION object_name |
  TABLESPACE object_name |
  TYPE object_name |
  VIEW object_name
} IS { string_literal | NULL }

where aggregate_signature is:

* |
[ argmode ] [ argname ] argtype [ , ... ] |
[ [ argmode ] [ argname ] argtype [ , ... ] ] ORDER BY [ argmode ] [ argname ] argtype [ , ... ]
```

## Descrição

`SECURITY LABEL` aplica uma etiqueta de segurança a um objeto de banco de dados. Um número arbitrário de etiquetas de segurança, uma por fornecedor de etiquetas, pode ser associado a um objeto de banco de dados dado. Os fornecedores de etiquetas são módulos carregáveis que se registram usando a função `register_label_provider`.

### Nota

`register_label_provider` não é uma função SQL; ela só pode ser chamada a partir de código C carregado no backend.

O fornecedor do rótulo determina se um rótulo dado é válido e se é permitido atribuir esse rótulo a um objeto dado. O significado de um rótulo dado também está a critério do fornecedor do rótulo. O PostgreSQL não estabelece restrições sobre se o fornecedor do rótulo deve interpretar as etiquetas de segurança ou como deve interpretá-las; ele simplesmente fornece um mecanismo para armazená-las. Na prática, essa facilidade é destinada a permitir a integração com sistemas de controle de acesso obrigatório (MAC) baseados em rótulos, como o SELinux. Esses sistemas tomam todas as decisões de controle de acesso com base em rótulos de objeto, em vez de conceitos tradicionais de controle de acesso discrecional (DAC), como usuários e grupos.

Você deve possuir o objeto do banco de dados para usar `SECURITY LABEL`.

## Parâmetros

*`object_name`* *`table_name.column_name`* *`aggregate_name`* *`function_name`* *`procedure_name`* *`routine_name`*: O nome do objeto que será rotulado. Os nomes dos objetos que residem em esquemas (tabelas, funções, etc.) podem ser qualificados por esquema.

*`provider`*: O nome do provedor com o qual este rótulo deve ser associado. O provedor nomeado deve ser carregado e deve consentir com a operação de rotulagem proposta. Se exatamente um provedor for carregado, o nome do provedor pode ser omitido por brevidade.

*`argmode`*: O modo de uma função, procedimento ou argumento agregado: `IN`, `OUT`, `INOUT` ou `VARIADIC`. Se omitido, o padrão é `IN`. Note que `SECURITY LABEL` não presta atenção na verdade em argumentos `OUT`, uma vez que apenas os argumentos de entrada são necessários para determinar a identidade da função. Portanto, é suficiente listar os argumentos `IN`, `INOUT` e `VARIADIC`.

*`argname`*: O nome de uma função, procedimento ou argumento agregado. Observe que `SECURITY LABEL` não presta atenção na verdade aos nomes dos argumentos, uma vez que apenas os tipos de dados dos argumentos são necessários para determinar a identidade da função.

*`argtype`*: O tipo de dados de uma função, procedimento ou argumento agregado.

*`large_object_oid`*: O OID do grande objeto.

`PROCEDURAL`: Esta é uma palavra de ruído.

*`string_literal`*: O novo ajuste do rótulo de segurança, escrito como um literal de string.

`NULL`: Escreva `NULL` para descartar a etiqueta de segurança.

## Exemplos

O exemplo a seguir mostra como o rótulo de segurança de uma tabela pode ser configurado ou alterado:

```
SECURITY LABEL FOR selinux ON TABLE mytable IS 'system_u:object_r:sepgsql_table_t:s0';
```

Para remover a etiqueta:

```
SECURITY LABEL FOR selinux ON TABLE mytable IS NULL;
```

## Compatibilidade

Não existe comando `SECURITY LABEL` no padrão SQL.

## Veja também

[sepgsql](sepgsql.md "F.40. sepgsql — SELinux-, label-based mandatory access control (MAC) módulo de segurança"), `src/test/modules/dummy_seclabel`