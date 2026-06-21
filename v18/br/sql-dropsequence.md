## DROP SEQUENCE

DROP SEQUENCE — remova uma sequência

## Sinopse

```
DROP SEQUENCE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP SEQUENCE` remove os geradores de número de sequência. Uma sequência só pode ser descartada pelo seu proprietário ou por um superusuário.

## Parâmetros

`IF EXISTS`: Não exija erro se a sequência não existir. Neste caso, é emitido um aviso.

*`name`*: O nome (opcionalmente qualificado por esquema) de uma sequência.

`CASCADE`: Descarte automaticamente os objetos que dependem da sequência e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a interrupção da sequência se quaisquer objetos dependerem dela. Esse é o padrão.

## Exemplos

Para remover a sequência `serial`:

```
DROP SEQUENCE serial;
```

## Compatibilidade

`DROP SEQUENCE` está em conformidade com o padrão SQL, exceto pelo fato de que o padrão só permite que uma sequência seja descartada por comando, e, à parte a opção `IF EXISTS`, que é uma extensão do PostgreSQL.

## Veja também

[Crie Sequência](sql-createsequence.md "CREATE SEQUENCE"), [Altere Sequência](sql-altersequence.md "ALTER SEQUENCE")