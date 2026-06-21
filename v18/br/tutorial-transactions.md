## 3.4. Transações [#](#TUTORIAL-TRANSACTIONS)

*Transações* são um conceito fundamental de todos os sistemas de banco de dados. O ponto essencial de uma transação é que ela agrupa múltiplos passos em uma operação única, tudo ou nada. Os estados intermediários entre os passos não são visíveis para outras transações concorrentes, e se ocorrer algum erro que impeça a conclusão da transação, então nenhum dos passos afeta o banco de dados.

Por exemplo, considere um banco de dados que contém saldos para várias contas de clientes, bem como saldos totais de depósitos para agências. Suponha que queira registrar um pagamento de $100,00 da conta de Alice para a conta de Bob. Simplificando de forma absurda, os comandos SQL para isso podem parecer assim:

```
UPDATE accounts SET balance = balance - 100.00
    WHERE name = 'Alice';
UPDATE branches SET balance = balance - 100.00
    WHERE name = (SELECT branch_name FROM accounts WHERE name = 'Alice');
UPDATE accounts SET balance = balance + 100.00
    WHERE name = 'Bob';
UPDATE branches SET balance = balance + 100.00
    WHERE name = (SELECT branch_name FROM accounts WHERE name = 'Bob');
```

Os detalhes desses comandos não são importantes aqui; o ponto importante é que há várias atualizações separadas envolvidas para realizar essa operação bastante simples. Os oficiais do nosso banco querem ter certeza de que todas essas atualizações acontecem, ou nenhuma delas acontece. Certamente não faria sentido que uma falha no sistema resultasse em Bob receber $100,00 que não foi debitado de Alice. Além disso, Alice não ficaria feliz por muito tempo se fosse debitada sem que Bob fosse creditado. Precisamos de uma garantia de que, se algo der errado em meio à operação, nenhuma das etapas executadas até então terá efeito. Agrupar as atualizações em uma *transação* nos dá essa garantia. Diz-se que uma transação é *atômica*: do ponto de vista de outras transações, ela acontece completamente ou não acontece de todo.

Também queremos uma garantia de que, uma vez que uma transação seja concluída e reconhecida pelo sistema de banco de dados, ela realmente tenha sido registrada permanentemente e não seja perdida, mesmo que ocorra um acidente pouco depois. Por exemplo, se estamos registrando uma retirada de dinheiro por Bob, não queremos nenhuma chance de o débito em sua conta desaparecer em um acidente logo depois que ele sai da porta do banco. Um banco de dados transacional garante que todas as atualizações feitas por uma transação sejam registradas em armazenamento permanente (ou seja, em disco) antes de a transação ser relatada como concluída.

Outra propriedade importante dos bancos de dados transacionais está intimamente relacionada à noção de atualizações atômicas: quando várias transações estão sendo executadas simultaneamente, cada uma delas não deve ser capaz de ver as mudanças incompletas feitas por outras. Por exemplo, se uma transação está ocupada totalizando todos os saldos das filiais, não faria sentido que incluísse o débito da filial de Alice, mas não o crédito da filial de Bob, nem vice-versa. Portanto, as transações devem ser tudo ou nada não apenas em termos de seu efeito permanente no banco de dados, mas também em termos de sua visibilidade à medida que ocorrem. As atualizações feitas até agora por uma transação aberta são invisíveis para outras transações até que a transação seja concluída, momento em que todas as atualizações se tornam visíveis simultaneamente.

Em PostgreSQL, uma transação é configurada ao envolver os comandos SQL da transação com os comandos `BEGIN` e `COMMIT`. Assim, nossa transação bancária ficaria assim:

```
BEGIN;
UPDATE accounts SET balance = balance - 100.00
    WHERE name = 'Alice';
-- etc etc
COMMIT;
```

Se, em meio à transação, decidirmos que não queremos comprometer (talvez tenhamos apenas notado que o saldo de Alice ficou negativo), podemos emitir o comando `ROLLBACK` em vez de `COMMIT`, e todas as nossas atualizações até agora serão canceladas.

O PostgreSQL, na verdade, trata cada declaração SQL como se ela fosse executada dentro de uma transação. Se você não emitir um comando `BEGIN`, então cada declaração individual tem um `BEGIN` implícito e (se bem-sucedido) `COMMIT` envolto nela. Um grupo de declarações cercadas por `BEGIN` e `COMMIT` é às vezes chamado de *bloco de transação*.

### Nota

Algumas bibliotecas de cliente emitem os comandos `BEGIN` e `COMMIT` automaticamente, de modo que você pode obter o efeito dos blocos de transação sem precisar perguntar. Verifique a documentação da interface que você está usando.

É possível controlar as declarações em uma transação de uma maneira mais granular através do uso de *savepoints*. Os savepoints permitem que você descarte seletivamente partes da transação, ao mesmo tempo em que compromete o restante. Após definir um savepoint com `SAVEPOINT`, você pode, se necessário, retornar ao savepoint com `ROLLBACK TO`. Todas as alterações no banco de dados da transação entre a definição do savepoint e o retorno a ele são descartadas, mas as alterações anteriores ao savepoint são mantidas.

Após retornar a um ponto de salvamento, ele continua sendo definido, então você pode retornar a ele várias vezes. Por outro lado, se você tem certeza de que não precisará retornar a um ponto de salvamento específico novamente, ele pode ser liberado, para que o sistema possa liberar alguns recursos. Tenha em mente que liberar ou retornar a um ponto de salvamento automaticamente libera todos os pontos de salvamento que foram definidos após ele.

Tudo isso está acontecendo dentro do bloco de transação, então nada disso é visível para outras sessões do banco de dados. Quando e se você compromet a transação, as ações comprometidas se tornam visíveis como uma unidade para outras sessões, enquanto as ações desfeitas nunca se tornam visíveis.

Lembrando-se do banco de dados bancário, suponha que detemos $100,00 da conta de Alice e creditamos a conta de Bob, apenas para descobrir mais tarde que deveríamos ter creditado a conta de Wally. Podemos fazer isso usando pontos de salvamento assim:

```
BEGIN;
UPDATE accounts SET balance = balance - 100.00
    WHERE name = 'Alice';
SAVEPOINT my_savepoint;
UPDATE accounts SET balance = balance + 100.00
    WHERE name = 'Bob';
-- oops ... forget that and use Wally's account
ROLLBACK TO my_savepoint;
UPDATE accounts SET balance = balance + 100.00
    WHERE name = 'Wally';
COMMIT;
```

Esse exemplo, é claro, é simplificado demais, mas é possível ter muito controle em um bloco de transação através do uso de pontos de salvamento. Além disso, `ROLLBACK TO` é a única maneira de recuperar o controle de um bloco de transação que foi colocado em estado abortado pelo sistema devido a um erro, a não ser que ele seja completamente desfeito e reiniciado.