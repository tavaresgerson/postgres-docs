## pg_config

pg_config — obtenha informações sobre a versão instalada do PostgreSQL

## Sinopse

`pg_config` [*`option`*...]

## Descrição

O utilitário pg_config exibe os parâmetros de configuração da versão instalada atualmente do PostgreSQL. Ele é destinado, por exemplo, a ser utilizado por pacotes de software que desejam interagir com o PostgreSQL para facilitar a localização dos arquivos de cabeçalho e das bibliotecas necessárias.

## Opções

Para usar o pg_config, forneça uma ou mais das seguintes opções:

`--bindir`: Imprima a localização dos executaveis do usuário. Use isso, por exemplo, para encontrar o programa `psql`. Normalmente, essa é também a localização onde o programa `pg_config` reside.

`--docdir`: Imprimir a localização dos arquivos de documentação.

`--htmldir`: Imprimir a localização dos arquivos de documentação HTML.

`--includedir`: Imprima a localização dos arquivos de cabeçalho C das interfaces do cliente.

`--pkgincludedir`: Imprima a localização de outros arquivos de cabeçalho C.

`--includedir-server`: Imprima a localização dos arquivos de cabeçalho C para programação de servidor.

`--libdir`: Imprima a localização das bibliotecas de código objeto.

`--pkglibdir`: Imprima a localização dos módulos dinamicamente carregáveis, ou onde o servidor os procurará. (Outros arquivos de dados dependentes da arquitetura também podem ser instalados neste diretório.)

`--localedir`: Imprima a localização dos arquivos de suporte de localização. (Isso será uma string vazia se o suporte de localização não foi configurado quando o PostgreSQL foi construído.)

`--mandir`: Imprimir a localização das páginas manuais.

`--sharedir`: Imprimir a localização dos arquivos de suporte independentes de arquitetura.

`--sysconfdir`: Imprimir a localização dos arquivos de configuração de nível de sistema.

`--pgxs`: Imprima a localização dos makefiles de extensão.

`--configure`: Imprima as opções que foram fornecidas ao script `configure` quando o PostgreSQL foi configurado para construção. Isso pode ser usado para reproduzir a configuração idêntica, ou para descobrir com que opções um pacote binário foi construído. (Observe, no entanto, que os pacotes binários frequentemente contêm patches personalizados específicos do fornecedor.) Veja também os exemplos abaixo.

`--cc`: Imprima o valor da variável `CC` que foi usada para construir o PostgreSQL. Isso mostra o compilador C utilizado.

`--cppflags`: Imprima o valor da variável `CPPFLAGS` que foi usada para construir o PostgreSQL. Isso mostra os switches do compilador C necessários no momento de pré-processamento (tipicamente, os switches `-I`).

`--cflags`: Imprima o valor da variável `CFLAGS` que foi usada para construir o PostgreSQL. Isso mostra as opções de compilador C.

`--cflags_sl`: Imprima o valor da variável `CFLAGS_SL` que foi usada para a construção do PostgreSQL. Isso mostra os switches adicionais do compilador C usados para a construção de bibliotecas compartilhadas.

`--ldflags`: Imprima o valor da variável `LDFLAGS` que foi usada para construir o PostgreSQL. Isso mostra os switches do link.

`--ldflags_ex`: Imprima o valor da variável `LDFLAGS_EX` que foi usada para construir o PostgreSQL. Isso mostra os switches do link que foram usados para construir os executables apenas.

`--ldflags_sl`: Imprima o valor da variável `LDFLAGS_SL` que foi usada para a construção do PostgreSQL. Isso mostra os switches de vinculação usados para a construção de bibliotecas compartilhadas apenas.

`--libs`: Imprima o valor da variável `LIBS` que foi usada para construir o PostgreSQL. Normalmente, contém interruptores `-l` para bibliotecas externas vinculadas ao PostgreSQL.

`--version`: Imprimir a versão do PostgreSQL.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_config e sair.

Se forem fornecidas mais de uma opção, as informações são impressas nessa ordem, um item por linha. Se não forem fornecidas opções, todas as informações disponíveis são impressas, com rótulos.

## Notas

As opções `--docdir`, `--pkgincludedir`, `--localedir`, `--mandir`, `--sharedir`, `--sysconfdir`, `--cc`, `--cppflags`, `--cflags`, `--cflags_sl`, `--ldflags`, `--ldflags_sl` e `--libs` foram adicionadas no PostgreSQL 8.1. A opção `--htmldir` foi adicionada no PostgreSQL 8.4. A opção `--ldflags_ex` foi adicionada no PostgreSQL 9.0.

## Exemplo

Para reproduzir a configuração de compilação da instalação atual do PostgreSQL, execute o seguinte comando:

```
eval ./configure `pg_config --configure`
```

A saída de `pg_config --configure` contém aspas de shell, portanto, argumentos com espaços são representados corretamente. Portanto, é necessário usar `eval` para obter resultados adequados.