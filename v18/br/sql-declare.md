## DECLARA-SE

DECLARE — definir um cursor

## Sinopse

```
DECLARE name [ BINARY ] [ ASENSITIVE | INSENSITIVE ] [ [ NO ] SCROLL ]
    CURSOR [ { WITH | WITHOUT } HOLD ] FOR query
```

## Descrição

`DECLARE` permite que um usuário crie cursor, que podem ser usados para recuperar um pequeno número de linhas de cada vez a partir de uma consulta maior. Após o cursor ser criado, as linhas são obtidas a partir dele usando `FETCH`(sql-fetch.md "FETCH").

### Nota

Esta página descreve o uso de cursor no nível do comando SQL. Se você está tentando usar cursors dentro de uma função PL/pgSQL, as regras são diferentes — veja [Seção 41.7][(plpgsql-cursors.md "41.7. Cursors")].

## Parâmetros

*`name`*: O nome do cursor a ser criado. Este nome deve ser diferente de qualquer outro nome de cursor ativo na sessão.

`BINARY`: Faz com que o cursor retorne dados em formato binário, em vez de texto.

`ASENSITIVE` `INSENSITIVE`: A sensibilidade do cursor determina se as alterações nos dados subjacentes ao cursor, realizadas na mesma transação, após o cursor ter sido declarado, são visíveis no cursor. `INSENSITIVE` significa que elas não são visíveis, `ASENSITIVE` significa que o comportamento depende da implementação. Um terceiro comportamento, `SENSITIVE`, que significa que tais alterações são visíveis no cursor, não está disponível no PostgreSQL. No PostgreSQL, todos os cursors são insensíveis; portanto, essas palavras-chave não têm efeito e são apenas aceitas para compatibilidade com o padrão SQL.

Especificar `INSENSITIVE` junto com `FOR UPDATE` ou `FOR SHARE` é um erro.

