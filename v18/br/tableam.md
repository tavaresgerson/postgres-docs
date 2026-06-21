## Capítulo 62. Definição da Interface do Método de Acesso à Tabela

Este capítulo explica a interface entre o sistema principal do PostgreSQL e os métodos de acesso a tabelas, que gerenciam o armazenamento das tabelas. O sistema principal sabe pouco sobre esses métodos de acesso, além do que é especificado aqui, portanto, é possível desenvolver tipos de métodos de acesso totalmente novos escrevendo código de complemento.

Cada método de acesso à tabela é descrito por uma linha no catálogo do sistema `pg_am`(catalog-pg-am.md "52.3. pg_am"). A entrada `pg_am` especifica um nome e uma *função de manipulador* para o método de acesso à tabela. Essas entradas podem ser criadas e excluídas usando os comandos SQL [CREATE ACCESS METHOD](sql-create-access-method.md "CREATE ACCESS METHOD") e [DROP ACCESS METHOD](sql-drop-access-method.md "DROP ACCESS METHOD").

Uma função de manipulador de método de acesso a tabela deve ser declarada para aceitar um único argumento do tipo `internal` e retornar o pseudotípico `table_am_handler`. O argumento é um valor fictício que simplesmente serve para impedir que as funções de manipulador sejam chamadas diretamente a partir de comandos SQL.

Veja como um arquivo de script de extensão SQL pode criar um manipulador de método de acesso a tabela:

```
CREATE OR REPLACE FUNCTION my_tableam_handler(internal)
  RETURNS table_am_handler AS 'my_extension', 'my_tableam_handler'
  LANGUAGE C STRICT;

CREATE ACCESS METHOD myam TYPE TABLE HANDLER my_tableam_handler;
```

O resultado da função deve ser um ponteiro para uma estrutura do tipo `TableAmRoutine`, que contém tudo o que o código principal precisa saber para fazer uso do método de acesso à tabela. O valor de retorno precisa ser de vida útil do servidor, que é tipicamente alcançado definindo-o como uma variável `static const` no escopo global.

Aqui está como um arquivo de fonte com o manipulador do método de acesso à tabela pode parecer:

```
#include "postgres.h"

#include "access/tableam.h"
#include "fmgr.h"

PG_MODULE_MAGIC;

static const TableAmRoutine my_tableam_methods = {
    .type = T_TableAmRoutine,

    /* Methods of TableAmRoutine omitted from example, add them here. */
};

PG_FUNCTION_INFO_V1(my_tableam_handler);

Datum
my_tableam_handler(PG_FUNCTION_ARGS)
{
    PG_RETURN_POINTER(&my_tableam_methods);
}
```

A estrutura `TableAmRoutine`, também chamada de estrutura *API* do método de acesso, define o comportamento do método de acesso usando callbacks. Esses callbacks são ponteiros para funções C simples e não são visíveis ou acessíveis no nível SQL. Todos os callbacks e seu comportamento são definidos na estrutura `TableAmRoutine` (com comentários dentro da estrutura que definem os requisitos para callbacks). A maioria dos callbacks tem funções de wrapper, que são documentadas do ponto de vista de um usuário (em vez de um implementador) do método de acesso à tabela. Para detalhes, consulte o arquivo `src/include/access/tableam.h`(https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/include/access/tableam.h;hb=HEAD).

Para implementar um método de acesso, um implementador normalmente precisa implementar um tipo específico de slot de tabela de tuplas para AM (ver `src/include/executor/tuptable.h` (https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/include/executor/tuptable.h;hb=HEAD)), que permite que o código externo ao método de acesso mantenha referências a tuplas da AM e acesse as colunas da tupla.

Atualmente, a forma como um AM realmente armazena dados é bastante não limitada. Por exemplo, é possível, mas não obrigatório, usar o cache de buffer compartilhado do postgres. No caso de ser usado, provavelmente faz sentido usar o layout padrão de página do PostgreSQL, conforme descrito em [Seção 66.6][(storage-page-layout.md "66.6. Database Page Layout")].

Uma restrição bastante grande do método de acesso à tabela API é que, atualmente, se o AM quiser suportar modificações e/ou índices, é necessário que cada tupla tenha um identificador de tupla (TID), que consiste em um número de bloco e um número de item (ver também [Seção 66.6] [(storage-page-layout.md "66.6. Database Page Layout")]). Não é estritamente necessário que as subpartes dos TIDs tenham o mesmo significado que, por exemplo, têm para `heap`, mas se o suporte de varredura de bitmap é desejado (é opcional), o número de bloco precisa fornecer localização.

Para a segurança em caso de falha, um AM pode usar o [WAL] de postgres (wal.md "Chapter 28. Reliability and the Write-Ahead Log"), ou uma implementação personalizada. Se o WAL for escolhido, pode-se usar o [Registros de WAL genéricos] (generic-wal.md "64.1. Generic WAL Records") ou implementar um [Gestor de recursos de WAL personalizado] (custom-rmgr.md "64.2. Custom WAL Resource Managers").

Para implementar suporte transacional de uma maneira que permita o acesso a diferentes métodos de acesso a tabela dentro de uma única transação, é provavelmente necessário integrar-se de perto com a maquinaria em `src/backend/access/transam/xlog.c`.

Qualquer desenvolvedor de um novo `table access method` pode consultar a implementação existente do `heap` presente em `src/backend/access/heap/heapam_handler.c` para obter detalhes sobre sua implementação.