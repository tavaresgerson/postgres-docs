## Capítulo 64. Registro antecipado para extensões

**Índice**

* [64.1. Registros genéricos WAL](generic-wal.md)
* [64.2. Gerenciadores de recursos WAL personalizados](custom-rmgr.md)

Algumas extensões, principalmente as que implementam métodos de acesso personalizados, podem precisar realizar log de escrita antecipada para garantir a segurança em caso de falha. O PostgreSQL oferece duas maneiras para as extensões alcançarem esse objetivo.

Em primeiro lugar, as extensões podem optar por usar [generic WAL](generic-wal.md), um tipo especial de registro WAL que descreve as alterações nas páginas de uma maneira genérica. Esse método é simples de implementar e não exige que uma biblioteca de extensão seja carregada para aplicar os registros. No entanto, os registros WAL genéricos serão ignorados ao realizar a decodificação lógica.

Em segundo lugar, as extensões podem optar por usar um gerenciador de recursos [custom](custom-rmgr.md). Esse método é mais flexível, suporta decodificação lógica e, às vezes, pode gerar registros de log de pré-escrita muito menores do que seria possível com o WAL genérico. No entanto, é mais complexo para uma extensão implementar.