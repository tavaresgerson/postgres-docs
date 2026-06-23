## B.1. Interpretação da entrada de data/hora [#](#DATETIME-INPUT-RULES)

As strings de entrada de data/hora são decodificadas usando o procedimento a seguir.

1. Divida a string de entrada em tokens e categorize cada token como uma string, hora, fuso horário ou número.

1. Se o token numérico contiver um colon (`:`), este é uma string de tempo. Inclua todos os dígitos e colones subsequentes.
   2. Se o token numérico contiver uma barra (`-`), uma barra inclinada (`/`), ou dois ou mais pontos (`.`), este é uma string de data que pode ter um mês de texto. Se um token de data já tiver sido visto, é interpretado como o nome de uma zona horária (por exemplo, `America/New_York`).
   3. Se o token for apenas numérico, então é um campo único ou uma data concatenada ISO 8601 (por exemplo, `19990113` para 13 de janeiro de 1999) ou tempo (por exemplo, `141516` para 14:15:16).
   4. Se o token começar com um mais (`+`) ou menos (`-`), então é um fuso horário numérico ou um campo especial.
2. Se o token for uma string alfabética, corresponda com as possíveis strings:

1. Verifique se o token corresponde a alguma abreviação conhecida de fuso horário. Essas abreviações são determinadas pelas configurações descritas na [Seção B.4](datetime-config-files.md).
2. Se não for encontrado, procure uma tabela interna para corresponder ao token como uma string especial (por exemplo, `today`, `Thursday`, `January` ou palavra de ruído (por exemplo, `at`, `on`).
3. Se ainda não for encontrado, lance um erro.
3. Quando o token é um número ou campo numérico:

1. Se houver oito ou seis dígitos e se nenhum outro campo de data tiver sido lido anteriormente, então interprete como uma "data concatenada" (por exemplo, `19990118` ou `990118`). A interpretação é `YYYYMMDD` ou `YYMMDD`.
2. Se o token for três dígitos e um ano já tiver sido lido, então interprete como o dia do ano.
3. Se quatro ou seis dígitos e um ano já tiver sido lido, então interprete como uma hora (`HHMM` ou `HHMMSS`).
4. Se três ou mais dígitos e nenhum campo de data ainda tiver sido encontrado, interprete como um ano (isso força a ordenação das demais datas em formato yy-mm-dd).
5. Caso contrário, a ordenação do campo de data é assumida de acordo com a configuração `DateStyle`: mm-dd-yy, dd-mm-yy ou yy-mm-dd. Arraste um erro se um campo de mês ou dia for encontrado fora do intervalo.
4. Se o BC foi especificado, negue o ano e adicione um para armazenamento interno. (Não há ano zero no calendário gregoriano, então numericamente 1 a.C. se torna ano zero.)
5. Caso o BC não tenha sido especificado e o campo de ano tenha sido de dois dígitos, ajuste o ano para quatro dígitos. Se o campo tiver menos de 70, adicione 2000, caso contrário, adicione 1900.

### DICA

Os anos gregorianos de 1 a 99 AD podem ser inseridos usando 4 dígitos com zeros na frente (por exemplo, `0099` é AD 99).