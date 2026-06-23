## 44.3. Compartilhamento de Dados [#](#PLPYTHON-SHARING)

O dicionário global `SD` está disponível para armazenar dados privados entre chamadas repetidas à mesma função. O dicionário global `GD` é um dado público, ou seja, disponível para todas as funções do Python dentro de uma sessão; use com cuidado.

Cada função recebe seu próprio ambiente de execução no interpretador Python, para que os dados globais e os argumentos da função de `myfunc` não estejam disponíveis para `myfunc2`. A exceção é o dado no dicionário de `GD`, conforme mencionado acima.