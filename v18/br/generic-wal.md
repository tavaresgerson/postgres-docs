## 64.1. Registros genéricos WAL [#](#GENERIC-WAL)

Embora todos os módulos integrados com registro WAL tenham seus próprios tipos de registros WAL, também existe um tipo genérico de registro WAL, que descreve as alterações em páginas de maneira genérica.

### Nota

Os registros genéricos do WAL são ignorados durante [Decodificação lógica](logicaldecoding.md). Se a decodificação lógica for necessária para sua extensão, considere um Gerenciador de Recursos de WAL Personalizado.

A API para a construção de registros genéricos do WAL é definida em `access/generic_xlog.h` e implementada em `access/transam/generic_xlog.c`.

Para realizar uma atualização de dados registrada em WAL usando a facilidade de registro genérico de WAL, siga estes passos:

1. `state = GenericXLogStart(relation)` — iniciar a construção de um registro WAL genérico para a relação dada.
2. `page = GenericXLogRegisterBuffer(state, buffer, flags)` — registrar um buffer que será modificado dentro do registro WAL genérico atual. Esta função retorna um ponteiro para uma cópia temporária da página do buffer, onde as modificações devem ser feitas. (Não modifique diretamente o conteúdo do buffer). O terceiro argumento é uma máscara de bits de flags aplicáveis à operação. Atualmente, a única flag desse tipo é `GENERIC_XLOG_FULL_IMAGE`, que indica que uma imagem de página completa em vez de uma atualização delta deve ser incluída no registro WAL. Tipicamente, essa flag seria definida se a página for nova ou tiver sido completamente reescrita. `GenericXLogRegisterBuffer` pode ser repetida se a ação registrada no WAL precisar modificar múltiplas páginas.
3. Aplicar as modificações às imagens das páginas obtidas na etapa anterior.
4. `GenericXLogFinish(state)` — aplicar as mudanças aos buffers e emitir o registro WAL genérico.

A construção do registro WAL pode ser cancelada entre qualquer um dos passos acima, chamando `GenericXLogAbort(state)`. Isso descartará todas as alterações nas cópias da imagem da página.

Por favor, observe os seguintes pontos ao usar a facilidade de registro genérico WAL:

* Não são permitidas modificações diretas nos buffers. Todas as modificações devem ser feitas em cópias adquiridas de `GenericXLogRegisterBuffer()`. Em outras palavras, o código que faz registros WAL genéricos nunca deve chamar `BufferGetPage()` por si mesmo. No entanto, permanece como responsabilidade do chamador pin/unpinar e bloquear/desbloquear os buffers em momentos apropriados. O bloqueio exclusivo deve ser mantido em cada buffer alvo antes de `GenericXLogRegisterBuffer()` até depois de `GenericXLogFinish()`.
* As inscrições dos buffers (passo 2) e as modificações das imagens de página (passo 3) podem ser misturadas livremente, ou seja, ambas as etapas podem ser repetidas em qualquer sequência. Tenha em mente que os buffers devem ser registrados na mesma ordem em que as chaves devem ser obtidas neles durante a reprodução.
* O número máximo de buffers que podem ser registrados para um registro WAL genérico é `MAX_GENERIC_XLOG_PAGES`. Um erro será lançado se esse limite for excedido.
* O WAL genérico assume que as páginas a serem modificadas têm layout padrão, e em particular que não há dados úteis entre `pd_lower` e `pd_upper`.
* Como você está modificando cópias de páginas de buffer, `GenericXLogStart()` não inicia uma seção crítica. Assim, você pode realizar alocação de memória, lançamento de erros, etc., com segurança entre `GenericXLogStart()` e `GenericXLogFinish()`. A única seção crítica real está presente dentro de `GenericXLogFinish()`. Não há necessidade de se preocupar em chamar `GenericXLogAbort()` durante uma saída de erro, também.
* `GenericXLogFinish()` cuida de marcar os buffers como sujos e definir seus LSNs. Você não precisa fazer isso explicitamente.
* Para relações não registradas, tudo funciona da mesma forma, exceto que não é emitido um registro WAL real. Assim, você normalmente não precisa fazer verificações explícitas para relações não registradas.
* A função de refazer genérica do WAL adquirirá chaves exclusivas para os buffers na mesma ordem em que foram registrados. Após refazer todas as alterações, as chaves serão liberadas na mesma ordem.
* Se `GENERIC_XLOG_FULL_IMAGE` não for especificado para um buffer registrado, o registro genérico do WAL contém um delta entre as imagens de página antigas e novas. Esse delta é baseado em comparação byte a byte. Isso não é muito compacto para o caso de mover dados dentro de uma página, e pode ser melhorado no futuro.