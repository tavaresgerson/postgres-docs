## 23.3. Suporte a conjuntos de caracteres [#](#MULTIBYTE)

* [23.3.1. Conjuntos de Caracteres Suportado][(multibyte.md#MULTIBYTE-CHARSET-SUPPORTED)
* [23.3.2. Configuração do Conjunto de Caracteres][(multibyte.md#MULTIBYTE-SETTING)
* [23.3.3. Conversão Automática de Conjunto de Caracteres Entre o Servidor e o Cliente][(multibyte.md#MULTIBYTE-AUTOMATIC-CONVERSION)
* [23.3.4. Conversões de Conjuntos de Caracteres Disponíveis][(multibyte.md#MULTIBYTE-CONVERSIONS-SUPPORTED)
* [23.3.5. Leitura Adicional][(multibyte.md#MULTIBYTE-FURTHER-READING)

O suporte a conjuntos de caracteres no PostgreSQL permite que você armazene texto em uma variedade de conjuntos de caracteres (também chamados codificações), incluindo conjuntos de caracteres de único byte, como a série ISO 8859, e conjuntos de caracteres de múltiplos bytes, como EUC (Código Unix estendido), UTF-8 e código interno Mule. Todos os conjuntos de caracteres suportados podem ser usados de forma transparente pelos clientes, mas alguns não são suportados para uso no servidor (ou seja, como codificação do lado do servidor). O conjunto de caracteres padrão é selecionado ao inicializar seu clúster de banco de dados PostgreSQL usando `initdb`. Ele pode ser sobrescrito ao criar um banco de dados, para que você possa ter vários bancos, cada um com um conjunto de caracteres diferente.

Uma restrição importante, no entanto, é que o conjunto de caracteres de cada banco de dados deve ser compatível com as configurações de `LC_CTYPE` (classificação de caracteres) e `LC_COLLATE` (ordem de classificação de strings) do banco de dados. Para os locais `C` ou `POSIX`, qualquer conjunto de caracteres é permitido, mas para outros locais fornecidos pela libc, há apenas um conjunto de caracteres que funcionará corretamente. (No entanto, em Windows, a codificação UTF-8 pode ser usada com qualquer local.) Se você tiver suporte para ICU configurado, locais fornecidos pelo ICU podem ser usados com a maioria, mas não com todas, as codificações do lado do servidor.

### 23.3.1. Conjuntos de caracteres suportados [#](#MULTIBYTE-CHARSET-SUPPORTED)

[Tabela 23.3] (multibyte.md#CHARSET-TABLE "Table 23.3. PostgreSQL Character Sets") mostra os conjuntos de caracteres disponíveis para uso no PostgreSQL.

**Tabela 23.3. Conjuntos de caracteres do PostgreSQL**



<table border="1" class="table" summary="PostgreSQL Character Sets">
<colgroup>
<col class="col1"/>
<col class="col2"/>
<col class="col3"/>
<col class="col4"/>
<col class="col5"/>
<col class="col6"/>
<col class="col7"/>
</colgroup>
<thead>
<tr>
<th>
    Name
   </th>
<th>Descrição</th>
<th>
    Language
   </th>
<th>
    Server?
   </th>
<th>
    ICU?
   </th>
<th>
    Bytes/​Char
   </th>
<th>
    Aliases
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     BIG5
    </code>
</td>
<td>Cinco Grandes</td>
<td>
    Traditional Chinese
   </td>
<td>
    No
   </td>
<td>
    No
   </td>
<td>
    1–2
   </td>
<td>
<code class="literal">
     WIN950
    </code>
    ,
    <code class="literal">
     Windows950
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     EUC_CN
    </code>
</td>
<td>Código de UNIX estendido-CN</td>
<td>
    Simplified Chinese
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1–3
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     EUC_JP
    </code>
</td>
<td>Código UNIX estendido-JP</td>
<td>
    Japanese
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1–3
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     EUC_JIS_2004
    </code>
</td>
<td>Código estendido UNIX-JP, JIS X 0213</td>
<td>
    Japanese
   </td>
<td>
    Yes
   </td>
<td>
    No
   </td>
<td>
    1–3
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     EUC_KR
    </code>
</td>
<td>Código de UNIX estendido - KR</td>
<td>
    Korean
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1–3
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     EUC_TW
    </code>
</td>
<td>Código de UNIX estendido-TW</td>
<td>
    Traditional Chinese, Taiwanese
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1–4
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     GB18030
    </code>
</td>
<td>Padrão Nacional</td>
<td>
    Chinese
   </td>
<td>
    No
   </td>
<td>
    No
   </td>
<td>
    1–4
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     GBK
    </code>
</td>
<td>Padrão Nacional Ampliado</td>
<td>
    Simplified Chinese
   </td>
<td>
    No
   </td>
<td>
    No
   </td>
<td>
    1–2
   </td>
<td>
<code class="literal">
     WIN936
    </code>
    ,
    <code class="literal">
     Windows936
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     ISO_8859_5
    </code>
</td>
<td>ISO 8859-5,<acronym class="acronym">ECMA</acronym>113</td>
<td>
    Latin/Cyrillic
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     ISO_8859_6
    </code>
</td>
<td>ISO 8859-6,<acronym class="acronym">ECMA</acronym>114</td>
<td>
    Latin/Arabic
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     ISO_8859_7
    </code>
</td>
<td>ISO 8859-7,<acronym class="acronym">ECMA</acronym>118</td>
<td>
    Latin/Greek
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     ISO_8859_8
    </code>
</td>
<td>ISO 8859-8,<acronym class="acronym">ECMA</acronym>121</td>
<td>
    Latin/Hebrew
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     JOHAB
    </code>
</td>
<td>
<acronym class="acronym">JOHAB</acronym>
</td>
<td>
    Korean (Hangul)
   </td>
<td>
    No
   </td>
<td>
    No
   </td>
<td>
    1–3
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     KOI8R
    </code>
</td>
<td>
<acronym class="acronym">KOI</acronym>8-R</td>
<td>
    Cyrillic (Russian)
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     KOI8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     KOI8U
    </code>
</td>
<td>
<acronym class="acronym">KOI</acronym>8-U</td>
<td>
    Cyrillic (Ukrainian)
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN1
    </code>
</td>
<td>ISO 8859-1,<acronym class="acronym">ECMA</acronym>94</td>
<td>
    Western European
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     ISO88591
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN2
    </code>
</td>
<td>ISO 8859-2,<acronym class="acronym">ECMA</acronym>94</td>
<td>
    Central European
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     ISO88592
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN3
    </code>
</td>
<td>ISO 8859-3,<acronym class="acronym">ECMA</acronym>94</td>
<td>
    South European
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     ISO88593
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN4
    </code>
</td>
<td>ISO 8859-4,<acronym class="acronym">ECMA</acronym>94</td>
<td>
    North European
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     ISO88594
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN5
    </code>
</td>
<td>ISO 8859-9,<acronym class="acronym">ECMA</acronym>128</td>
<td>
    Turkish
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     ISO88599
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN6
    </code>
</td>
<td>ISO 8859-10,<acronym class="acronym">ECMA</acronym>144</td>
<td>
    Nordic
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     ISO885910
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN7
    </code>
</td>
<td>ISO 8859-13</td>
<td>
    Baltic
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     ISO885913
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN8
    </code>
</td>
<td>ISO 8859-14</td>
<td>
    Celtic
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     ISO885914
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN9
    </code>
</td>
<td>ISO 8859-15</td>
<td>
    LATIN1 with Euro and accents
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     ISO885915
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN10
    </code>
</td>
<td>ISO 8859-16,<acronym class="acronym">ASRO</acronym>SR 14111</td>
<td>
    Romanian
   </td>
<td>
    Yes
   </td>
<td>
    No
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     ISO885916
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>Código interno do mulle</td>
<td>
    Multilingual Emacs
   </td>
<td>
    Yes
   </td>
<td>
    No
   </td>
<td>
    1–4
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     SJIS
    </code>
</td>
<td>Shift JIS</td>
<td>
    Japanese
   </td>
<td>
    No
   </td>
<td>
    No
   </td>
<td>
    1–2
   </td>
<td>
<code class="literal">
     Mskanji
    </code>
    ,
    <code class="literal">
     ShiftJIS
    </code>
    ,
    <code class="literal">
     WIN932
    </code>
    ,
    <code class="literal">
     Windows932
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     SHIFT_JIS_2004
    </code>
</td>
<td>Shift JIS, JIS X 0213</td>
<td>
    Japanese
   </td>
<td>
    No
   </td>
<td>
    No
   </td>
<td>
    1–2
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     SQL_ASCII
    </code>
</td>
<td>não especificado (ver texto)</td>
<td>
<span class="emphasis">
<em>
      any
     </em>
</span>
</td>
<td>
    Yes
   </td>
<td>
    No
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     UHC
    </code>
</td>
<td>Código Unificado de Hangul</td>
<td>
    Korean
   </td>
<td>
    No
   </td>
<td>
    No
   </td>
<td>
    1–2
   </td>
<td>
<code class="literal">
     WIN949
    </code>
    ,
    <code class="literal">
     Windows949
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>Unicode, 8-bit</td>
<td>
<span class="emphasis">
<em>
      all
     </em>
</span>
</td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1–4
   </td>
<td>
<code class="literal">
     Unicode
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN866
    </code>
</td>
<td>Windows CP866</td>
<td>
    Cyrillic
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     ALT
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN874
    </code>
</td>
<td>Windows CP874</td>
<td>
    Thai
   </td>
<td>
    Yes
   </td>
<td>
    No
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1250
    </code>
</td>
<td>Windows CP1250</td>
<td>
    Central European
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1251
    </code>
</td>
<td>Windows CP1251</td>
<td>
    Cyrillic
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     WIN
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1252
    </code>
</td>
<td>Windows CP1252</td>
<td>
    Western European
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1253
    </code>
</td>
<td>Windows CP1253</td>
<td>
    Greek
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1254
    </code>
</td>
<td>Windows CP1254</td>
<td>
    Turkish
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1255
    </code>
</td>
<td>Windows CP1255</td>
<td>
    Hebrew
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1256
    </code>
</td>
<td>Windows CP1256</td>
<td>
    Arabic
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1257
    </code>
</td>
<td>Windows CP1257</td>
<td>
    Baltic
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1258
    </code>
</td>
<td>Windows CP1258</td>
<td>
    Vietnamese
   </td>
<td>
    Yes
   </td>
<td>
    Yes
   </td>
<td>
    1
   </td>
<td>
<code class="literal">
     ABC
    </code>
    ,
    <code class="literal">
     TCVN
    </code>
    ,
    <code class="literal">
     TCVN5712
    </code>
    ,
    <code class="literal">
     VSCII
    </code>
</td>
</tr>
</tbody>
</table>




  

Nem todas as APIs do cliente suportam todos os conjuntos de caracteres listados. Por exemplo, o driver JDBC do PostgreSQL não suporta `MULE_INTERNAL`, `LATIN6`, `LATIN8` e `LATIN10`.

O ajuste `SQL_ASCII` se comporta de maneira consideravelmente diferente dos outros ajustes. Quando o conjunto de caracteres do servidor é `SQL_ASCII`, o servidor interpreta os valores de byte 0–127 de acordo com o padrão ASCII, enquanto os valores de byte 128–255 são considerados caracteres não interpretados. Não haverá conversão de codificação quando o ajuste for `SQL_ASCII`. Assim, este ajuste não é tanto uma declaração de que uma codificação específica está sendo usada, quanto uma declaração de ignorância sobre a codificação. Na maioria dos casos, se você estiver trabalhando com algum dado não ASCII, não é prudente usar o ajuste `SQL_ASCII`, pois o PostgreSQL não poderá ajudá-lo a converter ou validar caracteres não ASCII.

### 23.3.2. Configuração do Conjunto de Caracteres [#](#MULTIBYTE-SETTING)

`initdb` define o conjunto de caracteres padrão (codificação) para um clúster PostgreSQL. Por exemplo,

```
initdb -E EUC_JP
```

define o conjunto de caracteres padrão para `EUC_JP` (Código Unix estendido para japonês). Você pode usar `--encoding` em vez de `-E` se preferir strings de opção mais longas. Se não for fornecida nenhuma opção de `-E` ou `--encoding`, `initdb` tenta determinar o codificação apropriada a ser usada com base no local especificado ou padrão.

Você pode especificar uma codificação não padrão no momento da criação do banco de dados, desde que a codificação seja compatível com o local selecionado:

```
createdb -E EUC_KR -T template0 --lc-collate=ko_KR.euckr --lc-ctype=ko_KR.euckr korean
```

Isso criará um banco de dados denominado `korean` que utiliza o conjunto de caracteres `EUC_KR` e o local `ko_KR`. Outra maneira de realizar isso é usar este comando SQL:

```
CREATE DATABASE korean WITH ENCODING 'EUC_KR' LC_COLLATE='ko_KR.euckr' LC_CTYPE='ko_KR.euckr' TEMPLATE=template0;
```

Observe que os comandos acima especificam a cópia do banco de dados `template0`. Ao copiar qualquer outro banco de dados, as configurações de codificação e local não podem ser alteradas daqueles do banco de dados de origem, porque isso pode resultar em dados corrompidos. Para mais informações, consulte [Seção 22.3][(manage-ag-templatedbs.md "22.3. Template Databases")].

O codificação para um banco de dados é armazenado no catálogo do sistema `pg_database`. Você pode vê-lo usando a opção `psql` `-l` ou o comando `\l`.

```
$ psql -l
                                         List of databases
   Name    |  Owner   | Encoding  |  Collation  |    Ctype    |          Access Privileges
-----------+----------+-----------+-------------+-------------+-------------------------------------
 clocaledb | hlinnaka | SQL_ASCII | C           | C           |
 englishdb | hlinnaka | UTF8      | en_GB.UTF8  | en_GB.UTF8  |
 japanese  | hlinnaka | UTF8      | ja_JP.UTF8  | ja_JP.UTF8  |
 korean    | hlinnaka | EUC_KR    | ko_KR.euckr | ko_KR.euckr |
 postgres  | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  |
 template0 | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  | {=c/hlinnaka,hlinnaka=CTc/hlinnaka}
 template1 | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  | {=c/hlinnaka,hlinnaka=CTc/hlinnaka}
(7 rows)
```

### Importante

Na maioria dos sistemas operacionais modernos, o PostgreSQL pode determinar qual conjunto de caracteres é implícito pelo ajuste `LC_CTYPE`, e ele aplicará que apenas o codificação do banco de dados correspondente é usada. Em sistemas mais antigos, é sua responsabilidade garantir que você use o codificação esperada pelo local que você selecionou. Um erro nessa área provavelmente levará a comportamentos estranhos de operações dependentes do local, como a ordenação.

O PostgreSQL permitirá que os superusuários criem bancos de dados com codificação `SQL_ASCII` mesmo quando `LC_CTYPE` não é `C` ou `POSIX`. Como mencionado acima, `SQL_ASCII` não exige que os dados armazenados no banco de dados tenham uma codificação específica, e, portanto, essa escolha apresenta riscos de comportamento dependente do local. O uso dessa combinação de configurações é desaconselhável e pode ser proibido completamente em algum momento.

### 23.3.3. Conversão automática de conjunto de caracteres entre servidor e cliente [#](#MULTIBYTE-AUTOMATIC-CONVERSION)

O PostgreSQL suporta conversão automática de conjunto de caracteres entre servidor e cliente para muitas combinações de conjuntos de caracteres ([Seção 23.3.4] [(multibyte.md#MULTIBYTE-CONVERSIONS-SUPPORTED "23.3.4. Available Character Set Conversions")] mostra quais são).

Para habilitar a conversão automática do conjunto de caracteres, você precisa informar ao PostgreSQL o conjunto de caracteres (codificação) que você gostaria de usar no cliente. Existem várias maneiras de realizar isso:

* Usando o comando `\encoding` no psql. `\encoding` permite que você mude o codificação do cliente em tempo real. Por exemplo, para mudar a codificação para `SJIS`, digite:

```
  \encoding SJIS
  ``` * A libpq ([Seção 32.11](libpq-control.md "32.11. Control Functions")) possui funções para controlar o codificação do cliente. * Usando `SET client_encoding TO`. A definição da codificação do cliente pode ser feita com este comando SQL:

  ```
  SET CLIENT_ENCODING TO 'value';
  ```

Você também pode usar a sintaxe SQL padrão `SET NAMES` para esse propósito:

  ```
  SET NAMES 'value';
  ```

Para consultar o codificação atual do cliente:

  ```
  SHOW client_encoding;
  ```

Para retornar ao codificação padrão:

```
  RESET client_encoding;
  ``` * Usando `PGCLIENTENCODING`. Se a variável de ambiente `PGCLIENTENCODING` estiver definida no ambiente do cliente, essa codificação do cliente é selecionada automaticamente quando uma conexão com o servidor é feita. (Isso pode ser posteriormente sobrescrito usando qualquer um dos outros métodos mencionados acima.) * Usando a variável de configuração [client_encoding](runtime-config-client.md#GUC-CLIENT-ENCODING). Se a variável `client_encoding` estiver definida, essa codificação do cliente é selecionada automaticamente quando uma conexão com o servidor é feita. (Isso pode ser posteriormente sobrescrito usando qualquer um dos outros métodos mencionados acima.)

Se a conversão de um caractere específico não for possível — suponha que você escolheu `EUC_JP` para o servidor e `LATIN1` para o cliente, e alguns caracteres japoneses são retornados que não têm representação em `LATIN1` — um erro é relatado.

Se o conjunto de caracteres do cliente for definido como `SQL_ASCII`, a conversão de codificação é desativada, independentemente do conjunto de caracteres do servidor. (No entanto, se o conjunto de caracteres do servidor não for `SQL_ASCII`, o servidor ainda verificará se os dados recebidos são válidos para essa codificação; portanto, o efeito líquido é como se o conjunto de caracteres do cliente fosse o mesmo que o do servidor.) Assim como para o servidor, o uso de `SQL_ASCII` é imprudente, a menos que você esteja trabalhando com dados ASCII completos.

### 23.3.4. Conversões de conjuntos de caracteres disponíveis [#](#MULTIBYTE-CONVERSIONS-SUPPORTED)

O PostgreSQL permite a conversão entre qualquer dois conjuntos de caracteres para os quais uma função de conversão está listada no catálogo do sistema `pg_conversion`(catalog-pg-conversion.md "52.14. pg_conversion"). O PostgreSQL vem com algumas conversões predefinidas, resumidas na [Tabela 23.4](multibyte.md#MULTIBYTE-TRANSLATION-TABLE "Table 23.4. Built-in Client/Server Character Set Conversions") e mostradas com mais detalhes na [Tabela 23.5](multibyte.md#BUILTIN-CONVERSIONS-TABLE "Table 23.5. All Built-in Character Set Conversions"). Você pode criar uma nova conversão usando o comando SQL [CREATE CONVERSION](sql-createconversion.md "CREATE CONVERSION"). (Para ser usado para conversões automáticas cliente/servidor, uma conversão deve ser marcada como “padrão” para seu par de conjuntos de caracteres.)

**Tabela 23.4. Conversões de conjuntos de caracteres de cliente/servidor integrados**



<table border="1" class="table" summary="Built-in Client/Server Character Set Conversions">
<colgroup>
<col class="col1"/>
<col class="col2"/>
</colgroup>
<thead>
<tr>
<th>
    Server Character Set
   </th>
<th>Conjunto de caracteres disponíveis para o cliente</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     BIG5
    </code>
</td>
<td>
<span class="emphasis">
<em>não é suportado como codificação de servidor</em>
</span>
</td>
</tr>
<tr>
<td>
<code class="literal">
     EUC_CN
    </code>
</td>
<td>
<span class="emphasis">
<em>
      EUC_CN
     </em>
</span>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     EUC_JP
    </code>
</td>
<td>
<span class="emphasis">
<em>
      EUC_JP
     </em>
</span>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     SJIS
    </code>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     EUC_JIS_2004
    </code>
</td>
<td>
<span class="emphasis">
<em>
      EUC_JIS_2004
     </em>
</span>,<code class="literal">
     SHIFT_JIS_2004
    </code>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     EUC_KR
    </code>
</td>
<td>
<span class="emphasis">
<em>
      EUC_KR
     </em>
</span>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     EUC_TW
    </code>
</td>
<td>
<span class="emphasis">
<em>
      EUC_TW
     </em>
</span>,<code class="literal">
     BIG5
    </code>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     GB18030
    </code>
</td>
<td>
<span class="emphasis">
<em>não é suportado como codificação de servidor</em>
</span>
</td>
</tr>
<tr>
<td>
<code class="literal">
     GBK
    </code>
</td>
<td>
<span class="emphasis">
<em>não é suportado como codificação de servidor</em>
</span>
</td>
</tr>
<tr>
<td>
<code class="literal">
     ISO_8859_5
    </code>
</td>
<td>
<span class="emphasis">
<em>
      ISO_8859_5
     </em>
</span>,<code class="literal">
     KOI8R
    </code>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     UTF8
    </code>,<code class="literal">
     WIN866
    </code>,<code class="literal">
     WIN1251
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     ISO_8859_6
    </code>
</td>
<td>
<span class="emphasis">
<em>
      ISO_8859_6
     </em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     ISO_8859_7
    </code>
</td>
<td>
<span class="emphasis">
<em>
      ISO_8859_7
     </em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     ISO_8859_8
    </code>
</td>
<td>
<span class="emphasis">
<em>
      ISO_8859_8
     </em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     JOHAB
    </code>
</td>
<td>
<span class="emphasis">
<em>não é suportado como codificação de servidor</em>
</span>
</td>
</tr>
<tr>
<td>
<code class="literal">
     KOI8R
    </code>
</td>
<td>
<span class="emphasis">
<em>KOI8R</em>
</span>,<code class="literal">
     ISO_8859_5
    </code>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     UTF8
    </code>,<code class="literal">
     WIN866
    </code>,<code class="literal">
     WIN1251
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     KOI8U
    </code>
</td>
<td>
<span class="emphasis">
<em>KOI8U</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN1
    </code>
</td>
<td>
<span class="emphasis">
<em>LATINO1</em>
</span>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN2
    </code>
</td>
<td>
<span class="emphasis">
<em>LATINO2</em>
</span>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     UTF8
    </code>,<code class="literal">
     WIN1250
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN3
    </code>
</td>
<td>
<span class="emphasis">
<em>LATINO3</em>
</span>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN4
    </code>
</td>
<td>
<span class="emphasis">
<em>LATINO4</em>
</span>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN5
    </code>
</td>
<td>
<span class="emphasis">
<em>LATINO5</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN6
    </code>
</td>
<td>
<span class="emphasis">
<em>LATINO6</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN7
    </code>
</td>
<td>
<span class="emphasis">
<em>LATINO7</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN8
    </code>
</td>
<td>
<span class="emphasis">
<em>LATINO8</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN9
    </code>
</td>
<td>
<span class="emphasis">
<em>LATINO9</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     LATIN10
    </code>
</td>
<td>
<span class="emphasis">
<em>LATIN10</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<span class="emphasis">
<em>
      MULE_INTERNAL
     </em>
</span>,<code class="literal">
     BIG5
    </code>,<code class="literal">
     EUC_CN
    </code>,<code class="literal">
     EUC_JP
    </code>,<code class="literal">
     EUC_KR
    </code>,<code class="literal">
     EUC_TW
    </code>,<code class="literal">
     ISO_8859_5
    </code>,<code class="literal">
     KOI8R
    </code>,<code class="literal">
     LATIN1
    </code>para<code class="literal">
     LATIN4
    </code>,<code class="literal">
     SJIS
    </code>,<code class="literal">
     WIN866
    </code>,<code class="literal">
     WIN1250
    </code>,<code class="literal">
     WIN1251
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     SJIS
    </code>
</td>
<td>
<span class="emphasis">
<em>não é suportado como codificação de servidor</em>
</span>
</td>
</tr>
<tr>
<td>
<code class="literal">
     SHIFT_JIS_2004
    </code>
</td>
<td>
<span class="emphasis">
<em>não é suportado como codificação de servidor</em>
</span>
</td>
</tr>
<tr>
<td>
<code class="literal">
     SQL_ASCII
    </code>
</td>
<td>
<span class="emphasis">
<em>qualquer (não haverá nenhuma conversão)</em>
</span>
</td>
</tr>
<tr>
<td>
<code class="literal">
     UHC
    </code>
</td>
<td>
<span class="emphasis">
<em>não é suportado como codificação de servidor</em>
</span>
</td>
</tr>
<tr>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<span class="emphasis">
<em>todos os codificações suportados</em>
</span>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN866
    </code>
</td>
<td>
<span class="emphasis">
<em>WIN866</em>
</span>,<code class="literal">
     ISO_8859_5
    </code>,<code class="literal">
     KOI8R
    </code>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     UTF8
    </code>,<code class="literal">
     WIN1251
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN874
    </code>
</td>
<td>
<span class="emphasis">
<em>WIN874</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1250
    </code>
</td>
<td>
<span class="emphasis">
<em>WIN1250</em>
</span>,<code class="literal">
     LATIN2
    </code>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1251
    </code>
</td>
<td>
<span class="emphasis">
<em>WIN1251</em>
</span>,<code class="literal">
     ISO_8859_5
    </code>,<code class="literal">
     KOI8R
    </code>,<code class="literal">
     MULE_INTERNAL
    </code>,<code class="literal">
     UTF8
    </code>,<code class="literal">
     WIN866
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1252
    </code>
</td>
<td>
<span class="emphasis">
<em>WIN1252</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1253
    </code>
</td>
<td>
<span class="emphasis">
<em>WIN1253</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1254
    </code>
</td>
<td>
<span class="emphasis">
<em>WIN1254</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1255
    </code>
</td>
<td>
<span class="emphasis">
<em>WIN1255</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1256
    </code>
</td>
<td>
<span class="emphasis">
<em>WIN1256</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1257
    </code>
</td>
<td>
<span class="emphasis">
<em>WIN1257</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     WIN1258
    </code>
</td>
<td>
<span class="emphasis">
<em>WIN1258</em>
</span>,<code class="literal">
     UTF8
    </code>
</td>
</tr>
</tbody>
</table>




  

**Tabela 23.5. Todas as conversões de conjunto de caracteres embutido**



<table border="1" class="table" summary="All Built-in Character Set Conversions">
<colgroup>
<col class="col1"/>
<col class="col2"/>
<col class="col3"/>
</colgroup>
<thead>
<tr>
<th>
    Conversion Name
    <a class="footnote" href="#ftn.id-1.6.10.5.8.4.2.4.1.1.1">
<sup class="footnote" id="id-1.6.10.5.8.4.2.4.1.1.1">
      [a]
     </sup>
</a>
</th>
<th>
    Source Encoding
   </th>
<th>
    Destination Encoding
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     big5_to_euc_tw
    </code>
</td>
<td>
<code class="literal">
     BIG5
    </code>
</td>
<td>
<code class="literal">
     EUC_TW
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     big5_to_mic
    </code>
</td>
<td>
<code class="literal">
     BIG5
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     big5_to_utf8
    </code>
</td>
<td>
<code class="literal">
     BIG5
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     euc_cn_to_mic
    </code>
</td>
<td>
<code class="literal">
     EUC_CN
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     euc_cn_to_utf8
    </code>
</td>
<td>
<code class="literal">
     EUC_CN
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     euc_jp_to_mic
    </code>
</td>
<td>
<code class="literal">
     EUC_JP
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     euc_jp_to_sjis
    </code>
</td>
<td>
<code class="literal">
     EUC_JP
    </code>
</td>
<td>
<code class="literal">
     SJIS
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     euc_jp_to_utf8
    </code>
</td>
<td>
<code class="literal">
     EUC_JP
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     euc_kr_to_mic
    </code>
</td>
<td>
<code class="literal">
     EUC_KR
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     euc_kr_to_utf8
    </code>
</td>
<td>
<code class="literal">
     EUC_KR
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     euc_tw_to_big5
    </code>
</td>
<td>
<code class="literal">
     EUC_TW
    </code>
</td>
<td>
<code class="literal">
     BIG5
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     euc_tw_to_mic
    </code>
</td>
<td>
<code class="literal">
     EUC_TW
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     euc_tw_to_utf8
    </code>
</td>
<td>
<code class="literal">
     EUC_TW
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     gb18030_to_utf8
    </code>
</td>
<td>
<code class="literal">
     GB18030
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     gbk_to_utf8
    </code>
</td>
<td>
<code class="literal">
     GBK
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_10_to_utf8
    </code>
</td>
<td>
<code class="literal">
     LATIN6
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_13_to_utf8
    </code>
</td>
<td>
<code class="literal">
     LATIN7
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_14_to_utf8
    </code>
</td>
<td>
<code class="literal">
     LATIN8
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_15_to_utf8
    </code>
</td>
<td>
<code class="literal">
     LATIN9
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_16_to_utf8
    </code>
</td>
<td>
<code class="literal">
     LATIN10
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_1_to_mic
    </code>
</td>
<td>
<code class="literal">
     LATIN1
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_1_to_utf8
    </code>
</td>
<td>
<code class="literal">
     LATIN1
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_2_to_mic
    </code>
</td>
<td>
<code class="literal">
     LATIN2
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_2_to_utf8
    </code>
</td>
<td>
<code class="literal">
     LATIN2
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_2_to_windows_1250
    </code>
</td>
<td>
<code class="literal">
     LATIN2
    </code>
</td>
<td>
<code class="literal">
     WIN1250
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_3_to_mic
    </code>
</td>
<td>
<code class="literal">
     LATIN3
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_3_to_utf8
    </code>
</td>
<td>
<code class="literal">
     LATIN3
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_4_to_mic
    </code>
</td>
<td>
<code class="literal">
     LATIN4
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_4_to_utf8
    </code>
</td>
<td>
<code class="literal">
     LATIN4
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_5_to_koi8_r
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_5
    </code>
</td>
<td>
<code class="literal">
     KOI8R
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_5_to_mic
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_5
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_5_to_utf8
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_5
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_5_to_windows_1251
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_5
    </code>
</td>
<td>
<code class="literal">
     WIN1251
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_5_to_windows_866
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_5
    </code>
</td>
<td>
<code class="literal">
     WIN866
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_6_to_utf8
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_6
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_7_to_utf8
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_7
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_8_to_utf8
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_8
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     iso_8859_9_to_utf8
    </code>
</td>
<td>
<code class="literal">
     LATIN5
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     johab_to_utf8
    </code>
</td>
<td>
<code class="literal">
     JOHAB
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     koi8_r_to_iso_8859_5
    </code>
</td>
<td>
<code class="literal">
     KOI8R
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_5
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     koi8_r_to_mic
    </code>
</td>
<td>
<code class="literal">
     KOI8R
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     koi8_r_to_utf8
    </code>
</td>
<td>
<code class="literal">
     KOI8R
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     koi8_r_to_windows_1251
    </code>
</td>
<td>
<code class="literal">
     KOI8R
    </code>
</td>
<td>
<code class="literal">
     WIN1251
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     koi8_r_to_windows_866
    </code>
</td>
<td>
<code class="literal">
     KOI8R
    </code>
</td>
<td>
<code class="literal">
     WIN866
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     koi8_u_to_utf8
    </code>
</td>
<td>
<code class="literal">
     KOI8U
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_big5
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     BIG5
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_euc_cn
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     EUC_CN
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_euc_jp
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     EUC_JP
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_euc_kr
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     EUC_KR
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_euc_tw
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     EUC_TW
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_iso_8859_1
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     LATIN1
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_iso_8859_2
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     LATIN2
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_iso_8859_3
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     LATIN3
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_iso_8859_4
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     LATIN4
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_iso_8859_5
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_5
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_koi8_r
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     KOI8R
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_sjis
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     SJIS
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_windows_1250
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     WIN1250
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_windows_1251
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     WIN1251
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     mic_to_windows_866
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
<td>
<code class="literal">
     WIN866
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     sjis_to_euc_jp
    </code>
</td>
<td>
<code class="literal">
     SJIS
    </code>
</td>
<td>
<code class="literal">
     EUC_JP
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     sjis_to_mic
    </code>
</td>
<td>
<code class="literal">
     SJIS
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     sjis_to_utf8
    </code>
</td>
<td>
<code class="literal">
     SJIS
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_1258_to_utf8
    </code>
</td>
<td>
<code class="literal">
     WIN1258
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     uhc_to_utf8
    </code>
</td>
<td>
<code class="literal">
     UHC
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_big5
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     BIG5
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_euc_cn
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     EUC_CN
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_euc_jp
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     EUC_JP
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_euc_kr
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     EUC_KR
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_euc_tw
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     EUC_TW
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_gb18030
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     GB18030
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_gbk
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     GBK
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_1
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     LATIN1
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_10
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     LATIN6
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_13
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     LATIN7
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_14
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     LATIN8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_15
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     LATIN9
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_16
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     LATIN10
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_2
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     LATIN2
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_3
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     LATIN3
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_4
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     LATIN4
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_5
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_5
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_6
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_6
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_7
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_7
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_8
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_iso_8859_9
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     LATIN5
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_johab
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     JOHAB
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_koi8_r
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     KOI8R
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_koi8_u
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     KOI8U
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_sjis
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     SJIS
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_windows_1258
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     WIN1258
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_uhc
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     UHC
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_windows_1250
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     WIN1250
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_windows_1251
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     WIN1251
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_windows_1252
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     WIN1252
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_windows_1253
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     WIN1253
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_windows_1254
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     WIN1254
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_windows_1255
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     WIN1255
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_windows_1256
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     WIN1256
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_windows_1257
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     WIN1257
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_windows_866
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     WIN866
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_windows_874
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     WIN874
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_1250_to_iso_8859_2
    </code>
</td>
<td>
<code class="literal">
     WIN1250
    </code>
</td>
<td>
<code class="literal">
     LATIN2
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_1250_to_mic
    </code>
</td>
<td>
<code class="literal">
     WIN1250
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_1250_to_utf8
    </code>
</td>
<td>
<code class="literal">
     WIN1250
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_1251_to_iso_8859_5
    </code>
</td>
<td>
<code class="literal">
     WIN1251
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_5
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_1251_to_koi8_r
    </code>
</td>
<td>
<code class="literal">
     WIN1251
    </code>
</td>
<td>
<code class="literal">
     KOI8R
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_1251_to_mic
    </code>
</td>
<td>
<code class="literal">
     WIN1251
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_1251_to_utf8
    </code>
</td>
<td>
<code class="literal">
     WIN1251
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_1251_to_windows_866
    </code>
</td>
<td>
<code class="literal">
     WIN1251
    </code>
</td>
<td>
<code class="literal">
     WIN866
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_1252_to_utf8
    </code>
</td>
<td>
<code class="literal">
     WIN1252
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_1256_to_utf8
    </code>
</td>
<td>
<code class="literal">
     WIN1256
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_866_to_iso_8859_5
    </code>
</td>
<td>
<code class="literal">
     WIN866
    </code>
</td>
<td>
<code class="literal">
     ISO_8859_5
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_866_to_koi8_r
    </code>
</td>
<td>
<code class="literal">
     WIN866
    </code>
</td>
<td>
<code class="literal">
     KOI8R
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_866_to_mic
    </code>
</td>
<td>
<code class="literal">
     WIN866
    </code>
</td>
<td>
<code class="literal">
     MULE_INTERNAL
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_866_to_utf8
    </code>
</td>
<td>
<code class="literal">
     WIN866
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_866_to_windows_1251
    </code>
</td>
<td>
<code class="literal">
     WIN866
    </code>
</td>
<td>
<code class="literal">
     WIN
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     windows_874_to_utf8
    </code>
</td>
<td>
<code class="literal">
     WIN874
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     euc_jis_2004_to_utf8
    </code>
</td>
<td>
<code class="literal">
     EUC_JIS_2004
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_euc_jis_2004
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     EUC_JIS_2004
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     shift_jis_2004_to_utf8
    </code>
</td>
<td>
<code class="literal">
     SHIFT_JIS_2004
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     utf8_to_shift_jis_2004
    </code>
</td>
<td>
<code class="literal">
     UTF8
    </code>
</td>
<td>
<code class="literal">
     SHIFT_JIS_2004
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     euc_jis_2004_to_shift_jis_2004
    </code>
</td>
<td>
<code class="literal">
     EUC_JIS_2004
    </code>
</td>
<td>
<code class="literal">
     SHIFT_JIS_2004
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     shift_jis_2004_to_euc_jis_2004
    </code>
</td>
<td>
<code class="literal">
     SHIFT_JIS_2004
    </code>
</td>
<td>
<code class="literal">
     EUC_JIS_2004
    </code>
</td>
</tr>
</tbody>
<tbody class="footnotes">
<tr>
<td colspan="3">
<div class="footnote" id="ftn.id-1.6.10.5.8.4.2.4.1.1.1">
<p>
<a class="para" href="#id-1.6.10.5.8.4.2.4.1.1.1">
<sup class="para">
        [a]
       </sup>
</a>
      The conversion names follow a standard naming scheme: The official name of the source encoding with all non-alphanumeric characters replaced by underscores, followed by
      <code class="literal">
       _to_
      </code>
      , followed by the similarly processed destination encoding name.  Therefore, these names sometimes deviate from the customary encoding names shown in
      <a class="xref" href="multibyte.md#CHARSET-TABLE" title="Table 23.3. PostgreSQL Character Sets">
       Table 23.3
      </a>
      .
     </p>
</div>
</td>
</tr>
</tbody>
</table>



### 23.3.5. Leitura complementar [#](#MULTIBYTE-FURTHER-READING)

Essas são boas fontes para começar a aprender sobre vários tipos de sistemas de codificação.

*Processamento de Informação CJKV: Computação em Chinês, Japonês, Coreano e Vietnamita*: Contém explicações detalhadas de `EUC_JP`, `EUC_CN`, `EUC_KR`, `EUC_TW`.

<https://www.unicode.org/>: O site do Consórcio Unicode.

[RFC 3629][(https://datatracker.ietf.org/doc/html/rfc3629)]: O UTF-8 (Formato de Transformação UCS/Unicode de 8 bits) é definido aqui.