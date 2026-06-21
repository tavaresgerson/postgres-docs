## Apêndice B. Suporte para Data/Hora

**Índice**

* [B.1. Interpretação de Entrada de Data/Hora](datetime-input-rules.md)
* [B.2. Tratamento de Timestamps Inválidos ou Ambíguos](datetime-invalid-input.md)
* [B.3. Palavras-chave de Data/Hora](datetime-keywords.md)
* [B.4. Arquivos de Configuração de Data/Hora](datetime-config-files.md)
* [B.5. Especificações de Fuso Horário POSIX](datetime-posix-timezone-specs.md)
* [B.6. Histórico de Unidades](datetime-units-history.md)
* [B.7. Datas Julianas](datetime-julian-dates.md)

O PostgreSQL utiliza um analisador heurístico interno para todo o suporte de entrada de data/hora. As datas e horários são inseridos como strings e são divididos em campos distintos com uma determinação preliminar do tipo de informação que pode estar no campo. Cada campo é interpretado e recebe um valor numérico, é ignorado ou rejeitado. O analisador contém tabelas de pesquisa internas para todos os campos textuais, incluindo meses, dias da semana e fusos horários.

Este apêndice inclui informações sobre o conteúdo dessas tabelas de busca e descreve os passos utilizados pelo analisador para decodificar datas e horários.