## Crie a Coligação

CREATE COLLATION — definir uma nova correção

## Sinopse

```
CREATE COLLATION [ IF NOT EXISTS ] name (
    [ LOCALE = locale, ]
    [ LC_COLLATE = lc_collate, ]
    [ LC_CTYPE = lc_ctype, ]
    [ PROVIDER = provider, ]
    [ DETERMINISTIC = boolean, ]
    [ RULES = rules, ]
    [ VERSION = version ]
)
CREATE COLLATION [ IF NOT EXISTS ] name FROM existing_collation
```

## Descrição

`CREATE COLLATION` define uma nova correção de texto usando as configurações do idioma do sistema operacional especificadas, ou copiando uma correção de texto existente.

Para criar uma correção, você deve ter o privilégio `CREATE` no esquema de destino.

## Parâmetros

`IF NOT EXISTS`: Não exija um erro se uma correção com o mesmo nome já existir. Um aviso é emitido neste caso. Observe que não há garantia de que a correção existente seja algo parecido com a que teria sido criada.

*`name`*: O nome da correção. O nome da correção pode ser qualificado pelo esquema. Se não for, a correção é definida no esquema atual. O nome da correção deve ser único dentro desse esquema. (Os catálogos do sistema podem conter correções com o mesmo nome para outros codificações, mas esses são ignorados se a codificação do banco de dados não corresponder.)

*`locale`*: O nome do local para esta correção. Consulte a [Seção 23.2.2.3.1][(collation.md#COLLATION-MANAGING-CREATE-LIBC "23.2.2.3.1. libc Collations")] e a [Seção 23.2.2.3.2][(collation.md#COLLATION-MANAGING-CREATE-ICU "23.2.2.3.2. ICU Collations")] para obter detalhes.

Se *`provider`* for `libc`, este é um atalho para definir `LC_COLLATE` e `LC_CTYPE` de uma vez. Se você especificar *`locale`*, não poderá especificar nenhum desses parâmetros.

Se *`provider`* for `builtin`, então *`locale`* deve ser especificado e definido como `C`, `C.UTF-8` ou `PG_UNICODE_FAST`.

*`lc_collate`*: Se *`provider`* é `libc`, use o local do sistema operacional especificado para a categoria de local `LC_COLLATE`.

*`lc_ctype`*: Se *`provider`* for `libc`, use o local do sistema operacional especificado para a categoria de local do `LC_CTYPE`.

*`provider`*: Especifica o provedor a ser usado para serviços de localização associados a esta codificação. Os valores possíveis são `builtin`, `icu` (se o servidor foi construído com suporte ao ICU) ou `libc`. `libc` é o padrão. Consulte [Seção 23.1.4][(locale.md#LOCALE-PROVIDERS "23.1.4. Locale Providers")] para detalhes.

`DETERMINISTIC`: Especifica se a correção de texto deve usar comparações determinísticas. O padrão é verdadeiro. Uma comparação determinística considera que cadeias que não são iguais em bytes são desiguais, mesmo que sejam consideradas logicamente iguais pela comparação. O PostgreSQL resolve os empates usando uma comparação em bytes. A comparação que não é determinística pode fazer com que a correção de texto seja, por exemplo, insensível ao caso ou ao acento. Para isso, você precisa escolher um ajuste apropriado `LOCALE` *e* definir a correção de texto como não determinística aqui.

As collation não determinísticas são suportadas apenas com o provedor ICU.

*`rules`*: Especifica regras adicionais de ordenação para personalizar o comportamento da ordenação. Isso é suportado apenas para ICU. Consulte [Seção 23.2.3.4][(collation.md#ICU-TAILORING-RULES "23.2.3.4. ICU Tailoring Rules")] para detalhes.

*`version`*: Especifica a string de versão a ser armazenada com a correção de texto. Normalmente, isso deve ser omitido, o que fará com que a versão seja calculada a partir da versão real da correção de texto fornecida pelo sistema operacional. Esta opção é destinada a ser usada por `pg_upgrade` para copiar a versão de uma instalação existente.

Veja também [ALTER COLLATION](sql-altercollation.md "ALTER COLLATION") para saber como lidar com desalinhamentos na versão da coligação.

*`existing_collation`*: O nome de uma correção existente para copiar. A nova correção terá as mesmas propriedades que a existente, mas será um objeto independente.

## Notas

`CREATE COLLATION` assume um bloqueio `SHARE ROW EXCLUSIVE`, que é auto-contraditório, no catálogo do sistema `pg_collation`, de modo que apenas um comando `CREATE COLLATION` pode ser executado de cada vez.

Use `DROP COLLATION` para remover colateções definidas pelo usuário.

Consulte a [Seção 23.2.2.3][(collation.md#COLLATION-CREATE "23.2.2.3. Creating New Collation Objects")] para obter mais informações sobre como criar colatões.

Ao usar o provedor de codificação de collation `libc`, o local deve ser aplicável à codificação atual do banco de dados. Consulte [CREATE DATABASE](sql-createdatabase.md "CREATE DATABASE") para as regras precisas.

## Exemplos

Para criar uma correção a partir do local do sistema operacional `fr_FR.utf8` (assumindo que o codificação atual do banco de dados é `UTF8`):

```
CREATE COLLATION french (locale = 'fr_FR.utf8');
```

Para criar uma ordenação usando o provedor ICU com o pedido de classificação do catálogo telefônico alemão:

```
CREATE COLLATION german_phonebook (provider = icu, locale = 'de-u-co-phonebk');
```

Para criar uma ordenação usando o provedor ICU, com base no idioma raiz ICU, com regras personalizadas:

```
CREATE COLLATION custom (provider = icu, locale = 'und', rules = '&V << w <<< W');
```

Veja [Seção 23.2.3.4][(collation.md#ICU-TAILORING-RULES "23.2.3.4. ICU Tailoring Rules")] para mais detalhes e exemplos sobre a sintaxe das regras.

Para criar uma correção a partir de uma correção existente:

```
CREATE COLLATION german FROM "de_DE";
```

Essa característica pode ser conveniente para poder usar nomes de ordenação independentes do sistema operacional em aplicativos.

## Compatibilidade

Há uma declaração `CREATE COLLATION` no padrão SQL, mas ela é limitada à cópia de uma collation existente. A sintaxe para criar uma nova collation é uma extensão do PostgreSQL.

## Veja também

[ALTERAR COLUNA DE ORDENAÇÃO](sql-altercollation.md "ALTER COLLATION"), [DROP COLUNA DE ORDENAÇÃO](sql-dropcollation.md "DROP COLLATION")