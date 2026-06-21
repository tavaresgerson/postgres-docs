## 43.4. Valores globais em PL/Perl [#](#PLPERL-GLOBAL)

Você pode usar o hash global `%_SHARED` para armazenar dados, incluindo referências de código, entre chamadas de função para a vida útil da sessão atual.

Aqui está um exemplo simples para dados compartilhados:

```
CREATE OR REPLACE FUNCTION set_var(name text, val text) RETURNS text AS $$
    if ($_SHARED{$_[0]} = $_[1]) {
        return 'ok';
    } else {
        return "cannot set shared variable $_[0] to $_[1]";
    }
$$ LANGUAGE plperl;

CREATE OR REPLACE FUNCTION get_var(name text) RETURNS text AS $$
    return $_SHARED{$_[0]};
$$ LANGUAGE plperl;

SELECT set_var('sample', 'Hello, PL/Perl!  How''s tricks?');
SELECT get_var('sample');
```

Aqui está um exemplo um pouco mais complicado, usando uma referência de código:

```
CREATE OR REPLACE FUNCTION myfuncs() RETURNS void AS $$
    $_SHARED{myquote} = sub {
        my $arg = shift;
        $arg =~ s/(['\\])/\\$1/g;
        return "'$arg'";
    };
$$ LANGUAGE plperl;

SELECT myfuncs(); /* initializes the function */

/* Set up a function that uses the quote function */

CREATE OR REPLACE FUNCTION use_quote(TEXT) RETURNS text AS $$
    my $text_to_quote = shift;
    my $qfunc = $_SHARED{myquote};
    return &$qfunc($text_to_quote);
$$ LANGUAGE plperl;
```

(Você poderia ter substituído o acima pelo comando `return $_SHARED{myquote}->($_[0]);` em detrimento da legibilidade.)

Por razões de segurança, o PL/Perl executa funções chamadas por qualquer um dos papéis SQL em um interpretador Perl separado para esse papel. Isso previne interferência acidental ou maliciosa de um usuário no comportamento das funções PL/Perl de outro usuário. Cada interpretador tem seu próprio valor da variável `%_SHARED` e outro estado global. Assim, duas funções PL/Perl compartilharão o mesmo valor de `%_SHARED` se e somente se forem executadas pelo mesmo papel SQL. Em uma aplicação em que uma única sessão executa código sob múltiplos papéis SQL (através de funções `SECURITY DEFINER`, uso de `SET ROLE`, etc.), você pode precisar tomar medidas explícitas para garantir que as funções PL/Perl possam compartilhar dados via `%_SHARED`. Para isso, certifique-se de que as funções que devem se comunicar sejam de propriedade do mesmo usuário e marque-as `SECURITY DEFINER`. Você deve, naturalmente, ter cuidado para que tais funções não possam ser usadas para fazer algo não intencional.