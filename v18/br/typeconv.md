## Capítulo 10. Conversão de Tipo

**Índice**

* [10.1. Visão geral](typeconv-overview.md)
* [10.2. Operadores](typeconv-oper.md)
* [10.3. Funções](typeconv-func.md)
* [10.4. Armazenamento de valores](typeconv-query.md)
* [10.5. `UNION`, `CASE` e construções relacionadas](typeconv-union-case.md)
* [10.6. Colunas de saída `SELECT`](typeconv-select.md)

As instruções SQL podem, intencionalmente ou não, exigir a mistura de diferentes tipos de dados na mesma expressão. O PostgreSQL possui extensas facilidades para avaliar expressões de tipos mistos.

Em muitos casos, o usuário não precisa entender os detalhes do mecanismo de conversão de tipo. No entanto, as conversões implícitas realizadas pelo PostgreSQL podem afetar os resultados de uma consulta. Quando necessário, esses resultados podem ser ajustados usando *conversão explícita* de tipo.

Este capítulo apresenta os mecanismos e convenções de conversão de tipos do PostgreSQL. Consulte as seções relevantes em [Capítulo 8](datatype.md) e [Capítulo 9](functions.md) para obter mais informações sobre tipos de dados específicos e funções e operadores permitidos.