`SCROLL` `NO SCROLL`: `SCROLL` especifica que o cursor pode ser usado para recuperar linhas de uma maneira não sequencial (por exemplo, para trás). Dependendo da complexidade do plano de execução da consulta, especificar `SCROLL` pode impor uma penalidade de desempenho no tempo de execução da consulta. `NO SCROLL` especifica que o cursor não pode ser usado para recuperar linhas de uma maneira não sequencial. O padrão é permitir o rolagem em alguns casos; isso não é o mesmo que especificar `SCROLL`. Veja [Notas](sql-declare.md#SQL-DECLARE-NOTES "Notes") abaixo para detalhes.

`WITH HOLD` `WITHOUT HOLD`: `WITH HOLD` especifica que o cursor pode continuar sendo usado após a transação que o criou ter sido confirmada com sucesso. `WITHOUT HOLD` especifica que o cursor não pode ser usado fora da transação que o criou. Se nem `WITHOUT HOLD` nem `WITH HOLD` são especificados, `WITHOUT HOLD` é o padrão.

*`query`*: Um comando [`SELECT`](sql-select.md "SELECT") ou [`VALUES`](sql-values.md "VALUES") que fornecerá as linhas que serão devolvidas pelo cursor.

As palavras-chave `ASENSITIVE`, `BINARY`, `INSENSITIVE` e `SCROLL` podem aparecer em qualquer ordem.

## Notas

Os cursors normais retornam dados em formato de texto, da mesma forma que um `SELECT` produziria. A opção `BINARY` especifica que o cursor deve retornar dados em formato binário. Isso reduz o esforço de conversão tanto para o servidor quanto para o cliente, ao custo de mais esforço do programador para lidar com formatos de dados binários dependentes da plataforma. Como exemplo, se uma consulta retorna um valor de um de uma coluna inteira, você obteria uma string de `1` com um cursor padrão, enquanto com um cursor binário, você obteria um campo de 4 bytes contendo a representação interna do valor (em ordem de byte big-endian).

Os cursors binários devem ser usados com cuidado. Muitas aplicações, incluindo o psql, não estão preparadas para lidar com cursors binários e esperam que os dados retornem no formato de texto.

### Nota

Quando o aplicativo cliente usa o protocolo de "consulta estendida" para emitir um comando `FETCH`, a mensagem do protocolo Bind especifica se os dados devem ser recuperados em formato de texto ou binário. Essa escolha substitui a maneira como o cursor é definido. O conceito de cursor binário como tal é, portanto, obsoleto ao usar o protocolo de consulta estendida — qualquer cursor pode ser tratado como texto ou binário.

A menos que `WITH HOLD` seja especificado, o cursor criado por este comando só pode ser usado dentro da transação atual. Assim, `DECLARE` sem `WITH HOLD` é inútil fora de um bloco de transação: o cursor sobreviveria apenas até o término da declaração. Portanto, o PostgreSQL reporta um erro se tal comando for usado fora de um bloco de transação. Use [`BEGIN`(sql-begin.md "BEGIN") e [`COMMIT`(sql-commit.md "COMMIT") (ou [`ROLLBACK`(sql-rollback.md "ROLLBACK")) para definir um bloco de transação.

Se `WITH HOLD` for especificado e a transação que criou o cursor cometer com sucesso, o cursor pode continuar a ser acessado por transações subsequentes na mesma sessão. (Mas se a transação de criação for abortada, o cursor é removido.) Um cursor criado com `WITH HOLD` é fechado quando um comando explícito `CLOSE` é emitido sobre ele, ou quando a sessão termina. Na implementação atual, as linhas representadas por um cursor mantido são copiadas para um arquivo temporário ou área de memória para que permaneçam disponíveis para transações subsequentes.

`WITH HOLD` não pode ser especificado quando a consulta inclui `FOR UPDATE` ou `FOR SHARE`.

A opção `SCROLL` deve ser especificada ao definir um cursor que será usado para recuperar dados em sentido inverso. Isso é exigido pelo padrão SQL. No entanto, para compatibilidade com versões anteriores, o PostgreSQL permitirá recuperações em sentido inverso sem `SCROLL`, se o plano de consulta do cursor for simples o suficiente para que não seja necessário suporte adicional. No entanto, os desenvolvedores de aplicativos são aconselhados a não depender da utilização de recuperações em sentido inverso a partir de um cursor que não foi criado com `SCROLL`. Se `NO SCROLL` for especificado, as recuperações em sentido inverso serão desativadas em qualquer caso.

Os buscam retroativos também não são permitidos quando a consulta inclui `FOR UPDATE` ou `FOR SHARE`; portanto, `SCROLL` pode não ser especificado neste caso.

### Atenção

Os cursors roláveis podem fornecer resultados inesperados se invocarem funções voláteis (consulte [Seção 36.7][(xfunc-volatility.md "36.7. Function Volatility Categories")]). Quando uma linha previamente obtida é obtida novamente, as funções podem ser executadas novamente, o que pode levar a resultados diferentes da primeira vez. É melhor especificar `NO SCROLL` para uma consulta que envolva funções voláteis. Se isso não for prático, uma solução é declarar o cursor `SCROLL WITH HOLD` e confirmar a transação antes de ler quaisquer linhas dele. Isso forçará que toda a saída do cursor seja materializada em armazenamento temporário, de modo que as funções voláteis sejam executadas exatamente uma vez para cada linha.

Se a consulta do cursor incluir `FOR UPDATE` ou `FOR SHARE`, as linhas devolvidas serão bloqueadas no momento em que são obtidas pela primeira vez, da mesma maneira que para um comando regular [`SELECT`](sql-select.md "SELECT") com essas opções. Além disso, as linhas devolvidas serão as versões mais atualizadas.

### Atenção

Geralmente, é recomendado usar `FOR UPDATE` se o cursor estiver destinado a ser usado com `UPDATE ... WHERE CURRENT OF` ou `DELETE ... WHERE CURRENT OF`. Usar `FOR UPDATE` impede que outras sessões mudem as linhas entre o momento em que elas são obtidas e o momento em que são atualizadas. Sem `FOR UPDATE`, um comando subsequente `WHERE CURRENT OF` não terá efeito se a linha foi alterada desde que o cursor foi criado.

Outra razão para usar `FOR UPDATE` é que, sem ele, um subsequente `WHERE CURRENT OF` pode falhar se a consulta do cursor não atender às regras do padrão SQL para ser “simplesmente atualizável” (em particular, o cursor deve referenciar apenas uma tabela e não usar agrupamento ou `ORDER BY`). Cursors que não são simplesmente atualizáveis podem funcionar, ou não, dependendo dos detalhes da escolha do plano; portanto, no pior dos casos, um aplicativo pode funcionar em testes e falhar na produção. Se `FOR UPDATE` for especificado, o cursor é garantido para ser atualizável.

A principal razão para não usar `FOR UPDATE` com `WHERE CURRENT OF` é se você precisar que o cursor seja rolável ou que seja isolado de atualizações concorrentes (ou seja, continuar a mostrar os dados antigos). Se essa for uma exigência, preste muita atenção às advertências mostradas acima.

O padrão SQL só prevê disposições para cursor em SQL embutido. O servidor PostgreSQL não implementa uma declaração `OPEN` para cursor; um cursor é considerado aberto quando é declarado. No entanto, o ECPG, o pré-processador de SQL embutido para PostgreSQL, suporta as convenções padrão de cursor SQL, incluindo aquelas que envolvem as declarações `DECLARE` e `OPEN`.

A estrutura de dados do servidor que sustenta um cursor aberto é chamada de *portal*. Os nomes dos portais são expostos no protocolo do cliente: um cliente pode obter linhas diretamente de um portal aberto, se souber o nome do portal. Ao criar um cursor com `DECLARE`, o nome do portal é o mesmo que o nome do cursor.

Você pode ver todos os cursors disponíveis consultando a visão do sistema `pg_cursors`(view-pg-cursors.md "53.7. pg_cursors").

## Exemplos

Para declarar um cursor:

```
DECLARE liahona CURSOR FOR SELECT * FROM films;
```

Veja [FETCH](sql-fetch.md "FETCH") para mais exemplos de uso do cursor.

## Compatibilidade

O padrão SQL permite que os cursors sejam usados apenas em SQL incorporado e em módulos. O PostgreSQL permite que os cursors sejam usados de forma interativa.

De acordo com o padrão SQL, as alterações feitas em cursors insensíveis por meio das declarações `UPDATE ... WHERE CURRENT OF` e `DELETE ... WHERE CURRENT OF` são visíveis nesse mesmo cursor. O PostgreSQL trata essas declarações como todas as outras declarações que alteram dados, ou seja, elas não são visíveis em cursors insensíveis.

Os cursors binários são uma extensão do PostgreSQL.

## Veja também

[FECHAR][(sql-close.md "CLOSE"), [PESQUISAR][(sql-fetch.md "FETCH"), [MOVIMENTAR][(sql-move.md "MOVE")