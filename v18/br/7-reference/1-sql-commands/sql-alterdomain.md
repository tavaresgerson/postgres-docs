## ALTERAR DOMÍNIOS

ALTERAR DOMÍNIO — alterar a definição de um domínio

## Sinopse

```
ALTER DOMAIN name
    { SET DEFAULT expression | DROP DEFAULT }
ALTER DOMAIN name
    { SET | DROP } NOT NULL
ALTER DOMAIN name
    ADD domain_constraint [ NOT VALID ]
ALTER DOMAIN name
    DROP CONSTRAINT [ IF EXISTS ] constraint_name [ RESTRICT | CASCADE ]
ALTER DOMAIN name
     RENAME CONSTRAINT constraint_name TO new_constraint_name
ALTER DOMAIN name
    VALIDATE CONSTRAINT constraint_name
ALTER DOMAIN name
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER DOMAIN name
    RENAME TO new_name
ALTER DOMAIN name
    SET SCHEMA new_schema

where domain_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL | CHECK (expression) }
```

## Descrição

`ALTER DOMAIN` altera a definição de um domínio existente. Existem várias subformas:

`SET`/`DROP DEFAULT`: Esses formulários definem ou removem o valor padrão para um domínio. Observe que os padrões só se aplicam a comandos subsequentes `INSERT`; eles não afetam as linhas já em uma tabela que usa o domínio.

`SET`/`DROP NOT NULL`: Esses formulários alteram se um domínio é marcado para permitir valores NULL ou para rejeitar valores NULL. Você só pode `SET NOT NULL` quando as colunas que utilizam o domínio não contêm valores nulos.

`ADD domain_constraint [ NOT VALID ]`: Este formulário adiciona uma nova restrição a um domínio. Quando uma nova restrição é adicionada a um domínio, todas as colunas que utilizam esse domínio serão verificadas contra a restrição recém-adicionada. Esses verificações podem ser suprimidas adicionando a nova restrição usando a opção `NOT VALID`; a restrição pode ser validada posteriormente usando `ALTER DOMAIN ... VALIDATE CONSTRAINT`. Linhas recém-inseridas ou atualizadas são sempre verificadas contra todas as restrições, mesmo aquelas marcadas `NOT VALID`. `NOT VALID` é aceito apenas para restrições `CHECK`.

`DROP CONSTRAINT [ IF EXISTS ]`: Este formulário elimina as restrições de um domínio. Se `IF EXISTS` for especificado e a restrição não existir, não será lançada nenhuma mensagem de erro. Nesse caso, é emitida uma notificação em vez disso.

`RENAME CONSTRAINT`: Este formulário altera o nome de uma restrição em um domínio.

`VALIDATE CONSTRAINT`: Este formulário valida uma restrição previamente adicionada como `NOT VALID`, ou seja, verifica se todos os valores nas colunas da tabela do tipo de domínio satisfazem a restrição especificada.

`OWNER`: Este formulário altera o proprietário do domínio para o usuário especificado.

`RENAME`: Este formulário altera o nome do domínio.

`SET SCHEMA`: Este formulário altera o esquema do domínio. Quaisquer restrições associadas ao domínio também são movidas para o novo esquema.

Você deve ser o proprietário do domínio para usar `ALTER DOMAIN`. Para alterar o esquema de um domínio, você também deve ter o privilégio `CREATE` no novo esquema. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter o privilégio `CREATE` no esquema do domínio. (Essas restrições garantem que alterar o proprietário não faz nada que você não pudesse fazer ao descartar e recriar o domínio. No entanto, um superusuário pode alterar a propriedade de qualquer domínio de qualquer maneira.)

## Parâmetros

*`name`*: O nome (possivelmente qualificado por esquema) de um domínio existente que se deseja alterar.

*`domain_constraint`*: Nova restrição de domínio para o domínio.

*`constraint_name`*: Nome de uma restrição existente para excluir ou renomear.

`NOT VALID`: Não verifique os dados armazenados existentes quanto à validade da restrição.

`CASCADE`: Descarte automaticamente os objetos que dependem da restrição e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Rejeitar a eliminação da restrição se houver quaisquer objetos dependentes. Esse é o comportamento padrão.

*`new_name`*: O novo nome do domínio.

*`new_constraint_name`*: O novo nome para a restrição.

*`new_owner`*: O nome do usuário do novo proprietário do domínio.

*`new_schema`*: O novo esquema para o domínio.

## Notas

Embora o `ALTER DOMAIN ADD CONSTRAINT` tente verificar se os dados armazenados existentes atendem à nova restrição, essa verificação não é infalível, porque o comando não pode "ver" linhas de tabela que foram inseridas ou atualizadas recentemente e ainda não foram comprometidas. Se houver um risco de que operações concorrentes possam inserir dados errados, a maneira de proceder é adicionar a restrição usando a opção `NOT VALID`, comprometê-lo, esperar até que todas as transações iniciadas antes desse compromisso tenham sido concluídas e, em seguida, emitir `ALTER DOMAIN VALIDATE CONSTRAINT` para procurar dados que violam a restrição. Esse método é confiável porque, uma vez que a restrição é comprometida, todas as novas transações são garantidas para aplicá-la contra novos valores do tipo do domínio.

Atualmente, `ALTER DOMAIN ADD CONSTRAINT`, `ALTER DOMAIN VALIDATE CONSTRAINT` e `ALTER DOMAIN SET NOT NULL` falharão se o domínio nomeado ou qualquer domínio derivado for usado dentro de uma coluna de tipo contêiner (uma coluna composta, matriz ou de intervalo) em qualquer tabela no banco de dados. Eles devem ser aprimorados para poderem verificar a nova restrição para tais valores aninhados.

## Exemplos

Para adicionar uma restrição `NOT NULL` a um domínio:

```
ALTER DOMAIN zipcode SET NOT NULL;
```

Para remover uma restrição `NOT NULL` de um domínio:

```
ALTER DOMAIN zipcode DROP NOT NULL;
```

Para adicionar uma restrição de verificação a um domínio:

```
ALTER DOMAIN zipcode ADD CONSTRAINT zipchk CHECK (char_length(VALUE) = 5);
```

Para remover uma restrição de verificação de um domínio:

```
ALTER DOMAIN zipcode DROP CONSTRAINT zipchk;
```

Para renomear uma restrição de verificação em um domínio:

```
ALTER DOMAIN zipcode RENAME CONSTRAINT zipchk TO zip_check;
```

Para mover o domínio para um esquema diferente:

```
ALTER DOMAIN zipcode SET SCHEMA customers;
```

## Compatibilidade

`ALTER DOMAIN` é conforme com o padrão SQL, exceto para as variantes `OWNER`, `RENAME`, `SET SCHEMA` e `VALIDATE CONSTRAINT`, que são extensões do PostgreSQL. A cláusula `NOT VALID` da variante `ADD CONSTRAINT` também é uma extensão do PostgreSQL.

## Veja também

[Crie domínio](sql-createdomain.md "CREATE DOMAIN"), [Exclua domínio](sql-dropdomain.md "DROP DOMAIN")