## Capítulo 37. Gatilhos

**Índice**

* [37.1. Visão geral do comportamento do gatilho](trigger-definition.md)
* [37.2. Visibilidade das alterações dos dados](trigger-datachanges.md)
* [37.3. Escrever funções de gatilho em C](trigger-interface.md)
* [37.4. Um exemplo completo de gatilho](trigger-example.md)

Este capítulo fornece informações gerais sobre a escrita de funções de gatilho. As funções de gatilho podem ser escritas na maioria dos idiomas processuais disponíveis, incluindo PL/pgSQL ([Capítulo 41](plpgsql.md)), PL/Tcl ([Capítulo 42](pltcl.md)), PL/Perl ([Capítulo 43](plperl.md)) e PL/Python ([Capítulo 44](plpython.md)). Após ler este capítulo, você deve consultar o capítulo para o idioma processual que você prefere para descobrir os detalhes específicos do idioma para escrever um gatilho nele.

Também é possível escrever uma função de gatilho em C, embora a maioria das pessoas ache mais fácil usar uma das linguagens procedimentais. Atualmente, não é possível escrever uma função de gatilho no idioma de função SQL simples.