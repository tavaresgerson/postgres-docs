## 20.9. Autenticação entre pares [#](#AUTH-PEER)

O método de autenticação entre pares funciona obtendo o nome do usuário do sistema operacional do cliente do kernel e usando-o como o nome de usuário do banco de dados permitido (com mapeamento opcional de nome de usuário). Esse método é suportado apenas em conexões locais.

As seguintes opções de configuração são suportadas para `peer`:

`map`: Permite mapear entre os nomes de usuários do sistema e do banco de dados. Consulte a [Seção 20.2](auth-username-maps.md) para obter detalhes.

A autenticação entre pares só está disponível em sistemas operacionais que fornecem a função `getpeereid()`, o parâmetro de soquete `SO_PEERCRED` ou mecanismos semelhantes. Atualmente, isso inclui Linux, a maioria das versões de BSD, incluindo o macOS e o Solaris.