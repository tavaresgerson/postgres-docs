## pg_walsummary

pg_walsummary — imprimir conteúdos dos arquivos de resumo WAL

## Sinopse

`pg_walsummary` [*`option`*...] [*`file`*...]

## Descrição

O pg_walsummary é usado para imprimir o conteúdo dos arquivos de resumo WAL. Esses arquivos binários são encontrados no subdiretório `pg_wal/summaries` do diretório de dados e podem ser convertidos em texto usando essa ferramenta. Isso normalmente não é necessário, uma vez que os arquivos de resumo WAL existem principalmente para suportar [backup incremental](continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP), mas pode ser útil para fins de depuração.

Um arquivo de resumo WAL é indexado pelo OID do espaço de tabela, pelo OID da relação e pelo fork da relação. Para cada fork da relação, ele armazena a lista de blocos que foram modificados pelo WAL dentro do intervalo resumido no arquivo. Também pode armazenar um "bloco limite", que é 0 se o fork da relação foi criado ou truncado dentro do intervalo relevante do WAL, e, caso contrário, o comprimento mais curto para o qual o fork da relação foi truncado. Se o fork da relação não foi criado, excluído ou truncado dentro do intervalo relevante do WAL, o bloco limite é indefinido ou infinito e não será impresso por esta ferramenta.

## Opções

`-i` `--individual`: Por padrão, `pg_walsummary` imprime uma linha de saída para cada intervalo de um ou mais blocos modificados consecutivos. Isso pode tornar a saída muito mais concisa, pois uma relação onde todos os blocos de 0 a 999 foram modificados produzirá apenas uma linha de saída em vez de 1000 linhas separadas. Esta opção solicita uma linha de saída separada para cada bloco modificado.

`-q` `--quiet`: Não imprima nenhum resultado, exceto erros. Isso pode ser útil quando você deseja saber se um arquivo de resumo WAL pode ser analisado com sucesso, mas não se importa com o conteúdo.

`-V` `--version`: Exibir as informações da versão, e então sair.

`-?` `--help`: Mostra ajuda sobre os argumentos da linha de comando do comando pg_walsummary e a saída.

## Meio Ambiente

A variável de ambiente `PG_COLOR` especifica se é necessário usar cor nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Veja também

[pg_basebackup](app-pgbasebackup.md "pg_basebackup"), [pg_combinebackup](app-pgcombinebackup.md "pg_combinebackup")