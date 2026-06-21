## 23.1. Suporte a localização [#](#LOCALE)

* [23.1.1. Visão geral](locale.md#LOCALE-OVERVIEW)
* [23.1.2. Comportamento](locale.md#LOCALE-BEHAVIOR)
* [23.1.3. Seleção de locais](locale.md#LOCALE-SELECTING-LOCALES)
* [23.1.4. Fornecedores de locais](locale.md#LOCALE-PROVIDERS)
* [23.1.5. Locais ICU](locale.md#ICU-LOCALES)
* [23.1.6. Problemas](locale.md#LOCALE-PROBLEMS)

O suporte ao *Locale* refere-se a uma aplicação que respeita as preferências culturais em relação a alfabetos, classificação, formatação de números, etc. O PostgreSQL utiliza as instalações padrão de localização ISO C e POSIX fornecidas pelo sistema operacional do servidor. Para informações adicionais, consulte a documentação do seu sistema.

### 23.1.1. Visão geral [#](#LOCALE-OVERVIEW)

O suporte ao local é iniciado automaticamente quando um clúster de banco de dados é criado usando `initdb`. `initdb` iniciará o clúster de banco de dados com o ajuste do local de seu ambiente de execução por padrão, então, se o seu sistema já estiver configurado para usar o local que você deseja em seu clúster de banco de dados, não há nada mais que você precise fazer. Se você quiser usar um local diferente (ou não tem certeza de qual local o seu sistema está configurado) pode instruir `initdb` exatamente qual local usar, especificando a opção `--locale`. Por exemplo:

```
initdb --locale=sv_SE
```

Este exemplo para sistemas Unix define o idioma como sueco (`sv`) como falado na Suécia (`SE`). Outras possibilidades podem incluir `en_US` (inglês dos EUA) e `fr_CA` (francês canadense). Se mais de um conjunto de caracteres pode ser usado para um idioma, as especificações podem ter a forma *`language_territory.codeset`*. Por exemplo, `fr_BE.UTF-8` representa o idioma francês (fr) como falado na Bélgica (BE), com codificação de UTF-8.

Os locais disponíveis no seu sistema sob quais nomes dependem do que foi fornecido pelo fornecedor do sistema operacional e do que foi instalado. Na maioria dos sistemas Unix, o comando `locale -a` fornecerá uma lista de locais disponíveis. O Windows usa nomes de local mais verbose, como `German_Germany` ou `Swedish_Sweden.1252`, mas os princípios são os mesmos.

Ocasionalmente, é útil misturar regras de vários locais, por exemplo, usar regras de ordenação em inglês, mas mensagens em espanhol. Para isso, existe um conjunto de subcategorias de local que controlam apenas certos aspectos das regras de localização:



<table border="1" class="informaltable">
<colgroup>
<col class="col1"/>
<col class="col2"/>
</colgroup>
<tbody>
<tr>
<td>
<code class="envar">
     LC_COLLATE
    </code>
</td>
<td>Ordem de classificação de cordas</td>
</tr>
<tr>
<td>
<code class="envar">
     LC_CTYPE
    </code>
</td>
<td>Classificação de caracteres (O que é uma letra? Seu equivalente em maiúsculas?)</td>
</tr>
<tr>
<td>
<code class="envar">
     LC_MESSAGES
    </code>
</td>
<td>Idioma das mensagens</td>
</tr>
<tr>
<td>
<code class="envar">
     LC_MONETARY
    </code>
</td>
<td>Formatação de valores em moeda</td>
</tr>
<tr>
<td>
<code class="envar">
     LC_NUMERIC
    </code>
</td>
<td>Formatação de números</td>
</tr>
<tr>
<td>
<code class="envar">
     LC_TIME
    </code>
</td>
<td>Formatação de datas e horários</td>
</tr>
</tbody>
</table>



Os nomes das categorias traduzem-se em nomes de opções do `initdb` para substituir a escolha do local para uma categoria específica. Por exemplo, para definir o local como francês canadense, mas usar as regras dos EUA para formatação de moeda, use `initdb --locale=fr_CA --lc-monetary=en_US`.

Se você deseja que o sistema se comporte como se não tivesse suporte a localização, use o nome especial de localização `C`, ou, de forma equivalente, `POSIX`.

Algumas categorias de localização devem ter seus valores fixos quando o banco de dados é criado. Você pode usar diferentes configurações para diferentes bancos de dados, mas uma vez que um banco de dados é criado, você não pode mais alterá-los para esse banco de dados. `LC_COLLATE` e `LC_CTYPE` são essas categorias. Elas afetam a ordem de classificação dos índices, então elas devem ser mantidas fixas, ou os índices em colunas de texto se tornariam corrompidos. (Mas você pode aliviar essa restrição usando colatelias, como discutido em [Seção 23.2][(collation.md "23.2. Collation Support")]. Os valores padrão para essas categorias são determinados quando `initdb` é executado, e esses valores são usados quando novos bancos de dados são criados, a menos que seja especificado de outra forma no comando `CREATE DATABASE`.

As outras categorias de localização podem ser alteradas sempre que desejado, definindo os parâmetros de configuração do servidor que têm o mesmo nome das categorias de localização (consulte [Seção 19.11.2] para detalhes). Os valores escolhidos por (runtime-config-client.md#RUNTIME-CONFIG-CLIENT-FORMAT "19.11.2. Locale and Formatting") são, na verdade, apenas escritos no arquivo de configuração `postgresql.conf` para servir como padrões quando o servidor é iniciado. Se você remover essas atribuições de `postgresql.conf`, o servidor herdará as configurações do seu ambiente de execução.

Observe que o comportamento do local do servidor é determinado pelas variáveis de ambiente que o servidor vê, e não pelo ambiente de qualquer cliente. Portanto, tenha cuidado para configurar as configurações de local corretos antes de iniciar o servidor. Uma consequência disso é que, se o cliente e o servidor estiverem configurados em locais diferentes, as mensagens podem aparecer em diferentes idiomas, dependendo de onde elas se originaram.

### Nota

Quando falamos em herdar o local do ambiente de execução, isso significa o seguinte na maioria dos sistemas operacionais: Para uma categoria de local específica, digamos a correção de texto, as seguintes variáveis de ambiente são consultadas nesta ordem até que uma seja encontrada para ser definida: `LC_ALL`, `LC_COLLATE` (ou a variável correspondente à respectiva categoria), `LANG`. Se nenhuma dessas variáveis de ambiente estiver definida, o local padrão é `C`.

Algumas bibliotecas de localização de mensagens também analisam a variável de ambiente `LANGUAGE`, que substitui todas as outras configurações de localização para o propósito de definir o idioma das mensagens. Se houver dúvidas, consulte a documentação do seu sistema operacional, em particular a documentação sobre gettext.

Para permitir que as mensagens sejam traduzidas para o idioma preferido do usuário, o NLS deve ter sido selecionado na hora da construção (`configure --enable-nls`). Todo o outro suporte de localização é construído automaticamente.

### 23.1.2. Comportamento [#](#LOCALE-BEHAVIOR)

As configurações de localização influenciam os seguintes recursos do SQL:

* Ordenar a ordem em consultas usando `ORDER BY` ou os operadores de comparação padrão em dados textuais
* As funções `upper`, `lower` e `initcap`
* Operadores de correspondência de padrões (`LIKE`, `SIMILAR TO` e expressões regulares estilo POSIX); os locais afetam tanto a correspondência insensível ao caso quanto a classificação de caracteres por expressões regulares de classe de caracteres
* A família de funções `to_char`
* A capacidade de usar índices com cláusulas `LIKE`

O inconveniente de usar locais diferentes de `C` ou `POSIX` no PostgreSQL é o impacto em termos de desempenho. Isso reduz o manuseio de caracteres e impede que índices comuns sejam usados pelo `LIKE`. Por esse motivo, use locais apenas se você realmente precisar deles.

Como uma solução para permitir que o PostgreSQL use índices com cláusulas `LIKE` em um local não C, existem várias classes de operadores personalizados. Essas permitem a criação de um índice que realiza uma comparação estrita caractere por caractere, ignorando as regras de comparação de local. Consulte [Seção 11.10][(indexes-opclass.md "11.10. Operator Classes and Operator Families")] para mais informações. Outra abordagem é criar índices usando a collation `C`, conforme discutido em [Seção 23.2][(collation.md "23.2. Collation Support")].

### 23.1.3. Selecionar Locais [#](#LOCALE-SELECTING-LOCALES)

Os locais podem ser selecionados em diferentes escopos, dependendo das necessidades. A visão acima mostrou como os locais são especificados usando `initdb` para definir os padrões para todo o clúster. A lista a seguir mostra onde os locais podem ser selecionados. Cada item fornece os padrões para os itens subsequentes, e cada item inferior permite a supressão dos padrões em uma granularidade mais fina.

1. Como explicado acima, o ambiente do sistema operacional fornece os padrões para as localidades de um clúster de banco de dados recém-inicializado. Em muitos casos, isso é suficiente: se o sistema operacional estiver configurado para o idioma/território desejado, o PostgreSQL também se comportará de acordo com essa localidade por padrão.
2. Como mostrado acima, as opções de linha de comando para `initdb` especificam as configurações de localidade para um clúster de banco de dados recém-inicializado. Use isso se o sistema operacional não tiver a configuração de localidade que você deseja para seu sistema de banco de dados.
3. Uma localidade pode ser selecionada separadamente para cada banco de dados. O comando SQL `CREATE DATABASE` e seu equivalente de linha de comando `createdb` têm opções para isso. Use isso, por exemplo, se um clúster de bancos de dados abriga bancos de dados para vários inquilinos com requisitos diferentes.
4. As configurações de localidade podem ser feitas para colunas individuais de tabela. Isso usa um objeto SQL chamado *collation* e é explicado em [Seção 23.2][(collation.md "23.2. Collation Support")]. Use isso, por exemplo, para ordenar dados em diferentes idiomas ou personalizar a ordem de classificação de uma tabela específica.
5. Por fim, as localidades podem ser selecionadas para uma consulta individual. Novamente, isso usa objetos de collation SQL. Isso poderia ser usado para alterar a ordem de classificação com base em escolhas em tempo real ou para experimentação ad hoc.

### 23.1.4. Fornecedores de localização [#](#LOCALE-PROVIDERS)

Um provedor de localização especifica qual biblioteca define o comportamento da localização para colatões e classificações de caracteres.

Os comandos e ferramentas que selecionam as configurações de localização, conforme descrito acima, cada um tem uma opção para selecionar o provedor de localização. Aqui está um exemplo para inicializar um clúster de banco de dados usando o provedor ICU:

```
initdb --locale-provider=icu --icu-locale=en
```

Veja a descrição dos respectivos comandos e programas para obter detalhes. Observe que você pode misturar provedores de localização em diferentes granularidades, por exemplo, use `libc` como padrão para o clúster, mas tenha um banco de dados que use o provedor `icu`, e, em seguida, tenha objetos de collation usando qualquer um desses provedores dentro desses bancos de dados.

Independentemente do provedor de localização, o sistema operacional ainda é usado para fornecer algum comportamento sensível à localização, como mensagens (consulte [lc_messages][(runtime-config-client.md#GUC-LC-MESSAGES)]).

Os provedores de localização disponíveis estão listados abaixo:

`builtin`: O provedor `builtin` utiliza operações internas. Apenas os locais `C`, `C.UTF-8` e `PG_UNICODE_FAST` são suportados para este provedor.

O comportamento do local `C` é idêntico ao do local `C` no provedor de libc. Ao usar este local, o comportamento pode depender do codificação do banco de dados.

O local `C.UTF-8` está disponível apenas quando o codificação do banco de dados é `UTF-8`, e o comportamento é baseado em Unicode. A agregação de caracteres usa apenas os valores dos pontos de código. As classes de caracteres da expressão regular são baseadas na semântica "Compatível com POSIX", e o mapeamento de caso é a variante "simples".

O local `PG_UNICODE_FAST` está disponível apenas quando o codificação do banco de dados é `UTF-8`, e o comportamento é baseado em Unicode. A agregação de caracteres usa apenas os valores dos pontos de código. As classes de caracteres da expressão regular são baseadas na semântica "Padrão", e o mapeamento de caso é a variante "total".

`icu`: O provedor `icu` utiliza a biblioteca de ICU externa. O PostgreSQL deve ter sido configurado com suporte.

O ICU fornece comportamento de classificação e classificação de caracteres que é independente do sistema operacional e do codificação do banco de dados, o que é preferível se você espera fazer uma transição para outras plataformas sem qualquer alteração nos resultados. `LC_COLLATE` e `LC_CTYPE` podem ser definidos independentemente do local do ICU.

### Nota

Para o provedor de ICU, os resultados podem depender da versão da biblioteca de ICU utilizada, pois ela é atualizada para refletir as mudanças no idioma natural ao longo do tempo.

`libc`: O provedor `libc` utiliza a biblioteca C do sistema operacional. O comportamento de classificação e classificação de caracteres é controlado pelas configurações `LC_COLLATE` e `LC_CTYPE`, portanto, não podem ser configuradas de forma independente.

### Nota

O mesmo nome de local pode ter comportamento diferente em diferentes plataformas ao usar o provedor libc.

### 23.1.5. ICU Locais [#](#ICU-LOCALES)

#### 23.1.5.1. Nomes locais do ICU [#](#ICU-LOCALE-NAMES)

O formato ICU para o nome do local é um [Tag de idioma][(locale.md#ICU-LANGUAGE-TAG "23.1.5.3. Language Tag")].

```
CREATE COLLATION mycollation1 (provider = icu, locale = 'ja-JP');
CREATE COLLATION mycollation2 (provider = icu, locale = 'fr');
```

#### 23.1.5.2. **Canonicalização e validação de local [#](#ICU-CANONICALIZATION)

Ao definir um novo objeto de colagem de ICU ou um banco de dados com ICU como provedor, o nome do local fornecido é transformado (canônico) em uma tag de idioma, se ainda não estiver nessa forma. Por exemplo,

```
CREATE COLLATION mycollation3 (provider = icu, locale = 'en-US-u-kn-true');
NOTICE:  using standard form "en-US-u-kn" for locale "en-US-u-kn-true"
CREATE COLLATION mycollation4 (provider = icu, locale = 'de_DE.utf8');
NOTICE:  using standard form "de-DE" for locale "de_DE.utf8"
```

Se você ver este aviso, certifique-se de que os `provider` e `locale` são os resultados esperados. Para resultados consistentes ao usar o provedor de UTI, especifique a tag de idioma canônica (locale.md#ICU-LANGUAGE-TAG "23.1.5.3. Language Tag") em vez de confiar na transformação.

Um local sem nome de idioma, ou o nome especial do idioma `root`, é transformado para ter o idioma `und` ("definido").

O ICU pode transformar a maioria dos nomes de localização da libc, bem como alguns outros formatos, em tags de idioma para uma transição mais fácil para o ICU. Se um nome de localização da libc for usado no ICU, ele pode não ter exatamente o mesmo comportamento que na libc.

Se houver um problema na interpretação do nome do local, ou se o nome do local representar uma língua ou região que o ICU não reconheça, você verá o seguinte aviso:

```
CREATE COLLATION nonsense (provider = icu, locale = 'nonsense');
WARNING:  ICU locale "nonsense" has unknown language "nonsense"
HINT:  To disable ICU locale validation, set parameter icu_validation_level to DISABLED.
CREATE COLLATION
```

[icu_validation_level](runtime-config-client.md#GUC-ICU-VALIDATION-LEVEL) controla como a mensagem é relatada. A menos que esteja configurado para `ERROR`, a agregação ainda será criada, mas o comportamento pode não ser o que o usuário pretendia.

#### 23.1.5.3.  Tag de idioma [#](#ICU-LANGUAGE-TAG)

Uma tag de idioma, definida no BCP 47, é um identificador padronizado usado para identificar idiomas, regiões e outras informações sobre um local.

As tags básicas de idioma são simplesmente *`language`*`-`*`region`*; ou até mesmo apenas *`language`*. O *`language`* é um código de idioma (por exemplo, `fr` para francês), e *`region`* é um código de região (por exemplo, `CA` para o Canadá). Exemplos: `ja-JP`, `de`, ou `fr-CA`.

As configurações de ordenação podem ser incluídas na tag de idioma para personalizar o comportamento de ordenação. O ICU permite uma ampla personalização, como a sensibilidade (ou insensibilidade) a acentos, maiúsculas e pontuação; tratamento de dígitos dentro do texto; e muitas outras opções para atender a uma variedade de usos.

Para incluir essas informações adicionais de ordenação em uma tag de idioma, adicione `-u`, que indica que há configurações adicionais de ordenação, seguidas por um ou mais pares `-`*`key`*`-`*`value`*`key`*. O *`value`* é a chave para uma configuração de ordenação [(collation.md#ICU-COLLATION-SETTINGS "23.2.3.2. Collation Settings for an ICU Locale")] e *`-`* é um valor válido para essa configuração. Para configurações booleanas, o `key`*`-`* pode ser especificado sem um correspondente `value`*, o que implica um valor de `true`.

Por exemplo, o identificador de idioma `en-US-u-kn-ks-level2` significa o local com o idioma inglês na região dos EUA, com as configurações de ordenação `kn` definidas como `true` e `ks` definida como `level2`. Essas configurações significam que a ordenação será insensível ao caso e tratará uma sequência de dígitos como um único número:

```
CREATE COLLATION mycollation5 (provider = icu, deterministic = false, locale = 'en-US-u-kn-ks-level2');
SELECT 'aB' = 'Ab' COLLATE mycollation5 as result;
 result
--------
 t
(1 row)

SELECT 'N-45' < 'N-123' COLLATE mycollation5 as result;
 result
--------
 t
(1 row)
```

Consulte a [Seção 23.2.3][(collation.md#ICU-CUSTOM-COLLATIONS "23.2.3. ICU Custom Collations")] para obter detalhes e exemplos adicionais sobre o uso de tags de idioma com informações de ordenação personalizadas para o local.

### 23.1.6. Problemas [#](#LOCALE-PROBLEMS)

Se o suporte de localização não funcionar de acordo com a explicação acima, verifique se o suporte de localização no seu sistema operacional está configurado corretamente. Para verificar quais locais estão instalados no seu sistema, você pode usar o comando `locale -a` se o seu sistema operacional o fornecer.

Verifique se o PostgreSQL está realmente usando o idioma que você acha que está usando. As configurações `LC_COLLATE` e `LC_CTYPE` são determinadas quando um banco de dados é criado e não podem ser alteradas, exceto criando um novo banco de dados. Outras configurações de idioma, incluindo `LC_MESSAGES` e `LC_MONETARY`, são inicialmente determinadas pelo ambiente no qual o servidor é iniciado, mas podem ser alteradas em tempo real. Você pode verificar as configurações de idioma ativo usando o comando `SHOW`.

O diretório `src/test/locale` na distribuição de origem contém um conjunto de testes para o suporte de localização do PostgreSQL.

Os aplicativos do cliente que lidam com erros do lado do servidor, analisando o texto da mensagem de erro, obviamente terão problemas quando as mensagens do servidor estiverem em um idioma diferente. Os autores desses aplicativos são aconselhados a utilizar o esquema de código de erro em vez disso.

Manter catálogos de traduções de mensagens requer os esforços contínuos de muitos voluntários que desejam ver o PostgreSQL falar bem sua língua preferida. Se as mensagens em sua língua atualmente não estiverem disponíveis ou não estiverem totalmente traduzidas, sua assistência seria apreciada. Se você quiser ajudar, consulte [Capítulo 56][(nls.md "Chapter 56. Native Language Support")] ou escreva para a lista de correio dos desenvolvedores.