## B.2.  Tratamento de Datas e Horários Inválidos ou Ambíguos [#](#DATETIME-INVALID-INPUT)

Normalmente, se uma string de data/hora for sintaticamente válida, mas contiver valores de campo fora do intervalo, um erro será lançado. Por exemplo, a entrada que especifica o dia 31 de fevereiro será rejeitada.

Durante uma transição de horário de verão, é possível que uma string de marcação de tempo aparentemente válida represente um horário de marcação de tempo inexistente ou ambíguo. Esses casos não são rejeitados; a ambiguidade é resolvida determinando qual deslocamento UTC aplicar. Por exemplo, supondo que o parâmetro [TimeZone](runtime-config-client.md#GUC-TIMEZONE) esteja configurado como `America/New_York`, considere

```
=> SELECT '2018-03-11 02:30'::timestamptz;
      timestamptz
------------------------
 2018-03-11 03:30:00-04
(1 row)
```

Como esse dia era uma data de transição para a primavera nesse fuso horário, não havia um instante de hora civil às 2:30 AM; os relógios saltaram para a frente de 2 AM EST para 3 AM EDT. O PostgreSQL interpreta o horário fornecido como se fosse a hora padrão (UTC-5), o que resulta em 3:30 AM EDT (UTC-4).

Por outro lado, considere o comportamento durante uma transição de fallback:

```
=> SELECT '2018-11-04 01:30'::timestamptz;
      timestamptz
------------------------
 2018-11-04 01:30:00-05
(1 row)
```

Naquela data, havia duas possíveis interpretações das 1:30 da madrugada; havia 1:30 da madrugada EDT, e, uma hora depois, após os relógios terem retornado de 2 da madrugada EDT para 1 da manhã EST, havia 1:30 da manhã EST. Novamente, o PostgreSQL interpreta o horário fornecido como se fosse a hora padrão (UTC-5). Podemos forçar a outra interpretação especificando o horário de verão:

```
=> SELECT '2018-11-04 01:30 EDT'::timestamptz;
      timestamptz
------------------------
 2018-11-04 01:30:00-04
(1 row)
```

A regra precisa que é aplicada em tais casos é que um timestamp inválido que parece pertencer a uma transição de hora de verão para a frente é atribuído o deslocamento UTC que prevaleceu no fuso horário imediatamente antes da transição, enquanto um timestamp ambíguo que poderia ocorrer em qualquer lado de uma transição para trás é atribuído o deslocamento UTC que prevaleceu imediatamente após a transição. Na maioria dos fusos horários, isso é equivalente a dizer que "a interpretação da hora padrão é preferida quando houver dúvida".

Em todos os casos, o deslocamento UTC associado a um timestamp pode ser especificado explicitamente, utilizando um deslocamento UTC numérico ou uma abreviação de fuso horário que corresponda a um deslocamento UTC fixo. A regra acima mencionada só se aplica quando é necessário inferir um deslocamento UTC para um fuso horário em que o deslocamento varia.