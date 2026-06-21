## SET SESSION AUTHORIZATION

SET SESSION AUTHORIZATION — defina o identificador do usuário da sessão e o identificador do usuário atual da sessão atual

## Sinopse

```
SET [ SESSION | LOCAL ] SESSION AUTHORIZATION user_name
SET [ SESSION | LOCAL ] SESSION AUTHORIZATION DEFAULT
RESET SESSION AUTHORIZATION
```

## Descrição

Este comando define o identificador do usuário da sessão e o identificador do usuário atual da sessão SQL atual como *`user_name`*. O nome do usuário pode ser escrito como um identificador ou uma literal de string. Usando este comando, é possível, por exemplo, tornar-se temporariamente um usuário não privilegiado e, posteriormente, voltar a ser um superusuário.

O identificador do usuário da sessão é inicialmente definido como o nome do usuário (possivelmente autenticado) fornecido pelo cliente. O identificador atual do usuário normalmente é igual ao identificador do usuário da sessão, mas pode mudar temporariamente no contexto das funções `SECURITY DEFINER` e mecanismos semelhantes; também pode ser alterado por `SET ROLE` (sql-set-role.md "SET ROLE"). O identificador atual do usuário é relevante para a verificação de permissão.

O identificador do usuário da sessão pode ser alterado apenas se o usuário inicial da sessão (o usuário autenticado) tiver o privilégio de superusuário. Caso contrário, o comando é aceito apenas se especificar o nome do usuário autenticado.

Os modificadores `SESSION` e `LOCAL` atuam da mesma forma que o comando regular [`SET`(sql-set.md "SET")].

Os formulários `DEFAULT` e `RESET` redefinem as sessões e os identificadores do usuário atual para o nome do usuário autenticado originalmente. Esses formulários podem ser executados por qualquer usuário.

## Notas

`SET SESSION AUTHORIZATION` não pode ser usado dentro de uma função `SECURITY DEFINER`.

## Exemplos

```
SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user
--------------+--------------
 peter        | peter

SET SESSION AUTHORIZATION 'paul';

SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user
--------------+--------------
 paul         | paul
```

## Compatibilidade

O padrão SQL permite que outras expressões apareçam no lugar do literal *`user_name`*, mas essas opções não são importantes na prática. O PostgreSQL permite a sintaxe de identificadores (`"username"`), o que o SQL não faz. O SQL não permite esse comando durante uma transação; o PostgreSQL não faz essa restrição porque não há motivo para isso. Os modificadores `SESSION` e `LOCAL` são uma extensão do PostgreSQL, assim como a sintaxe `RESET`.

Os privilégios necessários para executar este comando são definidos pela implementação padrão.

## Veja também

[SET ROLE](sql-set-role.md "SET ROLE")