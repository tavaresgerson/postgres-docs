## B.7. Datas Julianas [#](#DATETIME-JULIAN-DATES)

O sistema de *Data Juliana* é um método para numerar os dias. Não está relacionado ao calendário Juliano, embora seja chamado de forma confusa de maneira semelhante a esse calendário. O sistema de Data Juliana foi inventado pelo erudito francês Joseph Justus Scaliger (1540-1609) e provavelmente leva seu nome do pai de Scaliger, o erudito italiano Julius Caesar Scaliger (1484-1558).

No sistema de Datas Julianas, cada dia tem um número sequencial, começando com JD 0 (que às vezes é chamado de *a* Datas Julianas). O JD 0 corresponde a 1º de janeiro de 4713 a.C. no calendário Juliano, ou a 24 de novembro de 4714 a.C. no calendário Gregoriano. A contagem de Datas Julianas é mais frequentemente usada por astrônomos para rotular suas observações noturnas, e, portanto, uma data vai do meio-dia UTC ao próximo meio-dia UTC, em vez de da meia-noite à meia-noite: o JD 0 designa as 24 horas do meio-dia UTC de 24 de novembro de 4714 a.C. ao meio-dia UTC de 25 de novembro de 4714 a.C.

Embora o PostgreSQL suporte a notação de data juliana para entrada e saída de datas (e também use datas julianas para alguns cálculos internos de datetime), ele não observa a conveniência de ter datas que corram de meio-dia a meio-dia. O PostgreSQL trata uma data juliana como sendo de meia-noite a meia-noite local, da mesma forma que uma data normal.

Essa definição, no entanto, oferece uma maneira de obter a definição astronômica quando você precisa dela: faça a aritmética no fuso horário `UTC+12`. Por exemplo,

```
=> SELECT extract(julian from '2021-06-23 7:00:00-04'::timestamptz at time zone 'UTC+12');
           extract
------------------------------
 2459388.95833333333333333333
(1 row)
=> SELECT extract(julian from '2021-06-23 8:00:00-04'::timestamptz at time zone 'UTC+12');
               extract
--------------------------------------
 2459389.0000000000000000000000000000
(1 row)
=> SELECT extract(julian from date '2021-06-23');
 extract
---------
 2459389
(1 row)
```
