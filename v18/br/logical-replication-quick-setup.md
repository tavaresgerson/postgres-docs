## 29.14. Configuração Rápida [#](#LOGICAL-REPLICATION-QUICK-SETUP)

Primeiro, defina as opções de configuração em `postgresql.conf`:

```
wal_level = logical
```

Os outros ajustes necessários têm valores padrão que são suficientes para uma configuração básica.

`pg_hba.conf` precisa ser ajustado para permitir a replicação (os valores aqui dependem da sua configuração de rede real e do usuário que você deseja usar para a conexão):

```
host     all     repuser     0.0.0.0/0     scram-sha-256
```

Em seguida, no banco de dados do editor:

```
CREATE PUBLICATION mypub FOR TABLE users, departments;
```

E no banco de dados de assinantes:

```
CREATE SUBSCRIPTION mysub CONNECTION 'dbname=foo host=bar user=repuser' PUBLICATION mypub;
```

O acima iniciará o processo de replicação, que sincroniza os conteúdos iniciais das tabelas `users` e `departments` e, em seguida, começa a replicar as alterações incrementais nessas tabelas.