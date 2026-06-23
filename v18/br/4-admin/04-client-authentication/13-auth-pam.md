## 20.13. Autenticação PAM [#](#AUTH-PAM)

Este método de autenticação opera de forma semelhante ao `password`, exceto que utiliza módulos de autenticação intercambiáveis (PAM - Pluggable Authentication Modules) como mecanismo de autenticação. O nome padrão do serviço PAM é `postgresql`. O PAM é usado apenas para validar pares de nome/senha do usuário e, opcionalmente, o nome do host remoto conectado ou o endereço IP. Portanto, o usuário deve já existir no banco de dados antes que o PAM possa ser usado para autenticação. Para mais informações sobre o PAM, leia a página [Linux-PAM](https://www.kernel.org/pub/linux/libs/pam/).

As seguintes opções de configuração são suportadas para o PAM:

`pamservice`: Nome do serviço PAM.

`pam_use_hostname`: Determina se o endereço IP remoto ou o nome do host é fornecido aos módulos PAM através do item `PAM_RHOST`. Por padrão, o endereço IP é usado. Defina esta opção para 1 para usar o nome do host resolvido em vez disso. A resolução do nome do host pode levar a atrasos no login. (A maioria das configurações PAM não usa essas informações, portanto, é necessário considerar apenas esse ajuste se uma configuração PAM foi especificamente criada para usá-la.)

Nota

Se o PAM estiver configurado para ler `/etc/shadow`, a autenticação falhará porque o servidor PostgreSQL é iniciado por um usuário que não é root. No entanto, isso não é um problema quando o PAM está configurado para usar LDAP ou outros métodos de autenticação.