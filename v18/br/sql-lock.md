## LOCK

LOCK — bloqueie uma tabela

## Sinopse

```
LOCK [ TABLE ] [ ONLY ] name [ * ] [, ...] [ IN lockmode MODE ] [ NOWAIT ]

where lockmode is one of:

    ACCESS SHARE | ROW SHARE | ROW EXCLUSIVE | SHARE UPDATE EXCLUSIVE
    | SHARE | SHARE ROW EXCLUSIVE | EXCLUSIVE | ACCESS EXCLUSIVE
```

## Descrição

`LOCK TABLE` obtém um bloqueio de nível de tabela, aguardando, se necessário, que quaisquer bloqueios conflitantes sejam liberados. Se `NOWAIT` for especificado, `LOCK TABLE` não aguarda para adquirir o bloqueio desejado: se não puder ser adquirido imediatamente, o comando é abortado e um erro é emitido. Uma vez obtido, o bloqueio é mantido pelo restante da transação atual. (Não há comando `UNLOCK TABLE`; os bloqueios são sempre liberados no final da transação.)

Quando uma visão é bloqueada, todas as relações que aparecem na consulta de definição da visão também são bloqueadas recursivamente com o mesmo modo de bloqueio.

Ao adquirir bloqueios automaticamente para comandos que fazem referência a tabelas, o PostgreSQL sempre usa o modo de bloqueio menos restritivo possível. `LOCK TABLE` prevê casos em que você pode precisar de bloqueio mais restritivo. Por exemplo, suponha que um aplicativo execute uma transação no nível de isolamento `READ COMMITTED` e precise garantir que os dados em uma tabela permaneçam estáveis durante a duração da transação. Para isso, você pode obter o modo de bloqueio `SHARE` sobre a tabela antes de fazer a consulta. Isso impedirá mudanças de dados concorrentes e garantirá que as leituras subsequentes da tabela mostrem uma visão estável dos dados comprometidos, porque o modo de bloqueio `SHARE` conflitam com o bloqueio `ROW EXCLUSIVE` adquirido pelos escritores, e sua declaração `LOCK TABLE name IN SHARE MODE` aguardará até que quaisquer detentores concorrentes de blocos de modo `ROW EXCLUSIVE` comprem ou retornem. Assim, uma vez que você obtenha o bloqueio, não há escritas não comprometidas em andamento; além disso, nenhuma pode começar até que você libere o bloqueio.

Para obter um efeito semelhante ao executar uma transação no nível de isolamento `REPEATABLE READ` ou `SERIALIZABLE`, você deve executar a instrução `LOCK TABLE` antes de executar qualquer instrução de modificação de dados `SELECT`. A visão dos dados de uma transação `REPEATABLE READ` ou `SERIALIZABLE` será congelada quando sua primeira instrução de modificação de dados ou `SELECT` começar. Uma `LOCK TABLE` mais tarde na transação ainda impedirá escritas concorrentes — mas não garantirá que o que a transação lê corresponda aos valores mais recentes comprometidos.

