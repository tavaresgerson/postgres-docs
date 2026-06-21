## 37.2. Visibilidade das Alterações de Dados [#](#TRIGGER-DATACHANGES)

Se você executar comandos SQL em sua função de gatilho e esses comandos acessem a tabela para a qual o gatilho está direcionado, você precisa estar ciente das regras de visibilidade dos dados, pois elas determinam se esses comandos SQL verão as alterações de dados para as quais o gatilho é disparado. Em resumo:

* Os gatilhos de nível de declaração seguem regras simples de visibilidade: nenhuma das alterações feitas por uma declaração é visível aos gatilhos `BEFORE` de nível de declaração, enquanto todas as modificações são visíveis aos gatilhos `AFTER` de nível de declaração.
* A mudança de dados (inserção, atualização ou exclusão) que causa o disparo do gatilho não é naturalmente *visível* aos comandos SQL executados em um gatilho `BEFORE` de nível de linha, porque ainda não aconteceu.
* No entanto, os comandos SQL executados em um gatilho `BEFORE` de nível de linha *verão* os efeitos das alterações de dados para as linhas processadas anteriormente no mesmo comando externo. Isso requer cautela, pois a ordem desses eventos de mudança não é previsível em geral; um comando SQL que afeta múltiplas linhas pode visitar as linhas em qualquer ordem.
* Da mesma forma, um gatilho `INSTEAD OF` de nível de linha verá os efeitos das alterações de dados feitas por disparos anteriores dos gatilhos `INSTEAD OF` no mesmo comando externo.
* Quando um gatilho `AFTER` de nível de linha é disparado, todas as alterações de dados feitas pelo comando externo já estão completas e são visíveis à função do gatilho invocada.

Se sua função de disparo for escrita em qualquer um dos idiomas processuais padrão, então as declarações acima se aplicam apenas se a função for declarada `VOLATILE`. As funções que são declaradas `STABLE` ou `IMMUTABLE` não verão alterações feitas pelo comando de chamada em qualquer caso.

Mais informações sobre as regras de visibilidade dos dados podem ser encontradas em [Seção 45.5][(spi-visibility.md "45.5. Visibility of Data Changes")]. O exemplo em [Seção 37.4][(trigger-example.md "37.4. A Complete Trigger Example")] contém uma demonstração dessas regras.