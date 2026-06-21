## ALTER COLLATION

ALTER COLLATION — alterar a definição de uma correção de caracteres

## Sinopse

```
ALTER COLLATION name REFRESH VERSION

ALTER COLLATION name RENAME TO new_name
ALTER COLLATION name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER COLLATION name SET SCHEMA new_schema
```

## Descrição

`ALTER COLLATION` altera a definição de uma correção.

Você deve ser o proprietário da agregação para usar `ALTER COLLATION`. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter `CREATE` privilégio no esquema da agregação. (Essas restrições garantem que alterar o proprietário não faz nada que você não pudesse fazer ao descartar e recriar a agregação. No entanto, um superusuário pode alterar a propriedade de qualquer agregação de qualquer maneira.)

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de uma correção existente.

*`new_name`*: O novo nome da agregação.

*`new_owner`*: O novo proprietário da agregação.

*`new_schema`*: O novo esquema para a correção.

`REFRESH VERSION`: Atualize a versão da correção. Veja [Notas][(sql-altercollation.md#SQL-ALTERCOLLATION-NOTES "Notes")] abaixo.

## Notas

Quando um objeto de ordenação é criado, a versão específica do provedor da ordenação é registrada no catálogo do sistema. Quando a ordenação é usada, a versão atual é verificada em relação à versão registrada e um aviso é emitido quando há uma incompatibilidade, por exemplo:

```
WARNING:  collation "xx-x-icu" has version mismatch
DETAIL:  The collation in the database was created using version 1.2.3.4, but the operating system provides version 2.3.4.5.
HINT:  Rebuild all objects affected by this collation and run ALTER COLLATION pg_catalog."xx-x-icu" REFRESH VERSION, or build PostgreSQL with the right library version.
```

Uma mudança nas definições de ordenação pode levar a índices corrompidos e outros problemas, pois o sistema de banco de dados depende de objetos armazenados que tenham uma certa ordem de classificação. Geralmente, isso deve ser evitado, mas pode acontecer em circunstâncias legítimas, como quando se atualiza o sistema operacional para uma nova versão principal ou quando se usa `pg_upgrade` para atualizar binários de servidor vinculados a uma versão mais recente do ICU. Quando isso acontece, todos os objetos que dependem da ordenação devem ser reconstruídos, por exemplo, usando `REINDEX`. Quando isso é feito, a versão da ordenação pode ser atualizada usando o comando `ALTER COLLATION ... REFRESH VERSION`. Isso atualizará o catálogo do sistema para registrar a versão atual da ordenação e fará o aviso desaparecer. Note que isso não verifica se todos os objetos afetados foram reconstruídos corretamente.

Ao usar as codificações fornecidas por `libc`, as informações sobre a versão são registradas em sistemas que utilizam a biblioteca GNU C (a maioria dos sistemas Linux), FreeBSD e Windows. Ao usar as codificações fornecidas por ICU, as informações sobre a versão são fornecidas pela biblioteca ICU e estão disponíveis em todas as plataformas.

### Nota

Ao usar a biblioteca GNU C para colagens, a versão da biblioteca C é usada como um proxy para a versão da colagem. Muitas distribuições Linux alteram as definições de colagem apenas ao atualizar a biblioteca C, mas essa abordagem é imperfeita, pois os mantenedores têm liberdade para retropor definições de colagem mais recentes para versões mais antigas da biblioteca C.

Ao usar o Windows para colagens, as informações de versão estão disponíveis apenas para colagens definidas com etiquetas de idioma BCP 47, como `en-US`.

Para a collation padrão do banco de dados, há um comando análogo `ALTER DATABASE ... REFRESH COLLATION VERSION`.

A seguinte consulta pode ser usada para identificar todas as codificações no banco de dados atual que precisam ser atualizadas e os objetos que dependem delas:

```
SELECT pg_describe_object(refclassid, refobjid, refobjsubid) AS "Collation",
       pg_describe_object(classid, objid, objsubid) AS "Object"
  FROM pg_depend d JOIN pg_collation c
       ON refclassid = 'pg_collation'::regclass AND refobjid = c.oid
  WHERE c.collversion <> pg_collation_actual_version(c.oid)
  ORDER BY 1, 2;
```

## Exemplos

Para renomear a agregação `de_DE` para `german`:

```
ALTER COLLATION "de_DE" RENAME TO german;
```

Para alterar o proprietário da correção `en_US` para `joe`:

```
ALTER COLLATION "en_US" OWNER TO joe;
```

## Compatibilidade

Não há declaração `ALTER COLLATION` no padrão SQL.

## Veja também

[Crie a correlação](sql-createcollation.md "CREATE COLLATION"), [Retire a correlação](sql-dropcollation.md "DROP COLLATION")