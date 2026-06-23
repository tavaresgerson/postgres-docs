## Capítulo 44. PL/Python — Linguagem Procedimental Python

**Índice**

* [44.1. Funções PL/Python](plpython-funcs.md)
* [44.2. Valores de dados](plpython-data.md)

+ [44.2.1. Mapeamento do Tipo de Dados](plpython-data.md#PLPYTHON-DATA-TYPE-MAPPING)
+ [44.2.2. Nulo, Nenhum](plpython-data.md#PLPYTHON-DATA-NULL)
+ [44.2.3. Arrays, Listas](plpython-data.md#PLPYTHON-ARRAYS)
+ [44.2.4. Tipos Compostos](plpython-data.md#PLPYTHON-DATA-COMPOSITE-TYPES)
+ [44.2.5. Funções de Conjunto que Retornam Conjuntos](plpython-data.md#PLPYTHON-DATA-SET-RETURNING-FUNCS)

* [44.3. Compartilhamento de Dados](plpython-sharing.md)
* [44.4. Blocos de Código Anônimo](plpython-do.md)
* [44.5. Funções de Desempenho](plpython-trigger.md)
* [44.6. Acesso ao Banco de Dados](plpython-database.md)

+ [44.6.1. Funções de Acesso ao Banco de Dados](plpython-database.md#PLPYTHON-DATABASE-ACCESS-FUNCS)
+ [44.6.2. Captura de Erros](plpython-database.md#PLPYTHON-TRAPPING)

* [44.7. Subtransações explícitas](plpython-subtransaction.md)

+ [44.7.1. Geradores de contexto de subtransação](plpython-subtransaction.md#PLPYTHON-SUBTRANSACTION-CONTEXT-MANAGERS)

* [44.8. Gerenciamento de Transações](plpython-transactions.md)
* [44.9. Funções de Utilidade](plpython-util.md)
* [44.10. Python 2 vs. Python 3](plpython-python23.md)
* [44.11. Variáveis de Ambiente](plpython-envar.md)

O PL/Python, linguagem procedural, permite que funções e procedimentos do PostgreSQL sejam escritos na linguagem [Python](https://www.python.org).

Para instalar o PL/Python em um banco de dados específico, use `CREATE EXTENSION plpython3u`.

### DICA

Se uma língua for instalada no `template1`, todas as bases de dados posteriormente criadas terão a língua instalada automaticamente.

PL/Python está disponível apenas como uma linguagem “não confiável”, o que significa que não oferece nenhuma maneira de restringir o que os usuários podem fazer nela e, portanto, é denominada `plpython3u`. Uma variante confiável `plpython` pode se tornar disponível no futuro se um mecanismo de execução seguro for desenvolvido no Python. O autor de uma função em PL/Python não confiável deve ter cuidado para que a função não possa ser usada para fazer algo indesejado, uma vez que ela poderá fazer qualquer coisa que um usuário conectado como administrador do banco de dados possa fazer. Apenas superusuários podem criar funções em linguagens não confiáveis, como `plpython3u`.

Nota

Os usuários dos pacotes de fonte devem habilitar especialmente a construção do PL/Python durante o processo de instalação. (Consulte as instruções de instalação para mais informações.) Os usuários dos pacotes binários podem encontrar o PL/Python em um subpacote separado.