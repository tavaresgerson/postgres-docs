## 67.3. Subtransações [#](#SUBXACTS)

As subtransações são iniciadas dentro das transações, permitindo que grandes transações sejam divididas em unidades menores. As subtransações podem ser confirmadas ou canceladas sem afetar suas transações parentais, permitindo que as transações parentais continuem. Isso permite que os erros sejam tratados mais facilmente, o que é um padrão comum no desenvolvimento de aplicações. A palavra subtransação é frequentemente abreviada como *subxact*.

Subtransações podem ser iniciadas explicitamente usando o comando `SAVEPOINT`, mas também podem ser iniciadas de outras maneiras, como a cláusula `EXCEPTION` do PL/pgSQL. O PL/Python e o PL/Tcl também suportam subtransações explícitas. As subtransações também podem ser iniciadas a partir de outras subtransações. A transação de nível superior e suas subtransações filhas formam uma hierarquia ou árvore, e é por isso que referimos a transação principal como a transação de nível superior.

Se uma subtransação receber um ID de transação não virtual, seu ID de transação é referido como um “subxid”. Subtransações somente de leitura não recebem subxids, mas, uma vez que tentem escrever, receberão um. Isso também faz com que todos os pais de um subxid, até a transação de nível superior, recebam IDs de transação não virtuais. Garantimos que um ID de pai sempre seja menor que qualquer um de seus subxids filhos.

O xid imediato de cada subxid é registrado no diretório `pg_subtrans`. Não é feita nenhuma entrada para xids de nível superior, uma vez que eles não têm um pai, e também não é feita nenhuma entrada para subtransações somente de leitura.

Quando uma subtransação é confirmada, todas as suas subtransações filhas confirmadas com subxids também serão consideradas subconfirmadas nessa transação. Quando uma subtransação é abortada, todas as suas subtransações filhas também serão consideradas abortadas.

Quando uma transação de nível superior com um xid é confirmada, todas as suas subtransações filhas subconfiadas também são persistentemente registradas como confirmadas no subdiretório `pg_xact`. Se a transação de nível superior abortar, todas as suas subtransações também são abortadas, mesmo que tenham sido subconfiadas.

Quanto mais subtransações cada transação mantém abertas (não retorcidas ou liberadas), maior será o custo de gerenciamento da transação. Até 64 subxids abertos são armazenados em memória compartilhada para cada backend; após esse ponto, o custo de I/O de armazenamento aumenta significativamente devido a pesquisas adicionais de entradas de subxid em `pg_subtrans`.