Se uma transação desse tipo vai alterar os dados na tabela, então ela deve usar o modo de bloqueio `SHARE ROW EXCLUSIVE` em vez do modo `SHARE`. Isso garante que apenas uma transação desse tipo execute de cada vez. Sem isso, é possível um impasse: duas transações podem adquirir o modo `SHARE`, e então não conseguem também adquirir o modo `ROW EXCLUSIVE` para realmente realizar suas atualizações. (Observe que as próprias tranças nunca entram em conflito, então uma transação pode adquirir o modo `ROW EXCLUSIVE` quando mantém o modo `SHARE`, mas não se alguém mais estiver segurando o modo `SHARE`. Para evitar impasses, certifique-se de que todas as transações adquiram blocos nos mesmos objetos na mesma ordem, e se vários modos de bloqueio estão envolvidos para um único objeto, então as transações devem sempre adquirir o modo mais restritivo primeiro.

Mais informações sobre os modos de bloqueio e as estratégias de bloqueio podem ser encontradas em [Seção 13.3][(explicit-locking.md "13.3. Explicit Locking")].

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de uma tabela existente para ser bloqueada. Se `ONLY` for especificado antes do nome da tabela, apenas essa tabela será bloqueada. Se `ONLY` não for especificado, a tabela e todas as suas tabelas descendentes (se houver) serão bloqueadas. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas descendentes são incluídas.

O comando `LOCK TABLE a, b;` é equivalente a `LOCK TABLE a; LOCK TABLE b;`. As tabelas são bloqueadas uma a uma na ordem especificada no comando `LOCK TABLE`.

*`lockmode`*: O modo de bloqueio especifica quais bloqueios este bloqueio entra em conflito. Os modos de bloqueio são descritos em [Seção 13.3][(explicit-locking.md "13.3. Explicit Locking")].

Se não for especificado nenhum modo de bloqueio, então `ACCESS EXCLUSIVE`, o modo mais restritivo, é utilizado.

`NOWAIT`: Especifica que `LOCK TABLE` não deve esperar que quaisquer bloqueios conflitantes sejam liberados: se o(s) bloqueio(s) especificado(s) não puderem ser adquiridos imediatamente sem esperar, a transação é abortada.

## Notas

Para bloquear uma tabela, o usuário deve ter o privilégio correto para o especificado *`lockmode`*. Se o usuário tiver privilégios de `MAINTAIN`, `UPDATE`, `DELETE` ou `TRUNCATE` na tabela, qualquer *`lockmode`* é permitido. Se o usuário tiver privilégios de `INSERT` na tabela, `ROW EXCLUSIVE MODE` (ou um modo menos conflituoso conforme descrito em [Seção 13.3][(explicit-locking.md "13.3. Explicit Locking")) é permitido. Se um usuário tiver privilégios de `SELECT` na tabela, `ACCESS SHARE MODE` é permitido.

O usuário que realiza o bloqueio da visão deve ter o privilégio correspondente à visão. Além disso, por padrão, o proprietário da visão deve ter os privilégios relevantes nas relações de base subjacentes, enquanto o usuário que realiza o bloqueio não precisa de quaisquer permissões nas relações de base subjacentes. No entanto, se a visão tiver `security_invoker` definida como `true` (consulte [`CREATE VIEW`](sql-createview.md "CREATE VIEW")), o usuário que realiza o bloqueio, e não o proprietário da visão, deve ter os privilégios relevantes nas relações de base subjacentes.

`LOCK TABLE` é inútil fora de um bloco de transação: o bloqueio permaneceria segurado apenas até a conclusão da declaração. Portanto, o PostgreSQL reporta um erro se `LOCK` for usado fora de um bloco de transação. Use `BEGIN`(sql-begin.md "BEGIN") e `COMMIT`(sql-commit.md "COMMIT") (ou `ROLLBACK`(sql-rollback.md "ROLLBACK")) para definir um bloco de transação.

`LOCK TABLE` trata apenas de bloqueios de nível de tabela, e, portanto, os nomes dos modos que envolvem `ROW` são todos nomes equivocados. Esses nomes dos modos devem ser lidos, em geral, como indicando a intenção do usuário de adquirir bloqueios de nível de linha na tabela bloqueada. Além disso, o modo `ROW EXCLUSIVE` é um bloqueio de tabela compartilhável. Tenha em mente que todos os modos de bloqueio têm semântica idêntica, quanto se refere a `LOCK TABLE`, diferindo apenas nas regras sobre quais modos entram em conflito com quais. Para informações sobre como adquirir um bloqueio de nível de linha real, consulte [Seção 13.3.2](explicit-locking.md#LOCKING-ROWS "13.3.2. Row-Level Locks") e [A Cláusula de Bloqueio](sql-select.md#SQL-FOR-UPDATE-SHARE "The Locking Clause") na documentação do [SELECT](sql-select.md "SELECT").

## Exemplos

Obtenha um bloqueio `SHARE` em uma tabela de chave primária ao realizar inserções em uma tabela de chave estrangeira:

```
BEGIN WORK;
LOCK TABLE films IN SHARE MODE;
SELECT id FROM films
    WHERE name = 'Star Wars: Episode I - The Phantom Menace';
-- Do ROLLBACK if record was not returned
INSERT INTO films_user_comments VALUES
    (_id_, 'GREAT! I was waiting for it for so long!');
COMMIT WORK;
```

Tome um bloqueio `SHARE ROW EXCLUSIVE` em uma tabela de chave primária ao realizar uma operação de exclusão:

```
BEGIN WORK;
LOCK TABLE films IN SHARE ROW EXCLUSIVE MODE;
DELETE FROM films_user_comments WHERE id IN
    (SELECT id FROM films WHERE rating < 5);
DELETE FROM films WHERE rating < 5;
COMMIT WORK;
```

## Compatibilidade

Não existe `LOCK TABLE` no padrão SQL, que, em vez disso, usa `SET TRANSACTION` para especificar os níveis de concorrência em transações. O PostgreSQL também suporta isso; veja [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION") para detalhes.

Exceto para os modos de bloqueio `ACCESS SHARE`, `ACCESS EXCLUSIVE` e `SHARE UPDATE EXCLUSIVE`, os modos de bloqueio do PostgreSQL e a sintaxe `LOCK TABLE` são compatíveis com os presentes no Oracle.