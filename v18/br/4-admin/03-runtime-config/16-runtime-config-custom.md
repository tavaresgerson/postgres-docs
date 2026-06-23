## 19.16. Opções Personalizadas [#](#RUNTIME-CONFIG-CUSTOM)

Esse recurso foi projetado para permitir que parâmetros que normalmente não são conhecidos pelo PostgreSQL sejam adicionados por módulos adicionais (como linguagens procedimentais). Isso permite que módulos de extensão sejam configurados nas formas padrão.

As opções personalizadas têm nomes compostos: um nome de extensão, seguido de um ponto e, em seguida, o nome próprio do parâmetro, muito parecido com nomes qualificados em SQL. Um exemplo é `plpgsql.variable_conflict`.

Como as opções personalizadas podem precisar ser definidas em processos que não carregaram o módulo de extensão relevante, o PostgreSQL aceitará uma definição para qualquer nome de parâmetro de duas partes. Tais variáveis são tratadas como marcadores e não têm função até que o módulo que as define seja carregado. Quando um módulo de extensão é carregado, ele adicionará suas definições de variáveis e converterá quaisquer valores de marcador de acordo com essas definições. Se houver quaisquer marcadores não reconhecidos que comecem com o nome da extensão, avisos são emitidos e esses marcadores são removidos.