## 43.5. PL/Perl confiável e não confiável [#](#PLPERL-TRUSTED)

Normalmente, o PL/Perl é instalado como uma linguagem de programação "confiável" chamada `plperl`. Nessa configuração, certas operações do Perl são desativadas para preservar a segurança. Em geral, as operações que são restritas são aquelas que interagem com o ambiente. Isso inclui operações com manipulação de controle de arquivo, `require` e `use` (para módulos externos). Não é possível acessar os recursos internos do processo do servidor de banco de dados ou obter acesso ao nível do sistema operacional com as permissões do processo do servidor, como uma função C pode fazer. Assim, qualquer usuário de banco de dados não privilegiado pode ser autorizado a usar essa linguagem.

### Aviso

O PL/Perl confiável depende do módulo Perl `Opcode` para preservar a segurança. O Perl [documentação](https://perldoc.perl.org/Opcode#WARNING) que o módulo não é eficaz para o caso de uso PL/Perl confiável. Se suas necessidades de segurança forem incompatíveis com a incerteza nesse aviso, considere executar `REVOKE USAGE ON LANGUAGE plperl FROM PUBLIC`.

Aqui está um exemplo de uma função que não funcionará porque as operações do sistema de arquivos não são permitidas por razões de segurança:

```
CREATE FUNCTION badfunc() RETURNS integer AS $$
    my $tmpfile = "/tmp/badfile";
    open my $fh, '>', $tmpfile
        or elog(ERROR, qq{could not open the file "$tmpfile": $!});
    print $fh "Testing writing to a file\n";
    close $fh or elog(ERROR, qq{could not close the file "$tmpfile": $!});
    return 1;
$$ LANGUAGE plperl;
```

A criação dessa função falhará, pois seu uso de uma operação proibida será detectado pelo validador.

Às vezes, é desejável escrever funções Perl que não sejam restritas. Por exemplo, pode-se querer uma função Perl que envie e-mail. Para lidar com esses casos, o PL/Perl também pode ser instalado como uma linguagem “não confiável” (geralmente chamada PL/PerlU). Neste caso, o idioma completo do Perl está disponível. Ao instalar a linguagem, o nome da linguagem `plperlu` selecionará a variante PL/Perl não confiável.

O autor de uma função PL/PerlU deve ter cuidado para que a função não possa ser usada para fazer algo indesejado, pois ela poderá fazer qualquer coisa que um usuário autenticado como administrador do banco de dados possa fazer. Observe que o sistema de banco de dados permite que apenas superusuários do banco de dados criem funções em linguagens não confiáveis.

Se a função acima foi criada por um superusuário usando a linguagem `plperlu`, a execução teria sucesso.

Da mesma forma, blocos de código anônimos escritos em Perl podem usar operações restritas se a linguagem for especificada como `plperlu` em vez de `plperl`, mas o chamador deve ser um superusuário.

### Nota

Enquanto as funções PL/Perl funcionam em um interpretador Perl separado para cada papel SQL, todas as funções PL/PerlU executadas em uma sessão dada funcionam em um único interpretador Perl (que não é nenhum dos usados para funções PL/Perl). Isso permite que as funções PL/PerlU compartilhem dados livremente, mas nenhuma comunicação pode ocorrer entre as funções PL/Perl e PL/PerlU.

### Nota

O Perl não pode suportar vários intérpretes dentro de um único processo, a menos que tenha sido construído com as bandeiras apropriadas, ou seja, `usemultiplicity` ou `useithreads`. (`usemultiplicity` é preferido, a menos que você realmente precise usar threads. Para mais detalhes, consulte a página do manual perlembed.) Se o PL/Perl for usado com uma cópia do Perl que não foi construída dessa maneira, então é possível ter apenas um intérprete Perl por sessão, e, portanto, qualquer sessão só pode executar funções PL/PerlU ou funções PL/Perl que são chamadas por todos os mesmos papéis de SQL.