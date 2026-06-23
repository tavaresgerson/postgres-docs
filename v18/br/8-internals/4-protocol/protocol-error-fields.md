## 54.8. Campos de Mensagem de Erro e Aviso [#](#PROTOCOL-ERROR-FIELDS)

Esta seção descreve os campos que podem aparecer nas mensagens de ErrorResponse e NoticeResponse. Cada tipo de campo tem um identificador de byte único. Note que qualquer tipo de campo dado deve aparecer no máximo uma vez por mensagem.

`S`: Gravidade: os conteúdos do campo são `ERROR`, `FATAL`, ou `PANIC` (em uma mensagem de erro), ou `WARNING`, `NOTICE`, `DEBUG`, `INFO`, ou `LOG` (em uma mensagem de aviso), ou uma tradução localizada de uma dessas. Sempre presente.

`V`: Gravidade: os conteúdos do campo são `ERROR`, `FATAL` ou `PANIC` (em uma mensagem de erro), ou `WARNING`, `NOTICE`, `DEBUG`, `INFO` ou `LOG` (em uma mensagem de aviso). Isso é idêntico ao campo `S`, exceto que os conteúdos nunca são localizados. Isso está presente apenas em mensagens geradas por versões do PostgreSQL 9.6 e posteriores.

`C`: Código: o código SQLSTATE para o erro (ver [Apêndice A](errcodes-appendix.md)). Não traduzível. Sempre presente.

`M`: Mensagem: a mensagem de erro primária legível pelo ser humano. Deve ser precisa, mas concisa (tipicamente uma linha). Sempre presente.

`D`: Detalhe: uma mensagem de erro secundária opcional que traz mais detalhes sobre o problema. Pode ocupar várias linhas.

`H`: Sugestão: uma sugestão opcional sobre o que fazer com o problema. Isso visa diferir do Detalhe, pois oferece conselhos (potencialmente inadequados) em vez de fatos concretos. Pode ocupar várias linhas.

`P`: Posição: o valor do campo é um inteiro decimal ASCII, indicando a posição do cursor de erro como um índice na string de consulta original. O primeiro caractere tem índice 1, e as posições são medidas em caracteres, não em bytes.

`p`: Posição interna: isso é definido da mesma forma que o campo `P`, mas é usado quando a posição do cursor se refere a um comando gerado internamente, e não ao que foi enviado pelo cliente. O campo `q` sempre aparecerá quando este campo aparecer.

`q`: Consulta interna: o texto de um comando gerado internamente que falhou. Isso pode ser, por exemplo, uma consulta SQL emitida por uma função PL/pgSQL.

`W`: Onde: uma indicação do contexto em que o erro ocorreu. Atualmente, isso inclui um histórico de pilha de chamadas de funções de linguagem procedural ativa e consultas geradas internamente. A traçada é uma entrada por linha, a mais recente em primeiro lugar.

`s`: Nome do esquema: se o erro estiver associado a um objeto específico do banco de dados, o nome do esquema que contém esse objeto, se houver.

`t`: Nome da tabela: se o erro estiver associado a uma tabela específica, o nome da tabela. (Consulte o campo Nome do esquema para o nome do esquema da tabela.)

`c`: Nome da coluna: se o erro estiver associado a uma coluna específica da tabela, o nome da coluna. (Consulte os campos de nome do esquema e da tabela para identificar a tabela.)

`d`: Nome do tipo de dados: se o erro estiver associado a um tipo de dados específico, o nome do tipo de dados. (Consulte o campo nome do esquema para o nome do esquema do tipo de dados.)

`n`: Nome da restrição: se o erro estiver associado a uma restrição específica, o nome da restrição. Consulte os campos listados acima para a tabela ou domínio associado. (Para este propósito, os índices são tratados como restrições, mesmo que não tenham sido criados com sintaxe de restrição.)

`F`: Arquivo: o nome do arquivo da localização do código-fonte onde o erro foi relatado.

`L`: Linha: o número da linha da localização do código-fonte onde o erro foi relatado.

`R`: Routine: o nome da rotina de código-fonte que relata o erro.

Nota

Os campos para o nome do esquema, nome da tabela, nome da coluna, nome do tipo de dados e nome da restrição são fornecidos apenas para um número limitado de tipos de erro; consulte [Apêndice A](errcodes-appendix.md). Os frontends não devem assumir que a presença de qualquer um desses campos garanta a presença de outro campo. As fontes de erro principais observam as inter-relações mencionadas acima, mas as funções definidas pelo usuário podem usar esses campos de outras maneiras. Na mesma linha, os clientes não devem assumir que esses campos denotem objetos contemporâneos no banco de dados atual.

O cliente é responsável por formatar as informações exibidas para atender às suas necessidades; em particular, ele deve quebrar as linhas longas conforme necessário. Caracteres de nova linha que aparecem nos campos da mensagem de erro devem ser tratados como quebra de parágrafo, e não como quebra de linha.