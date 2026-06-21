## F.24. passwordcheck — verify password strength [#](#PASSWORDCHECK)

* [F.24.1. Configuration Parameters](passwordcheck.md#PASSWORDCHECK-CONFIGURATION-PARAMETERS)

The `passwordcheck` module checks users' passwords whenever they are set with [CREATE ROLE](sql-createrole.md "CREATE ROLE") or [ALTER ROLE](sql-alterrole.md "ALTER ROLE"). If a password is considered too weak, it will be rejected and the command will terminate with an error.

To enable this module, add `'$libdir/passwordcheck'` to [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) in `postgresql.conf`, then restart the server.

You can adapt this module to your needs by changing the source code. For example, you can use [CrackLib](https://github.com/cracklib/cracklib) to check passwords — this only requires uncommenting two lines in the `Makefile` and rebuilding the module. (We cannot include CrackLib by default for license reasons.) Without CrackLib, the module enforces a few simple rules for password strength, which you can modify or extend as you see fit.

### Caution

To prevent unencrypted passwords from being sent across the network, written to the server log or otherwise stolen by a database administrator, PostgreSQL allows the user to supply pre-encrypted passwords. Many client programs make use of this functionality and encrypt the password before sending it to the server.

This limits the usefulness of the `passwordcheck` module, because in that case it can only try to guess the password. For this reason, `passwordcheck` is not recommended if your security requirements are high. It is more secure to use an external authentication method such as GSSAPI (see [Chapter 20](client-authentication.md "Chapter 20. Client Authentication")) than to rely on passwords within the database.

Alternatively, you could modify `passwordcheck` to reject pre-encrypted passwords, but forcing users to set their passwords in clear text carries its own security risks.

### F.24.1. Configuration Parameters [#](#PASSWORDCHECK-CONFIGURATION-PARAMETERS)

`passwordcheck.min_password_length` (`integer`): The minimum acceptable password length in bytes. The default is 8. Only superusers can change this setting.

### Note

This parameter has no effect if a user supplies a pre-encrypted password.

In ordinary usage, this parameter is set in `postgresql.conf`, but superusers can alter it on-the-fly within their own sessions. Typical usage might be:

```
# postgresql.conf
passwordcheck.min_password_length = 12
```
