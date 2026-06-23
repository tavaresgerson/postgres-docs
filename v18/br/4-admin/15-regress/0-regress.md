## Capítulo 31. Testes de Regressão

**Índice**

* [31.1. Realização dos testes](regress-run.md)

+ [31.1.1. Executar os testes em uma instalação temporária](regress-run.md#REGRESS-RUN-TEMP-INST)
+ [31.1.2. Executar os testes em uma instalação existente](regress-run.md#REGRESS-RUN-EXISTING-INST)
+ [31.1.3. Suítes de teste adicionais](regress-run.md#REGRESS-ADDITIONAL)
+ [31.1.4. Local e codificação](regress-run.md#REGRESS-RUN-LOCALE)
+ [31.1.5. Configurações personalizadas do servidor](regress-run.md#REGRESS-RUN-CUSTOM-SETTINGS)
+ [31.1.6. Testes extras](regress-run.md#REGRESS-RUN-EXTRA-TESTS)

* [31.2. Avaliação de Teste](regress-evaluation.md)

+ [31.2.1. Diferenças de Mensagem de Erro](regress-evaluation.md#REGRESS-EVALUATION-MESSAGE-DIFFERENCES)
+ [31.2.2. Diferenças de Local](regress-evaluation.md#REGRESS-EVALUATION-LOCALE-DIFFERENCES)
+ [31.2.3. Diferenças de Data e Hora](regress-evaluation.md#REGRESS-EVALUATION-DATE-TIME-DIFFERENCES)
+ [31.2.4. Diferenças de Ponto Flutuante](regress-evaluation.md#REGRESS-EVALUATION-FLOAT-DIFFERENCES)
+ [31.2.5. Diferenças de Ordem de Linha](regress-evaluation.md#REGRESS-EVALUATION-ORDERING-DIFFERENCES)
+ [31.2.6. Insuficiente Profundidade de Pilha](regress-evaluation.md#REGRESS-EVALUATION-STACK-DEPTH)
+ [31.2.7. O Teste “aleatório”](regress-evaluation.md#REGRESS-EVALUATION-RANDOM-TEST)
+ [31.2.8. Parâmetros de Configuração](regress-evaluation.md#REGRESS-EVALUATION-CONFIG-PARAMS)

* [31.3. Arquivos de Comparação de Variantes](regress-variant.md)
* [31.4. Testes de TAP](regress-tap.md)

+ [31.4.1. Variáveis de ambiente](regress-tap.md#REGRESS-TAP-VARS)

* [31.5. Exame de Cobertura de Teste](regress-coverage.md)

+ [31.5.1. Cobertura com Autoconf e Make](regress-coverage.md#REGRESS-COVERAGE-CONFIGURE)
+ [31.5.2. Cobertura com Meson](regress-coverage.md#REGRESS-COVERAGE-MESON)

Os testes de regressão são um conjunto abrangente de testes para a implementação SQL no PostgreSQL. Eles testam operações SQL padrão, bem como as capacidades extensas do PostgreSQL.