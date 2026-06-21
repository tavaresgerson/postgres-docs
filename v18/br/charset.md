## Capítulo 23. Localização

**Índice**

* [23.1. Suporte a localização](locale.md)

+ [23.1.1. Visão geral](locale.md#LOCALE-OVERVIEW)
+ [23.1.2. Comportamento](locale.md#LOCALE-BEHAVIOR)
+ [23.1.3. Seleção de locais](locale.md#LOCALE-SELECTING-LOCALES)
+ [23.1.4. Fornecedores de locais](locale.md#LOCALE-PROVIDERS)
+ [23.1.5. Locais ICU](locale.md#ICU-LOCALES)
+ [23.1.6. Problemas](locale.md#LOCALE-PROBLEMS)

* [23.2. Suporte de Colaboração](collation.md)

+ [23.2.1. Conceitos](collation.md#COLLATION-CONCEPTS)
+ [23.2.2. Gerenciamento de Colagens](collation.md#COLLATION-MANAGING)
+ [23.2.3. Colagens Personalizadas do ICU](collation.md#ICU-CUSTOM-COLLATIONS)

* [23.3. Suporte a Conjunto de Caracteres](multibyte.md)

+ [23.3.1. Conjuntos de Caracteres Suportado][(multibyte.md#MULTIBYTE-CHARSET-SUPPORTED)
+ [23.3.2. Configuração do Conjunto de Caracteres][(multibyte.md#MULTIBYTE-SETTING)
+ [23.3.3. Conversão Automática de Conjunto de Caracteres Entre o Servidor e o Cliente][(multibyte.md#MULTIBYTE-AUTOMATIC-CONVERSION)
+ [23.3.4. Conversões de Conjuntos de Caracteres Disponíveis][(multibyte.md#MULTIBYTE-CONVERSIONS-SUPPORTED)
+ [23.3.5. Leitura Adicional][(multibyte.md#MULTIBYTE-FURTHER-READING)

Este capítulo descreve as funcionalidades de localização disponíveis do ponto de vista do administrador. O PostgreSQL suporta duas funcionalidades de localização:

* Utilizar as funcionalidades de localização do sistema operacional para fornecer ordem de ordenação específica para a localização, formatação de números, mensagens traduzidas e outros aspectos. Isso é abordado na [Seção 23.1][(locale.md "23.1. Locale Support")] e [Seção 23.2][(collation.md "23.2. Collation Support")].
* Fornecer vários conjuntos de caracteres diferentes para suportar o armazenamento de texto em todos os tipos de idiomas, e fornecer tradução de conjuntos de caracteres entre cliente e servidor. Isso é abordado na [Seção 23.3][(multibyte.md "23.3. Character Set Support")].