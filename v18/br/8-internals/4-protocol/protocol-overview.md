## 54.1. Visão geral [#](#PROTOCOL-OVERVIEW)

* [54.1.1. Visão geral de mensagens](protocol-overview.md#PROTOCOL-MESSAGE-CONCEPTS)
* [54.1.2. Visão geral de consultas extensas](protocol-overview.md#PROTOCOL-QUERY-CONCEPTS)
* [54.1.3. Formatos e códigos de formato](protocol-overview.md#PROTOCOL-FORMAT-CODES)
* [54.1.4. Versões de protocolo](protocol-overview.md#PROTOCOL-VERSIONS)

O protocolo tem fases separadas para inicialização e operação normal. Na fase de inicialização, o frontend abre uma conexão com o servidor e se autentica para satisfação do servidor. (Isso pode envolver uma única mensagem, ou várias mensagens, dependendo do método de autenticação sendo usado.) Se tudo correr bem, o servidor envia informações de status para o frontend e, finalmente, entra em operação normal. Exceto pela mensagem inicial de solicitação de inicialização, essa parte do protocolo é controlada pelo servidor.

Durante o funcionamento normal, o frontend envia consultas e outros comandos ao backend, e o backend envia resultados de consulta e outras respostas de volta. Há alguns casos (como `NOTIFY`) em que o backend enviará mensagens não solicitadas, mas, na maior parte, essa parte da sessão é impulsionada por solicitações do frontend.

A interrupção da sessão é normalmente feita pela escolha do frontend, mas pode ser forçada pelo backend em certos casos. Em qualquer caso, quando o backend fecha a conexão, ele reverte qualquer transação aberta (incompleta) antes de sair.

Em operação normal, os comandos SQL podem ser executados através de um dos dois sub-protocolos. No protocolo de "consulta simples", o frontend apenas envia uma string de consulta textual, que é analisada e imediatamente executada pelo backend. No protocolo de "consulta estendida", o processamento das consultas é separado em múltiplos passos: análise, vinculação de valores de parâmetros e execução. Isso oferece flexibilidade e benefícios de desempenho, ao custo de complexidade extra.

O funcionamento normal possui subprotocolos adicionais para operações especiais, como `COPY`.

### 54.1.1. Visão geral das mensagens [#](#PROTOCOL-MESSAGE-CONCEPTS)

Toda comunicação é feita por meio de uma corrente de mensagens. O primeiro byte de uma mensagem identifica o tipo de mensagem, e os quatro bytes seguintes especificam o comprimento do restante da mensagem (esse contagem de comprimento inclui o próprio byte de tipo de mensagem, mas não o byte de tipo de mensagem). O conteúdo restante da mensagem é determinado pelo tipo de mensagem. Por razões históricas, a primeira mensagem enviada pelo cliente (a mensagem inicial) não tem o byte inicial de tipo de mensagem.

Para evitar perder a sincronização com o fluxo de mensagens, os servidores e clientes geralmente leem uma mensagem inteira em um buffer (usando o número de bytes) antes de tentar processar seu conteúdo. Isso permite uma recuperação fácil se um erro for detectado durante o processamento do conteúdo. Em situações extremas (como não ter memória suficiente para bufferizar a mensagem), o receptor pode usar o número de bytes para determinar quanto de entrada ignorar antes de retomar a leitura de mensagens.

Por outro lado, tanto os servidores quanto os clientes devem ter o cuidado de nunca enviar uma mensagem incompleta. Isso é comumente feito marcando toda a mensagem em um buffer antes de começar a enviá-la. Se ocorrer uma falha de comunicação durante a transmissão ou recepção de uma mensagem, a única resposta sensível é abandonar a conexão, uma vez que há pouca esperança de recuperar a sincronização do limite da mensagem.

### 54.1.2. Visão geral da consulta estendida [#](#PROTOCOL-QUERY-CONCEPTS)

No protocolo de consulta estendida, a execução de comandos SQL é dividida em múltiplos passos. O estado mantido entre os passos é representado por dois tipos de objetos: *declarações preparadas* e *portals*. Uma declaração preparada representa o resultado da análise sintática e semântica de uma cadeia de caracteres de consulta textual. Uma declaração preparada não está pronta para execução por si só, porque pode não ter valores específicos para *parâmetros*. Um portal representa uma declaração pronta para execução ou já parcialmente executada, com quaisquer valores de parâmetro faltantes preenchidos. (Para declarações `SELECT`, um portal é equivalente a um cursor aberto, mas escolhemos usar um termo diferente, uma vez que os cursors não lidam com declarações não `SELECT`.)

O ciclo geral de execução consiste em uma etapa de *paráfrase*, que cria uma declaração preparada a partir de uma string de consulta textual; uma etapa de *vinculação*, que cria um portal dado uma declaração preparada e valores para quaisquer parâmetros necessários; e uma etapa de *execução* que executa a consulta de um portal. No caso de uma consulta que retorna linhas (`SELECT`, `SHOW`, etc.), a etapa de execução pode ser instruída para obter apenas um número limitado de linhas, de modo que várias etapas de execução possam ser necessárias para completar a operação.

O backend pode acompanhar múltiplas declarações preparadas e portais (mas observe que esses existem apenas dentro de uma sessão e nunca são compartilhados entre sessões). As declarações preparadas e os portais existentes são referenciados por nomes atribuídos quando foram criados. Além disso, existe uma declaração preparada e um portal “sem nome”. Embora esses se comportem de maneira amplamente a mesma que os objetos nomeados, as operações neles são otimizadas para o caso de executar uma consulta apenas uma vez e, em seguida, descartá-la, enquanto as operações nos objetos nomeados são otimizadas na expectativa de múltiplos usos.

### 54.1.3. Formatos e Códigos de Formato [#](#PROTOCOL-FORMAT-CODES)

Os dados de um tipo de dado específico podem ser transmitidos em qualquer um dos vários *formatos* diferentes. A partir do PostgreSQL 7.4, os únicos formatos suportados são “texto” e “binário”, mas o protocolo prevê extensões futuras. O formato desejado para qualquer valor é especificado por um *código de formato*. Os clientes podem especificar um código de formato para cada valor do parâmetro transmitido e para cada coluna de um resultado de consulta. O texto tem código de formato zero, o binário tem código de formato um, e todos os outros códigos de formato são reservados para definição futura.

A representação textual dos valores é qualquer cadeia de caracteres produzida e aceita pelas funções de conversão de entrada/saída para o tipo de dados específico. Na representação transmitida, não há caractere nulo final; o frontend deve adicionar um aos valores recebidos se quiser processá-los como strings em C. (O formato de texto, aliás, não permite nulas embutidas.)

As representações binárias para inteiros utilizam a ordem de byte da rede (byte mais significativo primeiro). Para outros tipos de dados, consulte a documentação ou o código-fonte para saber mais sobre a representação binária. Tenha em mente que as representações binárias para tipos de dados complexos podem mudar entre as versões do servidor; o formato de texto é geralmente a opção mais portátil.

### 54.1.4. Versões do protocolo [#](#PROTOCOL-VERSIONS)

A versão atual e mais recente do protocolo é a versão 3.2. No entanto, para compatibilidade reversa com versões antigas do servidor e middleware que ainda não suportam a negociação de versão, o libpq ainda usa a versão do protocolo 3.0 por padrão.

Um único servidor pode suportar múltiplas versões de protocolo. A mensagem inicial de solicitação de inicialização informa ao servidor qual versão do protocolo o cliente está tentando usar. Se a versão principal solicitada pelo cliente não for suportada pelo servidor, a conexão será rejeitada (por exemplo, isso ocorreria se o cliente solicitasse a versão 4.0 do protocolo, que não existe neste momento). Se a versão menor solicitada pelo cliente não for suportada pelo servidor (por exemplo, o cliente solicita a versão 3.2, mas o servidor suporta apenas a versão 3.0), o servidor pode rejeitar a conexão ou pode responder com uma mensagem NegotiateProtocolVersion contendo a versão de protocolo menor mais alta que ele suporta. O cliente pode, então, optar por continuar com a conexão usando a versão de protocolo especificada ou por abortar a conexão.

A negociação de protocolo foi introduzida na versão 9.3.21 do PostgreSQL. As versões anteriores rejeitariam a conexão se o cliente solicitasse uma versão menor que não fosse suportada pelo servidor.

[Tabela 54.1](protocol-overview.md#PROTOCOL-VERSIONS-TABLE) mostra as versões de protocolo atualmente suportadas.

**Tabela 54.1. Versões do protocolo**



<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Version
   </th>
   <th>
    Apoiado por
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    3.2
   </td>
   <td>
    PostgreSQL 18 e versões posteriores
   </td>
   <td>
    Versão atual mais recente. A chave secreta usada na cancelamento de consulta foi ampliada de 4 bytes para um campo de comprimento variável. A mensagem BackendKeyData foi alterada para acomodar isso, e a mensagem CancelRequest foi redefinida para ter um payload de comprimento variável.
   </td>
  </tr>
  <tr>
   <td>
    3.1
   </td>
   <td>
    -
   </td>
   <td>
    Reservada. A versão 3.1 não foi usada por nenhuma versão do PostgreSQL, mas foi ignorada porque versões antigas do aplicativo popular pgbouncer tinham um bug na negociação do protocolo que o fazia afirmar incorretamente que suportava a versão 3.1.
   </td>
  </tr>
  <tr>
   <td>
    3.0
   </td>
   <td>
    PostgreSQL 7.4 e versões posteriores
   </td>
   <td class="auto-generated">
   </td>
  </tr>
  <tr>
   <td>
    2.0
   </td>
   <td>
    até PostgreSQL 13
   </td>
   <td>
    Veja as edições anteriores do
    <span class="productname">
     PostgreSQL
    </span>
    documentação para detalhes
   </td>
  </tr>
 </tbody>
</table>





