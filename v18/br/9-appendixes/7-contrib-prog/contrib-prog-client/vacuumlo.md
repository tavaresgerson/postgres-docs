## vacuumlo

vacuumlo — remova objetos grandes órfãos de um banco de dados PostgreSQL

## Sinopse

`vacuumlo` [*`option`*...] *`dbname`*...

## Descrição

O vacuumlo é um programa utilitário simples que removerá quaisquer objetos grandes “sozinhos” de um banco de dados PostgreSQL. Um objeto grande (OL) considerado solitário é aquele cujo OID não aparece em nenhuma coluna de dados `oid` ou `lo` do banco de dados.

Se você usa isso, também pode estar interessado no gatilho `lo_manage` no módulo [lo](lo.md "F.21. lo — manage large objects"). `lo_manage` é útil para tentar evitar a criação de LOs órfãos em primeiro lugar.

Todos os bancos de dados mencionados na linha de comando são processados.

## Opções

vacuumlo aceita os seguintes argumentos de linha de comando:

`-l limit` `--limit=limit`: Não remova mais de *`limit`* objetos grandes por transação (padrão 1000). Como o servidor adquire um bloqueio por LO removido, remover muitos LOs em uma transação arrisca exceder [max_locks_per_transaction](runtime-config-locks.md#GUC-MAX-LOCKS-PER-TRANSACTION). Defina o limite em zero se você deseja que todas as remoções sejam feitas em uma única transação.

`-n` `--dry-run`: Não remova nada, apenas mostre o que seria feito.

`-v` `--verbose`: Escreva muitas mensagens de progresso.

`-V` `--version`: Imprimir a versão vacuumlo e sair.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando vacuumlo e sair.

O vacuumlo também aceita os seguintes argumentos de linha de comando para parâmetros de conexão:

`-h host` `--host=host`: Host do servidor de banco de dados.

`-p port` `--port=port`: Porta do servidor de banco de dados.

`-U username` `--username=username`: Nome do usuário para se conectar como.

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Força o vácuo a solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o vacuumlo solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o vacuumlo desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

## Meio Ambiente

`PGHOST` `PGPORT` `PGUSER`: Parâmetros de conexão padrão.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a [Seção 32.15](libpq-envars.md)).

A variável de ambiente `PG_COLOR` especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

O vacuumlo funciona da seguinte maneira: Primeiro, o vacuumlo constrói uma tabela temporária que contém todos os OIDs dos grandes objetos no banco de dados selecionado. Em seguida, ele examina todas as colunas no banco de dados que são do tipo `oid` ou `lo`, e remove as entradas correspondentes da tabela temporária. (Nota: Apenas os tipos com esses nomes são considerados; em particular, os domínios sobre eles não são considerados.) As entradas restantes na tabela temporária identificam LOs órfãos. Estes são removidos.

## Autor

Peter Mount `<peter@retep.org.uk>`