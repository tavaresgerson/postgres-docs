## 39.5. Regras e Privilegios [#](#RULES-PRIVILEGES)

Devido à reescrita das consultas pelo sistema de regras do PostgreSQL, outras tabelas/visões que não as utilizadas na consulta original são acessadas. Quando as regras de atualização são utilizadas, isso pode incluir acesso de escrita às tabelas.

As regras de reescrita não têm um proprietário separado. O proprietário de uma relação (tabela ou visão) é automaticamente o proprietário das regras de reescrita que são definidas para ela. O sistema de regras do PostgreSQL altera o comportamento do sistema de controle de acesso padrão. Com exceção das regras `SELECT` associadas a vistas de invocador de segurança (consulte `CREATE VIEW` (sql-createview.md "CREATE VIEW")), todas as relações que são usadas devido às regras são verificadas em relação aos privilégios do proprietário da regra, não do usuário que invoca a regra. Isso significa que, exceto para vistas de invocador de segurança, os usuários precisam apenas dos privilégios necessários para as tabelas/visões que são explicitamente nomeadas em suas consultas.

Por exemplo: um usuário tem uma lista de números de telefone, onde alguns deles são privados, e outros são de interesse para o assistente do escritório. O usuário pode construir o seguinte:

```
CREATE TABLE phone_data (person text, phone text, private boolean);
CREATE VIEW phone_number AS
    SELECT person, CASE WHEN NOT private THEN phone END AS phone
    FROM phone_data;
GRANT SELECT ON phone_number TO assistant;
```

Ninguém, exceto esse usuário (e os superusuários do banco de dados), pode acessar a tabela `phone_data`. Mas, devido ao `GRANT`, o assistente pode executar um `SELECT` na visualização `phone_number`. O sistema de regras reescreverá o `SELECT` de `phone_number` em um `SELECT` de `phone_data`. Como o usuário é o proprietário de `phone_number` e, portanto, o proprietário da regra, o acesso de leitura a `phone_data` é verificado agora contra os privilégios do usuário e a consulta é permitida. A verificação para acessar `phone_number` também é realizada, mas isso é feito contra o usuário que está invocando, então ninguém, exceto o usuário e o assistente, pode usá-lo.

Os privilégios são verificados regra por regra. Portanto, o assistente é, por enquanto, o único que pode ver os números de telefone públicos. Mas o assistente pode configurar outra visualização e conceder acesso a essa visualização ao público. Então, qualquer pessoa pode ver os dados do `phone_number` através da visualização do assistente. O que o assistente não pode fazer é criar uma visualização que acesse diretamente o `phone_data`. (Na verdade, o assistente pode, mas não funcionará, pois todo acesso será negado durante as verificações de permissão.) E assim que o usuário perceber que o assistente abriu sua visualização do `phone_number`, o usuário pode revogar o acesso do assistente. Imediatamente, qualquer acesso à visualização do assistente falhará.

Pode-se pensar que essa verificação regra por regra é uma falha de segurança, mas na verdade não é. Mas se não funcionasse dessa maneira, o assistente poderia montar uma tabela com as mesmas colunas que `phone_number` e copiar os dados para lá uma vez por dia. Então, são dados do próprio assistente e o assistente pode conceder acesso a todos que quiser. Um comando `GRANT` significa: “Eu confio em você”. Se alguém em quem você confia faz a coisa acima, é hora de pensar e depois usar `REVOKE`.

Observe que, embora as visualizações possam ser usadas para ocultar o conteúdo de certas colunas usando a técnica mostrada acima, elas não podem ser usadas para ocultar de forma confiável os dados em linhas não vistas, a menos que a bandeira `security_barrier` tenha sido definida. Por exemplo, a seguinte visualização é insegura:

```
CREATE VIEW phone_number AS
    SELECT person, phone FROM phone_data WHERE phone NOT LIKE '412%';
```

Essa visão pode parecer segura, já que o sistema de regras reescreverá qualquer `SELECT` de `phone_number` para um `SELECT` de `phone_data` e adicionará a qualificação de que apenas as entradas onde `phone` não começa com 412 são desejadas. Mas se o usuário puder criar suas próprias funções, não é difícil convencer o planejador a executar a função definida pelo usuário antes da expressão `NOT LIKE`. Por exemplo:

```
CREATE FUNCTION tricky(text, text) RETURNS bool AS $$
BEGIN
    RAISE NOTICE '% => %', $1, $2;
    RETURN true;
END;
$$ LANGUAGE plpgsql COST 0.0000000000000000000001;

SELECT * FROM phone_number WHERE tricky(person, phone);
```

