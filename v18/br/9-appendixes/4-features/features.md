## Apêndice D. Conformação SQL

**Índice**

* [D.1. Recursos suportados](features-sql-standard.md)
* [D.2. Recursos não suportados](unsupported-features-sql-standard.md)
* [D.3. Limites XML e conformidade com SQL/XML](xml-limits-conformance.md)

+ [D.3.1. As consultas são restritas ao XPath 1.0](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-XPATH1)
+ [D.3.2. Limites incidentes da implementação](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-POSTGRESQL)

Esta seção tenta descrever em que medida o PostgreSQL se conforma ao padrão SQL atual. As informações a seguir não constituem uma declaração completa de conformidade, mas apresentam os principais tópicos com o máximo de detalhes que é razoável e útil para os usuários.

O nome formal do padrão SQL é ISO/IEC 9075 “Linguagem de banco de dados SQL”. Uma versão revisada do padrão é lançada de tempos em tempos; a atualização mais recente aparece em 2023. A versão de 2023 é referida como ISO/IEC 9075:2023, ou simplesmente como SQL:2023. As versões anteriores a essa foram SQL:2016, SQL:2011, SQL:2008, SQL:2006, SQL:2003, SQL:1999 e SQL-92. Cada versão substitui a anterior, portanto, reivindicações de conformidade com versões anteriores não têm mérito oficial. O desenvolvimento do PostgreSQL visa a conformidade com a versão mais recente do padrão oficial, onde tal conformidade não contradiz características tradicionais ou senso comum. Muitas das características exigidas pelo padrão SQL são suportadas, embora às vezes com sintaxe ou função ligeiramente diferentes. Movimentos adicionais em direção à conformidade podem ser esperados ao longo do tempo.

O SQL-92 definiu três conjuntos de características para conformidade: Entrada, Intermediário e Completo. A maioria dos sistemas de gerenciamento de banco de dados que reivindicavam conformidade com o padrão SQL estavam conformes apenas no nível de Entrada, pois o conjunto completo de características nos níveis Intermediário e Completo era ou muito volumoso ou em conflito com comportamentos legados.

Começando com SQL:1999, o padrão SQL define um grande conjunto de características individuais, em vez dos três níveis amplamente ineficazes encontrados no SQL-92. Um grande subconjunto dessas características representa as características “Core”, que todas as implementações SQL conformes devem fornecer. O resto das características são puramente opcionais.

O padrão é dividido em várias partes, cada uma também conhecida por um nome abreviado:

* ISO/IEC 9075-1 Estrutura (SQL/Framework)
* ISO/IEC 9075-2 Fundação (SQL/Foundation)
* ISO/IEC 9075-3 Interface de nível de chamada (SQL/CLI)
* ISO/IEC 9075-4 Módulos armazenados persistentes (SQL/PSM)
* ISO/IEC 9075-9 Gerenciamento de dados externos (SQL/MED)
* ISO/IEC 9075-10 Ligações de linguagem de objeto (SQL/OLB)
* ISO/IEC 9075-11 Esquemas de informação e definição (SQL/Schemata)
* ISO/IEC 9075-13 Rotinas e tipos usando o idioma Java (SQL/JRT)
* ISO/IEC 9075-14 Especificações relacionadas a XML (SQL/XML)
* ISO/IEC 9075-15 Matrizes multidimensionais (SQL/MDA)
* ISO/IEC 9075-16 Consultas de gráfico de propriedades (SQL/PGQ)

Observe que alguns números de peça não são (ou não são mais) utilizados.

O núcleo do PostgreSQL cobre as partes 1, 2, 9, 11 e 14. A parte 3 é coberta pelo driver ODBC, e a parte 13 é coberta pelo plug-in PL/Java, mas a conformidade exata atualmente não está sendo verificada para esses componentes. Atualmente, não há implementações das partes 4, 10, 15 e 16 para o PostgreSQL.

O PostgreSQL suporta a maioria das principais características do SQL:2023. Das 177 características obrigatórias necessárias para a conformidade completa do Núcleo, o PostgreSQL se conforma a pelo menos 170. Além disso, há uma longa lista de características opcionais suportadas. Vale ressaltar que, no momento da escrita, nenhuma versão atual de qualquer sistema de gerenciamento de banco de dados reivindica conformidade completa com o SQL:2023 do Núcleo.

Nas duas seções seguintes, fornecemos uma lista dessas funcionalidades que o PostgreSQL suporta, seguida de uma lista das funcionalidades definidas no SQL:2023 que ainda não são suportadas no PostgreSQL. Ambas as listas são aproximadas: Pode haver detalhes menores que não são conformes para uma funcionalidade que é listada como suportada, e grandes partes de uma funcionalidade não suportada podem, de fato, ser implementadas. O corpo principal da documentação sempre contém as informações mais precisas sobre o que funciona e o que não funciona.

### Nota

Os códigos de recurso que contêm um hífen são subrecursos. Portanto, se um recurso específico não for suportado, o recurso principal é listado como não suportado, mesmo que alguns outros subrecursos sejam suportados.