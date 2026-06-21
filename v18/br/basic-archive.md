## F.5. basic_archive — um exemplo de módulo de arquivo WAL [#](#BASIC-ARCHIVE)

* [F.5.1. Parâmetros de Configuração](basic-archive.md#BASIC-ARCHIVE-CONFIGURATION-PARAMETERS)
* [F.5.2. Notas](basic-archive.md#BASIC-ARCHIVE-NOTES)
* [F.5.3. Autor](basic-archive.md#BASIC-ARCHIVE-AUTHOR)

`basic_archive` é um exemplo de um módulo de arquivo. Este módulo copia os arquivos de segmento WAL concluídos para o diretório especificado. Isso pode não ser especialmente útil, mas pode servir como um ponto de partida para o desenvolvimento de seu próprio módulo de arquivo. Para mais informações sobre módulos de arquivo, consulte [Capítulo 49][(archive-modules.md "Chapter 49. Archive Modules")].

Para funcionar, este módulo deve ser carregado através de [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY), e [archive_mode](runtime-config-wal.md#GUC-ARCHIVE-MODE) deve ser habilitado.

### F.5.1. Parâmetros de Configuração [#](#BASIC-ARCHIVE-CONFIGURATION-PARAMETERS)

`basic_archive.archive_directory` (`string`): O diretório onde o servidor deve copiar os arquivos de segmento WAL. Este diretório deve já existir. O padrão é uma string vazia, que efetivamente interrompe a arquivamento do WAL, mas se [archive_mode](runtime-config-wal.md#GUC-ARCHIVE-MODE) estiver habilitado, o servidor acumulará os arquivos de segmento WAL na expectativa de que um valor seja fornecido em breve.

Esses parâmetros devem ser definidos em `postgresql.conf`. O uso típico pode ser:

```
# postgresql.conf
archive_mode = 'on'
archive_library = 'basic_archive'
basic_archive.archive_directory = '/path/to/archive/directory'
```

### F.5.2. Notas [#](#BASIC-ARCHIVE-NOTES)

As falhas do servidor podem deixar arquivos temporários com o prefixo `archtemp` no diretório do arquivo. Recomenda-se excluir esses arquivos antes de reiniciar o servidor após uma falha. É seguro remover esses arquivos enquanto o servidor estiver em execução, desde que não estejam relacionados a qualquer arquivamento em andamento, mas os usuários devem ter cuidado extra ao fazer isso.

### F.5.3. Autor [#](#BASIC-ARCHIVE-AUTHOR)

Nathan Bossart