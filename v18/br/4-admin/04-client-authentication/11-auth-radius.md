## 20.11. Autenticação RADIUS [#](#AUTH-RADIUS)

Este método de autenticação opera de forma semelhante ao `password`, exceto que ele usa RADIUS como o método de verificação de senha. O RADIUS é usado apenas para validar os pares de nome/senha do usuário. Portanto, o usuário deve já existir no banco de dados antes que o RADIUS possa ser usado para autenticação.

Ao usar autenticação RADIUS, uma mensagem de Solicitação de Acesso será enviada ao servidor RADIUS configurado. Essa solicitação será do tipo `Authenticate Only`, e incluirá parâmetros para `user name`, `password` (criptografado) e `NAS Identifier`. A solicitação será criptografada usando um segredo compartilhado com o servidor. O servidor RADIUS responderá a essa solicitação com `Access Accept` ou `Access Reject`. Não há suporte para contabilidade RADIUS.

Pode-se especificar vários servidores RADIUS, no caso, eles serão testados sequencialmente. Se uma resposta negativa for recebida de um servidor, a autenticação falhará. Se nenhuma resposta for recebida, o próximo servidor na lista será testado. Para especificar vários servidores, separe os nomes dos servidores com vírgulas e envolva a lista em aspas duplas. Se vários servidores forem especificados, as outras opções de RADIUS também podem ser fornecidas como listas separadas por vírgula, para fornecer valores individuais para cada servidor. Eles também podem ser especificados como um único valor, no caso, esse valor se aplicará a todos os servidores.

As seguintes opções de configuração são suportadas para RADIUS:

`radiusservers`: Os nomes de DNS ou endereços IP dos servidores RADIUS para se conectar. Este parâmetro é obrigatório.

`radiussecrets`: Os segredos compartilhados usados ao se comunicar de forma segura com os servidores RADIUS. Isso deve ter exatamente o mesmo valor nos servidores PostgreSQL e RADIUS. É recomendável que essa seja uma string com pelo menos 16 caracteres. Este parâmetro é obrigatório.

Nota

O vetor de criptografia utilizado será apenas criptograficamente forte se o PostgreSQL for construído com suporte para OpenSSL. Em outros casos, a transmissão para o servidor RADIUS só deve ser considerada ofuscada, não protegida, e medidas de segurança externas devem ser aplicadas, se necessário.

`radiusports`: Os números de porta para se conectar aos servidores RADIUS. Se nenhuma porta for especificada, a porta padrão RADIUS (`1812`) será usada.

`radiusidentifiers`: As cadeias de caracteres que serão usadas como `NAS Identifier` nas solicitações RADIUS. Este parâmetro pode ser usado, por exemplo, para identificar qual grupo de bancos o usuário está tentando conectar, o que pode ser útil para a correspondência de políticas no servidor RADIUS. Se nenhum identificador for especificado, o `postgresql` padrão será usado.

Se for necessário ter uma vírgula ou espaço em branco em um valor de parâmetro RADIUS, isso pode ser feito colocando aspas duplas ao redor do valor, mas é tedioso porque agora são necessárias duas camadas de aspas duplas. Um exemplo de colocar espaço em branco em strings secretas RADIUS é:

```
host ... radius radiusservers="server1,server2" radiussecrets="""secret one"",""secret two"""
```
