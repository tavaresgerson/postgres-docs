## 20.8. Autenticação de Identificação [#](#AUTH-IDENT)

O método de autenticação ident funciona obtendo o nome do usuário do sistema operacional do cliente de um servidor ident e usando-o como o nome do usuário permitido do banco de dados (com um mapeamento opcional de nome de usuário). Isso é suportado apenas em conexões TCP/IP.

### Nota

Quando o ident é especificado para uma conexão local (não TCP/IP), a autenticação de pares (consulte [Seção 20.9](auth-peer.md)) será usada em vez disso.

As seguintes opções de configuração são suportadas para `ident`:

`map`: Permite mapear entre os nomes de usuários do sistema e do banco de dados. Consulte a [Seção 20.2](auth-username-maps.md) para obter detalhes.

O "Protocolo de Identificação" é descrito em [RFC 1413](https://datatracker.ietf.org/doc/html/rfc1413). Praticamente todos os sistemas operacionais semelhantes ao Unix vêm com um servidor ident que escuta na porta TCP 113 por padrão. A funcionalidade básica de um servidor ident é responder a perguntas como “Qual usuário iniciou a conexão que sai da sua porta *`X`* e se conecta à minha porta *`Y`*?”. Como o PostgreSQL sabe tanto *`X`* quanto *`Y` quando uma conexão física é estabelecida, ele pode interrogar o servidor ident no host do cliente que está se conectando e, teoricamente, pode determinar o usuário do sistema operacional para qualquer conexão dada.

O inconveniente desse procedimento é que ele depende da integridade do cliente: se a máquina do cliente não é confiável ou comprometida, um invasor poderia executar praticamente qualquer programa na porta 113 e retornar qualquer nome de usuário que escolheu. Esse método de autenticação, portanto, é apropriado apenas para redes fechadas, onde cada máquina do cliente está sob controle rigoroso e onde os administradores do banco de dados e do sistema operam em contato próximo. Em outras palavras, você deve confiar na máquina que executa o servidor ident. Atenção ao aviso:

<table border="0" class="blockquote" style="width: 100%; cellspacing: 0; cellpadding: 0;" summary="Block quote">
 <tr>
  <td valign="top" width="10%">
  </td>
  <td valign="top" width="80%">
   <p>
    O Protocolo de Identificação não é destinado como um protocolo de autorização ou controle de acesso.
   </p>
  </td>
  <td valign="top" width="10%">
  </td>
 </tr>
 <tr>
  <td valign="top" width="10%">
  </td>
  <td align="right" colspan="2" valign="top">
   --
   <span class="attribution">
    RFC 1413
   </span>
  </td>
 </tr>
</table>

Alguns servidores ident têm uma opção não padrão que faz com que o nome do usuário retornado seja criptografado, usando uma chave que apenas o administrador da máquina de origem conhece. Esta opção *não deve* ser usada ao usar o servidor ident com o PostgreSQL, uma vez que o PostgreSQL não tem nenhuma maneira de descriptografar a string retornada para determinar o nome real do usuário.