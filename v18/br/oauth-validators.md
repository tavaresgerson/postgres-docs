## Capítulo 50. Módulos Validadores OAuth

**Índice**

* [50.1. Projetar com segurança um módulo de validação](oauth-validator-design.md)

+ [50.1.1. Responsabilidades do Validador](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-RESPONSIBILITIES)
+ [50.1.2. Diretrizes Gerais de Codificação](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-GUIDELINES)
+ [50.1.3. Autorização de Usuários (Delegação do Usermap)](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-USERMAP-DELEGATION)

* [50.2. Funções de Inicialização](oauth-validator-init.md)
* [50.3. Retornos de Chamada do Validador OAuth](oauth-validator-callbacks.md)

+ [50.3.1. Chamada de inicialização](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-STARTUP)
+ [50.3.2. Validação de chamada de retorno](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-VALIDATE)
+ [50.3.3. Desligamento de chamada de retorno](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-SHUTDOWN)

O PostgreSQL fornece uma infraestrutura para criar módulos personalizados que realizam validação de lado do servidor de tokens OAuth. Como as implementações do OAuth variam de forma tão ampla e a validação de tokens de portador depende fortemente da parte que os emite, o servidor não pode verificar o próprio token; os módulos de validação fornecem a camada de integração entre o servidor e o provedor OAuth em uso.

Os módulos de validação OAuth devem, pelo menos, consistir em uma função de inicialização (ver [Seção 50.2] [(oauth-validator-init.md "50.2. Initialization Functions")]) e o callback necessário para realizar a validação (ver [Seção 50.3.2] [(oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-VALIDATE "50.3.2. Validate Callback")]).

### Aviso

Como um validador que se comporta mal pode permitir que usuários não autorizados acessem o banco de dados, a implementação correta é crucial para a segurança do servidor. Consulte [Seção 50.1][(oauth-validator-design.md "50.1. Safely Designing a Validator Module")] para considerações de projeto.