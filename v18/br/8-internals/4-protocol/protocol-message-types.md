## 54.6. Tipos de dados de mensagem [#](#PROTOCOL-MESSAGE-TYPES)

Esta seção descreve os tipos de dados básicos utilizados em mensagens.

Int*`n`*(*`i`*): Um inteiro de *`n`*-bit no byte da rede (byte mais significativo primeiro). Se *`i`* for especificado, é o valor exato que aparecerá, caso contrário, o valor é variável. Exemplo: Int16, Int32(42).

Int*`n`*[*`k`*]: Uma matriz de *`k`* *`n`*-bits inteiros, cada um no formato de byte de rede. O comprimento da matriz *`k`* é sempre determinado por um campo anterior na mensagem. Exemplo: Int16[M].

String(*`s`*): Uma string terminada por nulo (string estilo C). Não há limitação específica de comprimento para strings. Se *`s`* for especificado, é o valor exato que aparecerá, caso contrário, o valor é variável. Exemplo: String, String("user").

Nota

*Não há um limite pré-definido* para o comprimento de uma string que pode ser devolvida pelo backend. Uma boa estratégia de codificação para um frontend é usar um buffer expansível para que qualquer coisa que cabe na memória possa ser aceita. Se isso não for viável, leia a string completa e descarte os caracteres finais que não cabem no seu buffer de tamanho fixo.

Byte*`n`*(*`c`*): Exatamente *`n`* bytes. Se a largura do campo *`n`* não for uma constante, ela sempre pode ser determinada a partir de um campo anterior na mensagem. Se *`c`* for especificado, é o valor exato. Exemplo: Byte2, Byte1('\n').