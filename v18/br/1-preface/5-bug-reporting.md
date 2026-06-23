## 5. Diretrizes para Relatar Bugs [#](#BUG-REPORTING)

* [5.1. Identificando Bugs](bug-reporting.md#BUG-REPORTING-IDENTIFYING-BUGS)
* [5.2. O que Relatar](bug-reporting.md#BUG-REPORTING-WHAT-TO-REPORT)
* [5.3. Onde Relatar Bugs](bug-reporting.md#BUG-REPORTING-WHERE-TO-REPORT-BUGS)

Quando você encontrar um erro no PostgreSQL, queremos saber sobre isso. Seus relatórios de bugs desempenham um papel importante em tornar o PostgreSQL mais confiável, porque nem o cuidado máximo pode garantir que cada parte do PostgreSQL funcione em todas as plataformas em todas as circunstâncias.

As sugestões a seguir visam ajudá-lo a formular relatórios de bugs que podem ser tratados de maneira eficaz. Ninguém é obrigado a segui-las, mas fazê-lo tende a ser a vantagem de todos.

Não podemos prometer corrigir todos os erros de uma só vez. Se o erro for óbvio, crítico ou afetar muitos usuários, é provável que alguém o analise. Também pode acontecer que lhe digamos atualizar para uma versão mais recente para ver se o erro acontece lá. Ou podemos decidir que o erro não pode ser corrigido antes de algumas reescritas importantes que podemos estar planejando serem feitas. Ou talvez seja simplesmente muito difícil e há coisas mais importantes na agenda. Se você precisa de ajuda imediatamente, considere obter um contrato de suporte comercial.

### 5.1. Identificação de Bugs [#](#BUG-REPORTING-IDENTIFYING-BUGS)

Antes de relatar um erro, leia e releia a documentação para verificar se realmente pode fazer o que está tentando. Se não estiver claro na documentação se você pode fazer algo ou não, informe isso também; é um erro na documentação. Se descobrir que um programa faz algo diferente do que a documentação diz, isso é um erro. Isso pode incluir, mas não está limitado a, as seguintes circunstâncias:

* Um programa termina com um sinal fatal ou uma mensagem de erro do sistema operacional que apontaria para um problema no programa. (Um contraexemplo pode ser uma mensagem de "disco cheio", pois você precisa consertar isso você mesmo.)
* Um programa produz a saída errada para qualquer entrada dada.
* Um programa se recusa a aceitar entrada válida (conforme definido na documentação).
* Um programa aceita entrada inválida sem uma notificação ou mensagem de erro. Mas tenha em mente que sua ideia de entrada inválida pode ser nossa ideia de extensão ou compatibilidade com a prática tradicional.
* O PostgreSQL não se compila, constrói ou instala de acordo com as instruções em plataformas suportadas.

Aqui, “programa” se refere a qualquer executável, não apenas o processo de backend.

Ser lento ou consumir recursos de forma excessiva não é necessariamente um bug. Leia a documentação ou peça ajuda em uma das listas de correio para ajustar suas aplicações. Não cumprir o padrão SQL não é necessariamente um bug, a menos que a conformidade para o recurso específico seja explicitamente reivindicada.

Antes de continuar, verifique a lista TODO e nas Perguntas Frequentes para ver se seu problema já é conhecido. Se você não conseguir decodificar as informações na lista TODO, informe seu problema. O mínimo que podemos fazer é tornar a lista TODO mais clara.

### 5.2. O que relatar [#](#BUG-REPORTING-WHAT-TO-REPORT)

A coisa mais importante a lembrar sobre o relato de bugs é declarar todos os fatos e apenas os fatos. Não especule o que você acha que deu errado, o que “pareceu fazer” ou qual parte do programa tem uma falha. Se você não está familiarizado com a implementação, provavelmente vai errar e não nos ajudar um pouco. E mesmo que esteja, explicações educadas são um ótimo complemento, mas não substituem os fatos. Se vamos corrigir o bug, ainda temos que vê-lo acontecer por nós mesmos primeiro. Relatar os fatos básicos é relativamente simples (você provavelmente pode copiá-los e colá-los da tela), mas muitas vezes detalhes importantes são deixados de lado porque alguém pensou que não importa ou o relatório seria entendido de qualquer maneira.

Os seguintes itens devem ser incluídos em cada relatório de bug:

* A sequência exata dos passos * a partir do início do programa * necessários para reproduzir o problema. Isso deve ser autossuficiente; não é suficiente enviar uma declaração `SELECT` sem as declarações `CREATE TABLE` e `INSERT` anteriores, se a saída deve depender dos dados nas tabelas. Não temos o tempo para engenharia reversa do esquema do seu banco de dados, e se estamos supostos a criar nossos próprios dados, provavelmente perderemos o problema.

O melhor formato para um caso de teste para problemas relacionados a SQL é um arquivo que pode ser executado através do frontend psql que mostra o problema. (Certifique-se de não ter nada em seu arquivo de inicialização `~/.psqlrc`. Uma maneira fácil de criar esse arquivo é usar pg_dump para drenar as declarações de tabela e os dados necessários para definir a cena, e depois adicionar a consulta do problema. Você é incentivado a minimizar o tamanho do seu exemplo, mas isso não é absolutamente necessário. Se o erro for reprodutível, encontraremos de qualquer maneira.

Se o seu aplicativo usa outra interface de cliente, como PHP, tente isolar as consultas que geram o problema. Provavelmente não configuraremos um servidor web para reproduzir o seu problema. Em qualquer caso, lembre-se de fornecer os arquivos de entrada exatos; não pense que o problema ocorre com "arquivos grandes" ou "bancos de dados de tamanho médio", etc., pois essas informações são muito inexatas para serem úteis.
* A saída que você obteve. Não diga que "não funcionou" ou "quebrou". Se houver uma mensagem de erro, mostre-a, mesmo que você não a entenda. Se o programa terminar com um erro do sistema operacional, diga qual. Se nada aconteça, diga isso. Mesmo que o resultado do seu caso de teste seja um programa quebrado ou de outra forma óbvio, pode não acontecer na nossa plataforma. A coisa mais fácil é copiar a saída do terminal, se possível.

### Nota

Se você está relatando uma mensagem de erro, obtenha a forma mais detalhada da mensagem. Em psql, diga `\set VERBOSITY verbose` previamente. Se você está extraindo a mensagem do log do servidor, defina o parâmetro de tempo de execução [log_error_verbosity](runtime-config-logging.md#GUC-LOG-ERROR-VERBOSITY) para `verbose` para que todos os detalhes sejam registrados.

### Nota

Em caso de erros fatais, a mensagem de erro relatada pelo cliente pode não conter todas as informações disponíveis. Além disso, consulte a saída do log do servidor de banco de dados. Se você não manter a saída do log do seu servidor, seria um bom momento para começar a fazer isso.
* A saída que você espera é muito importante de ser declarada. Se você apenas escrever “Este comando me dá essa saída.” ou “Isso não é o que eu esperava.”, podemos executar o comando nós mesmos, analisar a saída e pensar que ela parece OK e é exatamente o que esperávamos. Não devemos ter que gastar tempo para decodificar a semântica exata por trás dos seus comandos. Especialmente, não se afaste apenas dizendo que “Isso não é o que diz o SQL ou o Oracle.” Descobrir o comportamento correto do SQL não é uma tarefa divertida, e nem todos nós sabemos como todos os outros bancos relacionais lá fora se comportam. (Se o seu problema é um travamento do programa, você pode obviamente omitir este item.)
* Quaisquer opções de linha de comando e outras opções de inicialização, incluindo quaisquer variáveis de ambiente relevantes ou arquivos de configuração que você alterou a partir do padrão. Novamente, forneça informações exatas. Se você está usando uma distribuição pré-embalada que inicia o servidor de banco de dados no momento do boot, você deve tentar descobrir como isso é feito.
* Tudo o que você fez de maneira diferente das instruções de instalação.
* A versão do PostgreSQL. Você pode executar o comando `SELECT version();` para descobrir a versão do servidor com o qual você está conectado. A maioria dos programas executáveis também suporta uma opção `--version`; pelo menos `postgres --version` e `psql --version` devem funcionar. Se a função ou as opções não existirem, então sua versão é mais do que suficientemente antiga para justificar uma atualização. Se você executar uma versão pré-embalada, como RPMs, diga isso, incluindo qualquer subversão que o pacote possa ter. Se você está falando sobre um snapshot do Git, mencione isso, incluindo o hash do commit.

Se sua versão for mais antiga que 18.4, quase certamente vamos te dizer para fazer uma atualização. Há muitas correções de bugs e melhorias em cada nova versão, então é bem possível que um bug que você encontrou em uma versão mais antiga do PostgreSQL já tenha sido corrigido. Só podemos fornecer suporte limitado para sites que usam versões mais antigas do PostgreSQL; se você precisar de mais do que o que podemos fornecer, considere adquirir um contrato de suporte comercial.
* Informações da plataforma. Isso inclui o nome e a versão do kernel, a biblioteca C, o processador, informações de memória, e assim por diante. Na maioria dos casos, é suficiente relatar o fornecedor e a versão, mas não presuma que todos saibam exatamente o que “Debian” contém ou que todos funcionam no x86_64. Se você tiver problemas de instalação, as informações sobre a ferramenta na sua máquina (compilador, make, e assim por diante) também são necessárias.

Não tenha medo se seu relatório de bug se tornar bastante extenso. Esse é um fato da vida. É melhor relatar tudo na primeira vez do que ter que extrair os fatos de você. Por outro lado, se seus arquivos de entrada são enormes, é justo perguntar primeiro se alguém está interessado em examiná-los. Aqui está um [artigo](https://www.chiark.greenend.org.uk/~sgtatham/bugs.html) que descreve algumas dicas adicionais sobre relatórios de bugs.

Não passe todo o seu tempo descobrindo quais mudanças na entrada fazem o problema desaparecer. Provavelmente, isso não ajudará a resolvê-lo. Se descobrir que o erro não pode ser corrigido imediatamente, ainda terá tempo para encontrar e compartilhar sua solução. Além disso, mais uma vez, não perca tempo adivinhando por que o erro existe. Descobriremos isso em breve.

Ao escrever um relatório de bug, evite usar termos confusos. O pacote de software no total é chamado de “PostgreSQL”, às vezes abreviado como “Postgres”. Se você estiver falando especificamente sobre o processo de backend, mencione isso, não apenas diga “PostgreSQL trava”. Uma falha de um único processo de backend é bem diferente de uma falha do processo principal “postgres”; por favor, não diga “o servidor travou” quando você quer dizer que um único processo de backend caiu, nem vice-versa. Além disso, programas de cliente, como o frontend interativo “psql”, são completamente separados do backend. Por favor, tente ser específico sobre se o problema está no lado do cliente ou do servidor.

### 5.3. Onde relatar bugs [#](#BUG-REPORTING-WHERE-TO-REPORT-BUGS)

Em geral, envie relatórios de bugs para a lista de correio de relatórios de bugs em `<pgsql-bugs@lists.postgresql.org>`. Você é solicitado a usar um assunto descritivo para sua mensagem de e-mail, talvez partes da mensagem de erro.

Outro método é preencher o formulário de relatório de bugs disponível no site do projeto [web site](https://www.postgresql.org/account/submitbug/). Ao inserir um relatório de bugs dessa forma, ele é enviado por e-mail para a lista de discussão `<pgsql-bugs@lists.postgresql.org>`.

Se o seu relatório de erro tiver implicações de segurança e você preferir que ele não seja imediatamente visível em arquivos públicos, não o envie para `pgsql-bugs`. Questões de segurança podem ser relatadas privadamente para `<security@postgresql.org>`.

Não envie relatórios de bugs para nenhuma das listas de correio do usuário, como `<pgsql-sql@lists.postgresql.org>` ou `<pgsql-general@lists.postgresql.org>`. Essas listas de correio são para responder a perguntas do usuário, e seus assinantes normalmente não desejam receber relatórios de bugs. Mais importante ainda, é improvável que eles os corrijam.

Além disso, por favor, não envie relatórios para a lista de correio dos desenvolvedores `<pgsql-hackers@lists.postgresql.org>`. Esta lista é para discutir o desenvolvimento do PostgreSQL, e seria bom se pudéssemos manter os relatórios de bugs separados. Podemos optar por discutir seu relatório de bug no `pgsql-hackers`, se o problema precisar de mais revisão.

Se você tiver um problema com a documentação, o melhor lugar para relatar é a lista de correio da documentação `<pgsql-docs@lists.postgresql.org>`. Seja específico sobre qual parte da documentação você não está satisfeita.

Se o seu problema for um problema de portabilidade em uma plataforma não suportada, envie um e-mail para `<pgsql-hackers@lists.postgresql.org>`, para que nós (e você) possamos trabalhar na portabilidade do PostgreSQL para sua plataforma.

### Nota

Devido à quantidade infeliz de spam que circula, todos os listados acima serão moderados, a menos que você esteja inscrito. Isso significa que haverá um certo atraso antes do e-mail ser entregue. Se você deseja se inscrever nas listas, por favor, visite <https://lists.postgresql.org/> para obter instruções.