Cada pessoa e número de telefone na tabela `phone_data` será impresso como um `NOTICE`, porque o planejador optará por executar a função barata `tricky` antes da mais cara `NOT LIKE`. Mesmo que o usuário seja impedido de definir novas funções, funções embutidas podem ser usadas em ataques semelhantes. (Por exemplo, a maioria das funções de conversão inclui seus valores de entrada nos erros que produzem.)

Considerações semelhantes se aplicam às regras de atualização. Nos exemplos da seção anterior, o proprietário das tabelas no banco de dados de exemplo poderia conceder os privilégios `SELECT`, `INSERT`, `UPDATE` e `DELETE` na visão `shoelace` a outra pessoa, mas apenas `SELECT` na `shoelace_log`. A ação da regra para escrever entradas de log ainda será executada com sucesso, e esse outro usuário poderá ver as entradas de log. Mas eles não poderiam criar entradas falsas, nem poderiam manipular ou remover as existentes. Neste caso, não há possibilidade de subverter as regras convencendo o planejador a alterar a ordem das operações, porque a única regra que faz referência a `shoelace_log` é uma `INSERT` não qualificada. Isso pode não ser verdade em cenários mais complexos.

Quando é necessário que uma visão forneça segurança em nível de linha, o atributo `security_barrier` deve ser aplicado à visão. Isso impede que funções e operadores escolhidos maliciosamente recebam valores de linhas até que a visão tenha terminado seu trabalho. Por exemplo, se a visão mostrada acima tivesse sido criada assim, seria segura:

```
CREATE VIEW phone_number WITH (security_barrier) AS
    SELECT person, phone FROM phone_data WHERE phone NOT LIKE '412%';
```

As visualizações criadas com o `security_barrier` podem se sair muito pior do que as visualizações criadas sem essa opção. Em geral, não há como evitar isso: o plano mais rápido possível deve ser rejeitado se ele possa comprometer a segurança. Por esse motivo, essa opção não é ativada por padrão.

O planejador de consultas tem mais flexibilidade ao lidar com funções que não têm efeitos colaterais. Essas funções são referidas como `LEAKPROOF` e incluem muitos operadores simples e comumente usados, como muitos operadores de igualdade. O planejador de consultas pode permitir que essas funções sejam avaliadas em qualquer ponto do processo de execução da consulta, pois invocá-las em linhas invisíveis ao usuário não vazará nenhuma informação sobre as linhas não vistas. Além disso, funções que não aceitam argumentos ou que não recebem argumentos da vista da barreira de segurança não precisam ser marcadas como `LEAKPROOF` para serem empurradas para baixo, pois nunca recebem dados da vista. Em contraste, uma função que pode lançar um erro dependendo dos valores recebidos como argumentos (como uma que lança um erro no caso de overflow ou divisão por zero) não é à prova de vazamento e poderia fornecer informações significativas sobre as linhas não vistas se aplicada antes dos filtros de linha da vista.

Por exemplo, um índice não pode ser selecionado para consultas em visualizações de barreiras de segurança (ou tabelas com políticas de segurança a nível de linha) se um operador usado na cláusula `WHERE` estiver associado à família de operadores do índice, mas sua função subjacente não estiver marcada `LEAKPROOF`. O meta-comando `\dAo+` do programa [psql](app-psql.md) é útil para listar famílias de operadores e determinar quais de seus operadores estão marcados como à prova de vazamento.

É importante entender que, mesmo uma visão criada com a opção `security_barrier` é destinada a ser segura apenas no sentido limitado de que o conteúdo dos tuplos invisíveis não será passado para funções possivelmente inseguras. O usuário pode ter outros meios de fazer inferências sobre os dados invisíveis; por exemplo, eles podem ver o plano de consulta usando `EXPLAIN`, ou medir o tempo de execução das consultas contra a visão. Um atacante malicioso pode ser capaz de inferir algo sobre a quantidade de dados invisíveis, ou até mesmo obter alguma informação sobre a distribuição dos dados ou os valores mais comuns (já que essas coisas podem afetar o tempo de execução do plano; ou até mesmo, já que também são refletidas nas estatísticas do otimizador, a escolha do plano). Se esses tipos de ataques de "canal oculto" são preocupantes, provavelmente não é sábio conceder qualquer acesso aos dados.