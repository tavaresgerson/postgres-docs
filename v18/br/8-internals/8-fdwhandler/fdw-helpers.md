## 58.3. Funções de Ajudas de Wrapper de Dados Estrangeiros [#](#FDW-HELPERS)

Várias funções auxiliares são exportadas do servidor central, para que os autores de wrappers de dados estrangeiros possam ter acesso fácil aos atributos dos objetos relacionados ao FDW, como as opções do FDW. Para usar qualquer uma dessas funções, você precisa incluir o arquivo de cabeçalho `foreign/foreign.h` em seu arquivo de origem. Esse cabeçalho também define os tipos de estrutura que são retornados por essas funções.

```
ForeignDataWrapper *
GetForeignDataWrapperExtended(Oid fdwid, bits16 flags);
```

Essa função retorna um objeto `ForeignDataWrapper` para o wrapper de dados estrangeiro com o OID fornecido. Um objeto `ForeignDataWrapper` contém propriedades do FDW (consulte `foreign/foreign.h` para detalhes). `flags` é uma máscara de bits ou'd que indica um conjunto extra de opções. Ele pode assumir o valor `FDW_MISSING_OK`, nesse caso, um resultado `NULL` é retornado para o chamador em vez de um erro para um objeto indefinido.

```
ForeignDataWrapper *
GetForeignDataWrapper(Oid fdwid);
```

Essa função retorna um objeto `ForeignDataWrapper` para o wrapper de dados externos com o OID fornecido. Um objeto `ForeignDataWrapper` contém propriedades do FDW (consulte `foreign/foreign.h` para detalhes).

```
ForeignServer *
GetForeignServerExtended(Oid serverid, bits16 flags);
```

Essa função retorna um objeto `ForeignServer` para o servidor estrangeiro com o OID fornecido. Um objeto `ForeignServer` contém propriedades do servidor (consulte `foreign/foreign.h` para detalhes). `flags` é uma máscara de bits ou'd que indica um conjunto adicional de opções. Pode assumir o valor `FSV_MISSING_OK`, nesse caso, um resultado `NULL` é retornado para o chamador em vez de um erro para um objeto indefinido.

```
ForeignServer *
GetForeignServer(Oid serverid);
```

Essa função retorna um objeto `ForeignServer` para o servidor estrangeiro com o OID fornecido. Um objeto `ForeignServer` contém propriedades do servidor (consulte `foreign/foreign.h` para detalhes).

```
UserMapping *
GetUserMapping(Oid userid, Oid serverid);
```

Essa função retorna um objeto `UserMapping` para o mapeamento do usuário do papel especificado no servidor especificado. (Se não houver mapeamento para o usuário específico, ele retornará o mapeamento para `PUBLIC`, ou lançará erro se não houver nenhum). Um objeto `UserMapping` contém propriedades do mapeamento do usuário (consulte `foreign/foreign.h` para detalhes).

```
ForeignTable *
GetForeignTable(Oid relid);
```

Essa função retorna um objeto `ForeignTable` para a tabela estrangeira com o OID fornecido. Um objeto `ForeignTable` contém propriedades da tabela estrangeira (consulte `foreign/foreign.h` para detalhes).

```
List *
GetForeignColumnOptions(Oid relid, AttrNumber attnum);
```

Essa função retorna as opções de FDW por coluna para a coluna com o OID da tabela estrangeira e o número de atributo fornecidos, na forma de uma lista de `DefElem`. O NIL é retornado se a coluna não tiver opções.

Alguns tipos de objetos têm funções de busca baseadas em nome, além das baseadas em OID:

```
ForeignDataWrapper *
GetForeignDataWrapperByName(const char *name, bool missing_ok);
```

Essa função retorna um objeto `ForeignDataWrapper` para o wrapper de dados externos com o nome fornecido. Se o wrapper não for encontrado, retorne NULL se missing_ok for verdadeiro, caso contrário, exiba um erro.

```
ForeignServer *
GetForeignServerByName(const char *name, bool missing_ok);
```

Essa função retorna um objeto `ForeignServer` para o servidor estrangeiro com o nome fornecido. Se o servidor não for encontrado, retorne NULL se missing_ok for verdadeiro, caso contrário, exiba um erro.