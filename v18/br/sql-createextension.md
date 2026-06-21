## CRIAR EXTENSÃO

CREATE EXTENSION — instalar uma extensão

## Sinopse

```
CREATE EXTENSION [ IF NOT EXISTS ] extension_name
    [ WITH ] [ SCHEMA schema_name ]
             [ VERSION version ]
             [ CASCADE ]
```

## Descrição

`CREATE EXTENSION` carrega uma nova extensão no banco de dados atual. Não deve haver uma extensão com o mesmo nome já carregada.

Carregar uma extensão equivale, essencialmente, a executar o arquivo de script da extensão. O script normalmente cria novos objetos SQL, como funções, tipos de dados, operadores e métodos de suporte a índices. `CREATE EXTENSION` registra, adicionalmente, as identidades de todos os objetos criados, para que possam ser excluídos novamente se `DROP EXTENSION` for emitido.

O usuário que executa `CREATE EXTENSION` torna-se o proprietário da extensão para fins de verificação de privilégios posteriores, e normalmente também torna-se o proprietário de quaisquer objetos criados pelo script da extensão.

Carregar uma extensão normalmente requer os mesmos privilégios que seriam necessários para criar seus objetos componentes. Para muitas extensões, isso significa que são necessários privilégios de superusuário. No entanto, se a extensão estiver marcada como *confiável* em seu arquivo de controle, ela pode ser instalada por qualquer usuário que tenha privilégio `CREATE` no banco de dados atual. Neste caso, o próprio objeto da extensão será de propriedade do usuário que a fez, mas os objetos contidos serão de propriedade do superusuário de inicialização (a menos que o script da extensão os atribua explicitamente ao usuário que a fez). Esta configuração dá ao usuário que a fez o direito de descartar a extensão, mas não de modificar objetos individuais dentro dela.

## Parâmetros

`IF NOT EXISTS`: Não exija um erro se uma extensão com o mesmo nome já existir. Neste caso, é emitido um aviso. Observe que não há garantia de que a extensão existente seja algo semelhante àquela que teria sido criada a partir do arquivo de script atualmente disponível.

*`extension_name`*: O nome da extensão a ser instalada. O PostgreSQL criará a extensão usando os detalhes do arquivo `extension_name.control`, encontrado através do caminho de controle de extensão do servidor (definido por [extension_control_path](runtime-config-client.md#GUC-EXTENSION-CONTROL-PATH).).

*`schema_name`*: O nome do esquema no qual os objetos da extensão serão instalados, uma vez que a extensão permite que seu conteúdo seja realocado. O esquema nomeado deve já existir. Se não for especificado e o arquivo de controle da extensão não especificar um esquema, o esquema atual de criação de objetos padrão será usado.

Se a extensão especificar um parâmetro `schema` em seu arquivo de controle, então esse esquema não pode ser sobrescrito com uma cláusula `SCHEMA`. Normalmente, um erro será exibido se uma cláusula `SCHEMA` for dada e conflitar com o parâmetro `schema` da extensão. No entanto, se a cláusula `CASCADE` também for dada, então *`schema_name`* é ignorado quando há conflito. O *`schema_name`* dado será usado para a instalação de quaisquer extensões necessárias que não especifiquem `schema` em seus arquivos de controle.

Lembre-se de que a própria extensão não é considerada parte de nenhum esquema: as extensões têm nomes não qualificados que devem ser únicos em todo o banco de dados. Mas os objetos que pertencem à extensão podem estar em esquemas.

*`version`*: A versão da extensão a ser instalada. Isso pode ser escrito como um identificador ou uma literal de cadeia de caracteres. A versão padrão é aquela especificada no arquivo de controle da extensão.

`CASCADE`: Instale automaticamente todas as extensões que esta extensão depende e que não estão já instaladas. Suas dependências são igualmente instaladas automaticamente, recursivamente. A cláusula `SCHEMA`, se fornecida, aplica-se a todas as extensões que são instaladas dessa maneira. Outras opções da declaração não são aplicadas a extensões instaladas automaticamente; em particular, suas versões padrão são sempre selecionadas.

## Notas

Antes de poder usar `CREATE EXTENSION` para carregar uma extensão em um banco de dados, os arquivos de suporte da extensão devem ser instalados. Informações sobre a instalação das extensões fornecidas com o PostgreSQL podem ser encontradas em [Módulos adicionais fornecidos](contrib.md).

As extensões atualmente disponíveis para carregamento podem ser identificadas a partir das visualizações do sistema `pg_available_extensions` (view-pg-available-extensions.md "53.3. pg_available_extensions") ou `pg_available_extension_versions` (view-pg-available-extension-versions.md "53.4. pg_available_extension_versions").

### Atenção

Instalar uma extensão como superusuário exige confiar que o autor da extensão escreveu o script de instalação da extensão de uma maneira segura. Não é muito difícil para um usuário malicioso criar objetos de cavalo de Troia que comprometam a execução posterior de um script de extensão mal escrito, permitindo que o usuário adquira privilégios de superusuário. No entanto, os objetos de cavalo de Troia são apenas perigosos se estiverem no `search_path` durante a execução do script, o que significa que estão no esquema de alvo de instalação da extensão ou no esquema de alguma extensão de que depende. Portanto, uma boa regra de ouro ao lidar com extensões cujos scripts não foram cuidadosamente verificados é instalá-las apenas em esquemas para os quais o privilégio CREATE não foi concedido e não será concedido a nenhum usuário não confiável. Da mesma forma, para quaisquer extensões de que dependem.

Acredita-se que as extensões fornecidas com o PostgreSQL sejam seguras contra ataques no momento da instalação desse tipo, exceto por algumas que dependem de outras extensões. Como afirmado na documentação dessas extensões, elas devem ser instaladas em esquemas seguros, ou instaladas nos mesmos esquemas das extensões das quais dependem, ou em ambos.

Para informações sobre como escrever novas extensões, consulte [Seção 36.17](extend-extensions.md).

## Exemplos

Instale a extensão [hstore](hstore.md) no banco de dados atual, colocando seus objetos no esquema `addons`:

```
CREATE EXTENSION hstore SCHEMA addons;
```

Outra maneira de realizar a mesma coisa:

```
SET search_path = addons;
CREATE EXTENSION hstore;
```

## Compatibilidade

`CREATE EXTENSION` é uma extensão do PostgreSQL.

## Veja também

[ALTER EXTENSION](sql-alterextension.md "ALTER EXTENSION"), [DROP EXTENSION](sql-dropextension.md "DROP EXTENSION")