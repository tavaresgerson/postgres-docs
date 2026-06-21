## 68.2. Catálogo do sistema Dados iniciais [#](#SYSTEM-CATALOG-INITIAL-DATA)

* [68.2.1. Formato do arquivo de dados](system-catalog-initial-data.md#SYSTEM-CATALOG-INITIAL-DATA-FORMAT)
* [68.2.2. Atribuição de OID](system-catalog-initial-data.md#SYSTEM-CATALOG-OID-ASSIGNMENT)
* [68.2.3. Pesquisa de referência de OID](system-catalog-initial-data.md#SYSTEM-CATALOG-OID-REFERENCES)
* [68.2.4. Criação automática de tipos de matriz](system-catalog-initial-data.md#SYSTEM-CATALOG-AUTO-ARRAY-TYPES)
* [68.2.5. Receitas para edição de arquivos de dados](system-catalog-initial-data.md#SYSTEM-CATALOG-RECIPES)

Cada catálogo que tenha algum dado inicial criado manualmente (alguns não têm) tem um arquivo correspondente `.dat` que contém seus dados iniciais em um formato editável.

### 68.2.1. Formato do arquivo de dados [#](#SYSTEM-CATALOG-INITIAL-DATA-FORMAT)

Cada arquivo `.dat` contém literais de estrutura de dados Perl que são simplesmente avaliados para produzir uma estrutura de dados em memória composta por uma matriz de referências de hash, uma por linha de catálogo. Um trecho ligeiramente modificado de `pg_database.dat` demonstrará as principais características:

```
[

# A comment could appear here.
{ oid => '1', oid_symbol => 'Template1DbOid',
  descr => 'database\'s default template',
  datname => 'template1', encoding => 'ENCODING',
  datlocprovider => 'LOCALE_PROVIDER', datistemplate => 't',
  datallowconn => 't', dathasloginevt => 'f', datconnlimit => '-1', datfrozenxid => '0',
  datminmxid => '1', dattablespace => 'pg_default', datcollate => 'LC_COLLATE',
  datctype => 'LC_CTYPE', datlocale => 'DATLOCALE', datacl => '_null_' },

]
```

Pontos a destacar:

* O layout geral do arquivo é: chaves fechadas em chaves angulares, um ou mais conjuntos de chaves angulares, cada um representando uma linha de catálogo, chaves fechadas em chaves angulares. Escreva uma vírgula após cada chave fechada em chaves angulares.
* Dentro de cada linha de catálogo, escreva pares separados por vírgula *`key`* *`=>` *`value`*. Os *`key`s permitidos são os nomes das colunas do catálogo, além das chaves de metadados `oid`, `oid_symbol`, `array_type_oid`, e `descr`. (O uso de `oid` e `oid_symbol` é descrito em [Seção 68.2.2](system-catalog-initial-data.md#SYSTEM-CATALOG-OID-ASSIGNMENT "68.2.2. OID Assignment") abaixo, enquanto `array_type_oid` é descrito em [Seção 68.2.4](system-catalog-initial-data.md#SYSTEM-CATALOG-AUTO-ARRAY-TYPES "68.2.4. Automatic Creation of Array Types"). `descr` fornece uma string de descrição para o objeto, que será inserida em `pg_description` ou `pg_shdescription` conforme apropriado.) Embora as chaves de metadados sejam opcionais, todas as colunas definidas do catálogo devem ser fornecidas, exceto quando o arquivo `.h` do catálogo especifica um valor padrão para a coluna. (No exemplo acima, o campo `datdba` foi omitido porque `pg_database.h` fornece um valor padrão adequado para ele.)
* Todos os valores devem ser em citação simples. Esconda as citações simples usadas dentro de um valor com uma barra invertida. As barras invertidas significam dados, mas não precisam ser duplicadas; isso segue as regras do Perl para literais citados simples. Note que as barras que aparecem como dados serão tratadas como escapamentos pelo scanner de bootstrap, de acordo com as mesmas regras que para constantes de string de escapamento (veja [Seção 4.1.2.2](sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE "4.1.2.2. String Constants with C-Style Escapes")); por exemplo, `\t` converte em um caractere de tabulação. Se você realmente quiser uma barra invertida no valor final, você precisará escrever quatro delas: o Perl remove duas, deixando `\\` para que o scanner de bootstrap veja.
* Valores nulos são representados por `_null_`. (Note que não há como criar um valor que seja apenas essa string.)
* Comentários são precedidos por `#`, e devem estar em suas próprias linhas.
* Os valores dos campos que são OIDs de outras entradas do catálogo devem ser representados por nomes simbólicos em vez de OIDs numéricos reais. (No exemplo acima, `dattablespace` contém tal referência.) Isso é descrito em [Seção 68.2.3](system-catalog-initial-data.md#SYSTEM-CATALOG-OID-REFERENCES "68.2.3. OID Reference Lookup") abaixo.
* Como os hashes são estruturas de dados não ordenadas, a ordem dos campos e o layout das linhas não são semânticamente significativos. No entanto, para manter uma aparência consistente, definimos algumas regras que são aplicadas pelo script de formatação `reformat_dat_file.pl`:

+ Dentro de cada par de chaves espirais, os campos de metadados `oid`, `oid_symbol`, `array_type_oid` e `descr` (se presentes) vêm primeiro, nessa ordem, depois os campos do próprio catálogo aparecem em seu ordem definida.
  + Novas linhas são inseridas entre os campos conforme necessário para limitar o comprimento da linha a 80 caracteres, se possível. Uma nova linha também é inserida entre os campos de metadados e os campos regulares.
  + Se o arquivo `.h` do catálogo especificar um valor padrão para uma coluna e uma entrada de dados tenha esse mesmo valor, `reformat_dat_file.pl` o omitirá do arquivo de dados. Isso mantém a representação dos dados compacta.
  + `reformat_dat_file.pl` preserva as linhas em branco e as linhas de comentário como estão.

Recomenda-se executar `reformat_dat_file.pl` antes de submeter os patches de dados do catálogo. Para conveniência, você pode simplesmente mudar para `src/include/catalog/` e executar `make reformat-dat-files`. * Se você deseja adicionar um novo método para tornar a representação dos dados menor, você deve implementá-lo em `reformat_dat_file.pl` e também ensinar `Catalog::ParseData()` a expandir os dados de volta para a representação completa.

### 68.2.2. Atribuição de OID [#](#SYSTEM-CATALOG-OID-ASSIGNMENT)

Uma linha de catálogo que aparece nos dados iniciais pode receber um OID atribuído manualmente escrevendo um campo de metadados `oid => nnnn`. Além disso, se um OID for atribuído, uma macro C para esse OID pode ser criada escrevendo um campo de metadados `oid_symbol => name`.

As linhas do catálogo pré-carregadas devem ter OIDs pré-atribuídos se houver referências de OID para elas em outras linhas pré-carregadas. Um OID pré-atribuído também é necessário se o OID da linha precisar ser referenciado a partir do código C. Se nenhum dos casos se aplica, o campo de metadados `oid` pode ser omitido, nesse caso, o código de bootstrap atribui um OID automaticamente. Na prática, geralmente predefinimos OIDs para todas ou nenhuma das linhas pré-carregadas em um catálogo dado, mesmo que apenas algumas delas sejam realmente cruzadas.

Escrever o valor numérico real de qualquer OID em código C é considerado uma forma muito ruim; sempre use uma macro, em vez disso. Referências diretas aos OIDs `pg_proc` são suficientemente comuns para que haja um mecanismo especial para criar as macros necessárias automaticamente; veja `src/backend/utils/Gen_fmgrtab.pl`. Da mesma forma — mas, por razões históricas, não feito da mesma maneira — há um método automático para criar macros para OIDs `pg_type`. As entradas `oid_symbol` não são, portanto, necessárias nesses dois catálogos. Da mesma forma, as macros para os OIDs `pg_class` dos catálogos e índices do sistema são configuradas automaticamente. Para todos os outros catálogos do sistema, você precisa especificar manualmente quaisquer macros necessárias via entradas `oid_symbol`.

Para encontrar um OID disponível para uma nova linha pré-carregada, execute o script `src/include/catalog/unused_oids`. Ele imprime os intervalos inclusivos de OIDs não utilizados (por exemplo, a linha de saída `45-900` significa que os OIDs 45 a 900 ainda não foram alocados). Atualmente, os OIDs 1–9999 são reservados para atribuição manual; o script `unused_oids` simplesmente examina os cabeçalhos do catálogo e os arquivos `.dat` para ver quais deles não aparecem. Você também pode usar o script `duplicate_oids` para verificar erros. (O script `genbki.pl` atribuirá OIDs para quaisquer linhas que não tenham sido atribuídas manualmente e também detectará duplicatas de OIDs no momento da compilação.)

Ao escolher OIDs para um patch que não é esperado ser comprometido imediatamente, a melhor prática é usar um grupo de OIDs mais ou menos consecutivos, começando com alguma escolha aleatória na faixa de 8000 a 9999. Isso minimiza o risco de colisões de OIDs com outros patches que estão sendo desenvolvidos simultaneamente. Para manter a faixa de 8000 a 9999 livre para fins de desenvolvimento, após um patch ter sido comprometido no repositório mestre do git, seus OIDs devem ser renumerados em espaço disponível abaixo dessa faixa. Tipicamente, isso é feito perto do final de cada ciclo de desenvolvimento, movendo todos os OIDs consumidos por patches comprometidos nesse ciclo ao mesmo tempo. O script `renumber_oids.pl` pode ser usado para esse propósito. Se um patch não comprometido for encontrado com conflitos de OID com algum patch recentemente comprometido, `renumber_oids.pl` também pode ser útil para se recuperar dessa situação.

Devido a essa convenção de possivelmente renumerar OIDs atribuídos por patches, os OIDs atribuídos por um patch não devem ser considerados estáveis até que o patch tenha sido incluído em uma versão oficial. No entanto, não alteramos OIDs de objetos atribuídos manualmente uma vez que foram liberados, pois isso criaria problemas de compatibilidade variados.

Se o `genbki.pl` precisar atribuir um OID a uma entrada de catálogo que não tenha um OID atribuído manualmente, ele usará um valor no intervalo de 10000 a 11999. O contador de OID do servidor é definido em 10000 no início de uma execução de bootstrap, para que quaisquer objetos criados em tempo real durante o processamento de bootstrap também recebam OIDs neste intervalo. (O mecanismo usual de atribuição de OID cuida para evitar quaisquer conflitos.)

Objetos com OIDs abaixo de `FirstUnpinnedObjectId` (12000) são considerados "fixados", impedindo que sejam excluídos. (Há um pequeno número de exceções, que estão embutidas em `IsPinnedObject()`.). O initdb força o contador de OID até `FirstUnpinnedObjectId` assim que está pronto para criar objetos não fixados. Assim, os objetos criados durante as fases posteriores do initdb, como os objetos criados enquanto executa o script `information_schema.sql`, não serão fixados, enquanto todos os objetos conhecidos por `genbki.pl` serão.

Os OIDs atribuídos durante o funcionamento normal do banco de dados são restritos a serem 16384 ou superior. Isso garante que o intervalo de 10000 a 16383 esteja livre para OIDs automaticamente atribuídos por `genbki.pl` ou durante o initdb. Esses OIDs automaticamente atribuídos não são considerados estáveis e podem mudar de uma instalação para outra.

### 68.2.3. Busca de referência de OID [#](#SYSTEM-CATALOG-OID-REFERENCES)

Em princípio, as referências cruzadas de uma linha inicial de catálogo para outra poderiam ser escritas simplesmente escrevendo o OID pré-atribuído da linha referenciada no campo de referência. No entanto, isso vai contra a política do projeto, porque é propenso a erros, difícil de ler e sujeito a quebra se um OID recém-atribuído for renumerado. Portanto, o `genbki.pl` fornece mecanismos para escrever referências simbólicas em vez disso. As regras são as seguintes:

* O uso de referências simbólicas é habilitado em uma coluna de catálogo específica anexando `BKI_LOOKUP(lookuprule)` à definição da coluna, onde *`lookuprule`* é o nome do catálogo referenciado, por exemplo, `pg_proc`. `BKI_LOOKUP` pode ser anexado a colunas do tipo `Oid`, `regproc`, `oidvector` ou `Oid[]`; nos dois últimos casos, isso implica realizar uma pesquisa em cada elemento do array.
* Também é permitido anexar `BKI_LOOKUP(encoding)` a colunas numéricas para referenciar codificações de conjuntos de caracteres, que atualmente não são representadas como OIDs de catálogo, mas têm um conjunto de valores conhecidos por `genbki.pl`.
* Em algumas colunas de catálogo, é permitido que as entradas sejam zero em vez de uma referência válida. Se isso for permitido, escreva `BKI_LOOKUP_OPT` em vez de `BKI_LOOKUP`. Em seguida, você pode escrever `0` para uma entrada. (Se a coluna for declarada como `regproc`, você pode opcionalmente escrever `-` em vez de `0`.]) Exceto por esse caso especial, todas as entradas em uma coluna de `BKI_LOOKUP` devem ser referências simbólicas. `genbki.pl` alertará sobre nomes não reconhecidos.
* A maioria dos tipos de objetos de catálogo é simplesmente referenciada por seus nomes. Note que os nomes dos tipos devem corresponder exatamente à entrada `typname` do `integer` (isso funciona como entrada de regproc). Caso contrário, escreva como *`proname(argtypename,argtypename,...)`*, como regprocedure. Os nomes dos tipos de argumento devem ser escritos exatamente como aparecem no campo `pg_proc.dat` da entrada `proargtypes`. Não insira espaços.
* Os operadores são representados por *`oprname(lefttype,righttype)`*, escrevendo os nomes dos tipos exatamente como aparecem nos campos `pg_operator.dat` e `oprright` da entrada `oprleft`. (Escreva `0` para o operador unário omitido.)
* Os nomes das opclasses e opfamilies são únicos apenas dentro de um método de acesso, então são representados por *`access_method_name`*`/`*`object_name`.
* Nenhum desses casos prevê disposição para qualificação de esquema; todos os objetos criados durante o bootstrap são esperados estar no esquema `pg_catalog`.

`genbki.pl` resolve todas as referências simbólicas enquanto está em execução e coloca IDs numéricos simples no arquivo BKI emitido. Portanto, não há necessidade de o backend de bootstrap lidar com referências simbólicas.

É desejável marcar as colunas de referência OID com `BKI_LOOKUP` ou `BKI_LOOKUP_OPT`, mesmo que o catálogo não tenha dados iniciais que exijam pesquisa. Isso permite que `genbki.pl` registre as relações de chave estrangeira que existem nos catálogos do sistema. Essas informações são usadas nos testes de regressão para verificar entradas incorretas. Veja também as macros `DECLARE_FOREIGN_KEY`, `DECLARE_FOREIGN_KEY_OPT`, `DECLARE_ARRAY_FOREIGN_KEY` e `DECLARE_ARRAY_FOREIGN_KEY_OPT`, que são usadas para declarar relações de chave estrangeira que são muito complexas para `BKI_LOOKUP` (tipicamente, chaves estrangeiras de várias colunas).

### 68.2.4. Criação automática de tipos de matriz [#](#SYSTEM-CATALOG-AUTO-ARRAY-TYPES)

A maioria dos tipos de dados escalares deve ter um tipo de matriz correspondente (ou seja, um tipo de matriz padrão de varlena, cujo tipo de elemento é o tipo escalar, e que é referenciado pelo campo `typarray` da entrada `pg_type` do tipo escalar). `genbki.pl` é capaz de gerar a entrada `pg_type` para o tipo de matriz automaticamente na maioria dos casos.

Para usar essa facilidade, basta escrever um campo de metadados `array_type_oid => nnnn` na entrada `pg_type` do tipo escalar, especificando o OID a ser usado para o tipo de matriz. Em seguida, você pode omitir o campo `typarray`, uma vez que ele será preenchido automaticamente com esse OID.

O nome do tipo de matriz gerado é o nome do tipo escalar com um underscore pré-pendido. Os outros campos da entrada da matriz são preenchidos a partir das anotações `BKI_ARRAY_DEFAULT(value)` em `pg_type.h`, ou se não houver uma, copiadas do tipo escalar. (Há também um caso especial para `typalign`.) Em seguida, os campos `typelem` e `typarray` das duas entradas são definidos para fazer referência cruzada entre si.

### 68.2.5. Receitas para edição de arquivos de dados [#](#SYSTEM-CATALOG-RECIPES)

Aqui estão algumas sugestões sobre as formas mais fáceis de realizar tarefas comuns ao atualizar arquivos de dados do catálogo.

**Adicione uma nova coluna com um valor padrão a um catálogo:** Adicione a coluna ao arquivo de cabeçalho com uma anotação `BKI_DEFAULT(value)`. O arquivo de dados só precisa ser ajustado adicionando o campo em linhas existentes onde é necessário um valor não padrão.

**Adicione um valor padrão a uma coluna existente que não o tenha:** Adicione uma anotação `BKI_DEFAULT` ao arquivo de cabeçalho, em seguida, execute `make reformat-dat-files` para remover as entradas de campo agora redundantes.

**Remova uma coluna, independentemente de ela ter um padrão ou não:** Remova a coluna do cabeçalho, em seguida, execute `make reformat-dat-files` para remover as entradas de campo que não são mais úteis.

**Alterar ou remover um valor padrão existente:** Você não pode simplesmente alterar o arquivo de cabeçalho, pois isso fará com que os dados atuais sejam interpretados incorretamente. Primeiro, execute `make expand-dat-files` para reescrever os arquivos de dados com todos os valores padrão inseridos explicitamente, em seguida, altere ou remova a anotação `BKI_DEFAULT`, em seguida, execute `make reformat-dat-files` para remover campos supérfluos novamente.

**Edição em massa ad-hoc:** `reformat_dat_file.pl` pode ser adaptado para realizar muitos tipos de alterações em massa. Procure seus comentários em bloco que mostram onde o código único pode ser inserido. No exemplo a seguir, vamos consolidar dois campos booleanos em `pg_proc` em um campo de caractere:

1. Adicione a nova coluna, com uma coluna padrão, a `pg_proc.h`:

2. Crie um novo script com base em `reformat_dat_file.pl` para inserir valores apropriados em tempo real:

```
   -           # At this point we have the full row in memory as a hash
   -           # and can do any operations we want. As written, it only
   -           # removes default values, but this script can be adapted to
   -           # do one-off bulk-editing.
   +           # One-off change to migrate to prokind
   +           # Default has already been filled in by now, so change to other
   +           # values as appropriate
   +           if ($values{proisagg} eq 't')
   +           {
   +               $values{prokind} = 'a';
   +           }
   +           elsif ($values{proiswindow} eq 't')
   +           {
   +               $values{prokind} = 'w';
   +           }
   ``` 3. Execute o novo script:

   ```
   $ cd src/include/catalog
   $ perl  rewrite_dat_with_prokind.pl  pg_proc.dat
   ```

Neste ponto, `pg_proc.dat` possui as três colunas `prokind`, `proisagg` e `proiswindow`, embora elas apareçam apenas em linhas onde elas têm valores não padrão.
4. Remova as colunas antigas de `pg_proc.h`:

5. Por fim, execute `make reformat-dat-files` para remover as entradas antigas inúteis de `pg_proc.dat`.

Para mais exemplos de scripts usados para edição em massa, consulte `convert_oid2name.pl` e `remove_pg_type_oid_symbols.pl` anexados a esta mensagem:
<https://www.postgresql.org/message-id/CAJVSVGVX8gXnPm+Xa=DxR7kFYprcQ1tNcCT5D0O3ShfnM6jehA@mail.gmail.com>