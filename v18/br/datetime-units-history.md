## B.6. Histórico das Unidades [#](#DATETIME-UNITS-HISTORY)

O padrão SQL afirma que “dentro da definição de um ‘literal datetime’, os ‘valores datetime’ são restringidos pelas regras naturais para datas e horários de acordo com o calendário gregoriano”. O PostgreSQL segue o exemplo do padrão SQL ao contar datas exclusivamente no calendário gregoriano, mesmo para anos antes desse calendário estar em uso. Essa regra é conhecida como o *calendário gregoriano proleptico*.

O calendário Juliano foi introduzido por Júlio César em 45 a.C. Ele era utilizado comumente no mundo ocidental até o ano de 1582, quando os países começaram a mudar para o calendário Gregoriano. No calendário Juliano, o ano tropical é aproximado como 365 1/4 dias = 365,25 dias. Isso gera um erro de cerca de 1 dia em 128 anos.

O erro acumulado no calendário levou o Papa Gregório XIII a reformar o calendário de acordo com as instruções do Concílio de Trento. No calendário gregoriano, o ano tropical é aproximado como 365 + 97 / 400 dias = 365,2425 dias. Assim, leva aproximadamente 3300 anos para o ano tropical mudar um dia em relação ao calendário gregoriano.

A aproximação 365+97/400 é alcançada ao ter 97 anos bissextos a cada 400 anos, utilizando as seguintes regras:



<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   Todo ano divisível por 4 é um ano bissexto.
  </td>
 </tr>
 <tr>
  <td>
   No entanto, todo ano divisível por 100 não é um ano bissexto.
  </td>
 </tr>
 <tr>
  <td>
   No entanto, todo ano divisível por 400 é, afinal, um ano bissexto.
  </td>
 </tr>
</table>







Portanto, 1700, 1800, 1900, 2100 e 2200 não são anos bissextos. Mas 1600, 2000 e 2400 são anos bissextos. Em contraste, no calendário juliano mais antigo, todos os anos divisíveis por 4 são anos bissextos.

A bula papal de 15 de fevereiro de 1582 decretou que 10 dias deveriam ser eliminados de outubro de 1582, para que o dia 15 de outubro seguisse imediatamente após o dia 4 de outubro. Isso foi observado na Itália, na Polônia, em Portugal e na Espanha. Outros países católicos seguiram pouco depois, mas os países protestantes relutaram em mudar, e os países ortodoxos gregos não mudaram até o início do século XX. A reforma foi observada pela Grã-Bretanha e seus domínios (incluindo o que é agora os EUA) em 1752. Assim, o dia 2 de setembro de 1752 foi seguido pelo dia 14 de setembro de 1752. É por isso que os sistemas Unix que possuem o programa `cal` produzem o seguinte:

```
$ cal 9 1752
   September 1752
 S  M Tu  W Th  F  S
       1  2 14 15 16
17 18 19 20 21 22 23
24 25 26 27 28 29 30
```

Mas, claro, este calendário é válido apenas para a Grã-Bretanha e seus domínios, não para outros lugares. Como seria difícil e confuso tentar rastrear os calendários reais que estavam em uso em vários lugares em diferentes momentos, o PostgreSQL não tenta, mas sim segue as regras do calendário gregoriano para todas as datas, embora esse método não seja historicamente preciso.

Diferentes calendários foram desenvolvidos em várias partes do mundo, muitos deles anteriores ao sistema gregoriano. Por exemplo, os primeiros registros do calendário chinês podem ser rastreados até o século XIV a.C. A lenda diz que o imperador Huangdi inventou esse calendário em 2637 a.C. A República Popular da China utiliza o calendário gregoriano para fins civis. O calendário chinês é utilizado para determinar festivais.