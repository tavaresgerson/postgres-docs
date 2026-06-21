## Appendix M. Glossary

This is a list of terms and their meaning in the context of PostgreSQL and relational database systems in general.

ACID: [*[Atomicity](glossary.md#GLOSSARY-ATOMICITY "Atomicity")*](glossary.md#GLOSSARY-ATOMICITY), [*[Consistency](glossary.md#GLOSSARY-CONSISTENCY "Consistency")*](glossary.md#GLOSSARY-CONSISTENCY), [*[Isolation](glossary.md#GLOSSARY-ISOLATION "Isolation")*](glossary.md#GLOSSARY-ISOLATION), and [*[Durability](glossary.md#GLOSSARY-DURABILITY "Durability")*](glossary.md#GLOSSARY-DURABILITY). This set of properties of database transactions is intended to guarantee validity in concurrent operation and even in event of errors, power failures, etc.

Aggregate function (routine): A [*[function](glossary.md#GLOSSARY-FUNCTION "Function (routine)")*](glossary.md#GLOSSARY-FUNCTION) that combines (*aggregates*) multiple input values, for example by counting, averaging or adding, yielding a single output value.

For more information, see [Section 9.21](functions-aggregate.md "9.21. Aggregate Functions").

See Also [Window function (routine)](glossary.md#GLOSSARY-WINDOW-FUNCTION).

Access Method: Interfaces which PostgreSQL use in order to access data in tables and indexes. This abstraction allows for adding support for new types of data storage.

For more information, see [Chapter 62](tableam.md "Chapter 62. Table Access Method Interface Definition") and [Chapter 63](indexam.md "Chapter 63. Index Access Method Interface Definition").

Analytic function: See [Window function (routine)](glossary.md#GLOSSARY-WINDOW-FUNCTION).

Analyze (operation): The act of collecting statistics from data in [*[tables](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) and other [*[relations](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) to help the [*[query planner](glossary.md#GLOSSARY-PLANNER "Query planner")*](glossary.md#GLOSSARY-PLANNER) to make decisions about how to execute [*[queries](glossary.md#GLOSSARY-QUERY "Query")*](glossary.md#GLOSSARY-QUERY).

(Don't confuse this term with the `ANALYZE` option to the [EXPLAIN](sql-explain.md "EXPLAIN") command.)

For more information, see [ANALYZE](sql-analyze.md "ANALYZE").

Asynchronous I/O (AIO): Asynchronous I/O (AIO) describes performing I/O in a non-blocking way (asynchronously), in contrast to synchronous I/O, which blocks for the entire duration of the I/O.

With AIO, starting an I/O operation is separated from waiting for the result of the operation, allowing multiple I/O operations to be initiated concurrently, as well as performing CPU heavy operations concurrently with I/O. The price for that increased concurrency is increased complexity.

See Also [Input/Output](glossary.md#GLOSSARY-IO).

Atomic: In reference to a [*[datum](glossary.md#GLOSSARY-DATUM "Datum")*](glossary.md#GLOSSARY-DATUM): the fact that its value cannot be broken down into smaller components.: In reference to a [*[database transaction](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossary.md#GLOSSARY-TRANSACTION): see [*[atomicity](glossary.md#GLOSSARY-ATOMICITY "Atomicity")*](glossary.md#GLOSSARY-ATOMICITY).

Atomicity: The property of a [*[transaction](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossary.md#GLOSSARY-TRANSACTION) that either all its operations complete as a single unit or none do. In addition, if a system failure occurs during the execution of a transaction, no partial results are visible after recovery. This is one of the ACID properties.

Attribute: An element with a certain name and data type found within a [*[tuple](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE).

Autovacuum (process): A set of background processes that routinely perform [*[vacuum](glossary.md#GLOSSARY-VACUUM "Vacuum")*](glossary.md#GLOSSARY-VACUUM) and [*[analyze](glossary.md#GLOSSARY-ANALYZE "Analyze (operation)")*](glossary.md#GLOSSARY-ANALYZE) operations. The [*[auxiliary process](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) that coordinates the work and is always present (unless autovacuum is disabled) is known as the *autovacuum launcher*, and the processes that carry out the tasks are known as the *autovacuum workers*.

For more information, see [Section 24.1.6](routine-vacuuming.md#AUTOVACUUM "24.1.6. The Autovacuum Daemon").

Auxiliary process: A process within an [*[instance](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossary.md#GLOSSARY-INSTANCE) that is in charge of some specific background task for the instance. The auxiliary processes consist of the [*[autovacuum launcher](glossary.md#GLOSSARY-AUTOVACUUM "Autovacuum (process)")*](glossary.md#GLOSSARY-AUTOVACUUM) (but not the autovacuum workers), the [*[background writer](glossary.md#GLOSSARY-BACKGROUND-WRITER "Background writer (process)")*](glossary.md#GLOSSARY-BACKGROUND-WRITER), the [*[checkpointer](glossary.md#GLOSSARY-CHECKPOINTER "Checkpointer (process)")*](glossary.md#GLOSSARY-CHECKPOINTER), the [*[logger](glossary.md#GLOSSARY-LOGGER "Logger (process)")*](glossary.md#GLOSSARY-LOGGER), the [*[startup process](glossary.md#GLOSSARY-STARTUP-PROCESS "Startup process")*](glossary.md#GLOSSARY-STARTUP-PROCESS), the [*[WAL archiver](glossary.md#GLOSSARY-WAL-ARCHIVER "WAL archiver (process)")*](glossary.md#GLOSSARY-WAL-ARCHIVER), the [*[WAL receiver](glossary.md#GLOSSARY-WAL-RECEIVER "WAL receiver (process)")*](glossary.md#GLOSSARY-WAL-RECEIVER) (but not the [*[WAL senders](glossary.md#GLOSSARY-WAL-SENDER "WAL sender (process)")*](glossary.md#GLOSSARY-WAL-SENDER)), the [*[WAL summarizer](glossary.md#GLOSSARY-WAL-SUMMARIZER "WAL summarizer (process)")*](glossary.md#GLOSSARY-WAL-SUMMARIZER), and the [*[WAL writer](glossary.md#GLOSSARY-WAL-WRITER "WAL writer (process)")*](glossary.md#GLOSSARY-WAL-WRITER).

Backend (process): Process of an [*[instance](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossary.md#GLOSSARY-INSTANCE) which acts on behalf of a [*[client session](glossary.md#GLOSSARY-SESSION "Session")*](glossary.md#GLOSSARY-SESSION) and handles its requests.

(Don't confuse this term with the similar terms [*[Background Worker](glossary.md#GLOSSARY-BACKGROUND-WORKER "Background worker (process)")*](glossary.md#GLOSSARY-BACKGROUND-WORKER) or [*[Background Writer](glossary.md#GLOSSARY-BACKGROUND-WRITER "Background writer (process)")*](glossary.md#GLOSSARY-BACKGROUND-WRITER)).

Background worker (process): Process within an [*[instance](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossary.md#GLOSSARY-INSTANCE), which runs system- or user-supplied code. Serves as infrastructure for several features in PostgreSQL, such as [*[logical replication](glossary.md#GLOSSARY-REPLICATION "Replication")*](glossary.md#GLOSSARY-REPLICATION) and [*[parallel queries](glossary.md#GLOSSARY-PARALLEL-QUERY "Parallel query")*](glossary.md#GLOSSARY-PARALLEL-QUERY). In addition, [*[Extensions](glossary.md#GLOSSARY-EXTENSION "Extension")*](glossary.md#GLOSSARY-EXTENSION) can add custom background worker processes.

For more information, see [Chapter 46](bgworker.md "Chapter 46. Background Worker Processes").

Background writer (process): An [*[auxiliary process](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) that writes dirty [*[data pages](glossary.md#GLOSSARY-DATA-PAGE "Data page")*](glossary.md#GLOSSARY-DATA-PAGE) from [*[shared memory](glossary.md#GLOSSARY-SHARED-MEMORY "Shared memory")*](glossary.md#GLOSSARY-SHARED-MEMORY) to the file system. It wakes up periodically, but works only for a short period in order to distribute its expensive I/O activity over time to avoid generating larger I/O peaks which could block other processes.

For more information, see [Section 19.4.4](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER "19.4.4. Background Writer").

Base Backup: A binary copy of all [*[database cluster](glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*](glossary.md#GLOSSARY-DB-CLUSTER) files. It is generated by the tool [pg_basebackup](app-pgbasebackup.md "pg_basebackup"). In combination with WAL files it can be used as the starting point for recovery, log shipping, or streaming replication.

Bloat: Space in data pages which does not contain current row versions, such as unused (free) space or outdated row versions.

Bootstrap superuser: The first [*[user](glossary.md#GLOSSARY-USER "User")*](glossary.md#GLOSSARY-USER) initialized in a [*[database cluster](glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*](glossary.md#GLOSSARY-DB-CLUSTER).

This user owns all system catalog tables in each database. It is also the role from which all granted permissions originate. Because of these things, this role may not be dropped.

This role also behaves as a normal [*[database superuser](glossary.md#GLOSSARY-DATABASE-SUPERUSER "Database superuser")*](glossary.md#GLOSSARY-DATABASE-SUPERUSER), and its superuser status cannot be removed.

Buffer Access Strategy: Some operations will access a large number of [*[pages](glossary.md#GLOSSARY-DATA-PAGE "Data page")*](glossary.md#GLOSSARY-DATA-PAGE). A *Buffer Access Strategy* helps to prevent these operations from evicting too many pages from [*[shared buffers](glossary.md#GLOSSARY-SHARED-MEMORY "Shared memory")*](glossary.md#GLOSSARY-SHARED-MEMORY).

A Buffer Access Strategy sets up references to a limited number of [*[shared buffers](glossary.md#GLOSSARY-SHARED-MEMORY "Shared memory")*](glossary.md#GLOSSARY-SHARED-MEMORY) and reuses them circularly. When the operation requires a new page, a victim buffer is chosen from the buffers in the strategy ring, which may require flushing the page's dirty data and possibly also unflushed [*[WAL](glossary.md#GLOSSARY-WAL "Write-ahead log")*](glossary.md#GLOSSARY-WAL) to permanent storage.

Buffer Access Strategies are used for various operations such as sequential scans of large tables, `VACUUM`, `COPY`, `CREATE TABLE AS SELECT`, `ALTER TABLE`, `CREATE DATABASE`, `CREATE INDEX`, and `CLUSTER`.

Cast: A conversion of a [*[datum](glossary.md#GLOSSARY-DATUM "Datum")*](glossary.md#GLOSSARY-DATUM) from its current data type to another data type.

For more information, see [CREATE CAST](sql-createcast.md "CREATE CAST").

Catalog: The SQL standard uses this term to indicate what is called a [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) in PostgreSQL's terminology.

(Don't confuse this term with [*[system catalog](glossary.md#GLOSSARY-SYSTEM-CATALOG "System catalog")*](glossary.md#GLOSSARY-SYSTEM-CATALOG)).

For more information, see [Section 22.1](manage-ag-overview.md "22.1. Overview").

Check constraint: A type of [*[constraint](glossary.md#GLOSSARY-CONSTRAINT "Constraint")*](glossary.md#GLOSSARY-CONSTRAINT) defined on a [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) which restricts the values allowed in one or more [*[attributes](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossary.md#GLOSSARY-ATTRIBUTE). The check constraint can make reference to any attribute of the same row in the relation, but cannot reference other rows of the same relation or other relations.

For more information, see [Section 5.5](ddl-constraints.md "5.5. Constraints").

Checkpoint: A point in the [*[WAL](glossary.md#GLOSSARY-WAL "Write-ahead log")*](glossary.md#GLOSSARY-WAL) sequence at which it is guaranteed that the heap and index data files have been updated with all information from [*[shared memory](glossary.md#GLOSSARY-SHARED-MEMORY "Shared memory")*](glossary.md#GLOSSARY-SHARED-MEMORY) modified before that checkpoint; a *checkpoint record* is written and flushed to WAL to mark that point.

A checkpoint is also the act of carrying out all the actions that are necessary to reach a checkpoint as defined above. This process is initiated when predefined conditions are met, such as a specified amount of time has passed, or a certain volume of records has been written; or it can be invoked by the user with the command `CHECKPOINT`.

For more information, see [Section 28.5](wal-configuration.md "28.5. WAL Configuration").

Checkpointer (process): An [*[auxiliary process](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) that is responsible for executing [*[checkpoints](glossary.md#GLOSSARY-CHECKPOINT "Checkpoint")*](glossary.md#GLOSSARY-CHECKPOINT).

Class (archaic): See [Relation](glossary.md#GLOSSARY-RELATION).

Client (process): Any process, possibly remote, that establishes a [*[session](glossary.md#GLOSSARY-SESSION "Session")*](glossary.md#GLOSSARY-SESSION) by [*[connecting](glossary.md#GLOSSARY-CONNECTION "Connection")*](glossary.md#GLOSSARY-CONNECTION) to an [*[instance](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossary.md#GLOSSARY-INSTANCE) to interact with a [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE).

Cluster owner: The operating system user that owns the [*[data directory](glossary.md#GLOSSARY-DATA-DIRECTORY "Data directory")*](glossary.md#GLOSSARY-DATA-DIRECTORY) and under which the `postgres` process is run. It is required that this user exist prior to creating a new [*[database cluster](glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*](glossary.md#GLOSSARY-DB-CLUSTER).

On operating systems with a `root` user, said user is not allowed to be the cluster owner.

Column: An [*[attribute](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossary.md#GLOSSARY-ATTRIBUTE) found in a [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) or [*[view](glossary.md#GLOSSARY-VIEW "View")*](glossary.md#GLOSSARY-VIEW).

Commit: The act of finalizing a [*[transaction](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossary.md#GLOSSARY-TRANSACTION) within the [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE), which makes it visible to other transactions and assures its [*[durability](glossary.md#GLOSSARY-DURABILITY "Durability")*](glossary.md#GLOSSARY-DURABILITY).

For more information, see [COMMIT](sql-commit.md "COMMIT").

Concurrency: The concept that multiple independent operations happen within the [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) at the same time. In PostgreSQL, concurrency is controlled by the [*[multiversion concurrency control](glossary.md#GLOSSARY-MVCC "Multi-version concurrency control (MVCC)")*](glossary.md#GLOSSARY-MVCC) mechanism.

Connection: An established line of communication between a client process and a [*[backend](glossary.md#GLOSSARY-BACKEND "Backend (process)")*](glossary.md#GLOSSARY-BACKEND) process, usually over a network, supporting a [*[session](glossary.md#GLOSSARY-SESSION "Session")*](glossary.md#GLOSSARY-SESSION). This term is sometimes used as a synonym for session.

For more information, see [Section 19.3](runtime-config-connection.md "19.3. Connections and Authentication").

Consistency: The property that the data in the [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) is always in compliance with [*[integrity constraints](glossary.md#GLOSSARY-CONSTRAINT "Constraint")*](glossary.md#GLOSSARY-CONSTRAINT). Transactions may be allowed to violate some of the constraints transiently before it commits, but if such violations are not resolved by the time it commits, such a transaction is automatically [*[rolled back](glossary.md#GLOSSARY-ROLLBACK "Rollback")*](glossary.md#GLOSSARY-ROLLBACK). This is one of the ACID properties.

Constraint: A restriction on the values of data allowed within a [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE), or in attributes of a [*[domain](glossary.md#GLOSSARY-DOMAIN "Domain")*](glossary.md#GLOSSARY-DOMAIN).

For more information, see [Section 5.5](ddl-constraints.md "5.5. Constraints").

Cumulative Statistics System: A system which, if enabled, accumulates statistical information about the [*[instance](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossary.md#GLOSSARY-INSTANCE)'s activities.

For more information, see [Section 27.2](monitoring-stats.md "27.2. The Cumulative Statistics System").

Data area: See [Data directory](glossary.md#GLOSSARY-DATA-DIRECTORY).

Database: A named collection of [*[local SQL objects](glossary.md#GLOSSARY-SQL-OBJECT "SQL object")*](glossary.md#GLOSSARY-SQL-OBJECT).

For more information, see [Section 22.1](manage-ag-overview.md "22.1. Overview").

Database cluster: A collection of databases and global SQL objects, and their common static and dynamic metadata. Sometimes referred to as a *cluster*. A database cluster is created using the [initdb](app-initdb.md "initdb") program.

In PostgreSQL, the term *cluster* is also sometimes used to refer to an instance. (Don't confuse this term with the SQL command `CLUSTER`.)

See also [*[cluster owner](glossary.md#GLOSSARY-CLUSTER-OWNER "Cluster owner")*](glossary.md#GLOSSARY-CLUSTER-OWNER), the operating-system owner of a cluster, and [*[bootstrap superuser](glossary.md#GLOSSARY-BOOTSTRAP-SUPERUSER "Bootstrap superuser")*](glossary.md#GLOSSARY-BOOTSTRAP-SUPERUSER), the PostgreSQL owner of a cluster.

Database server: See [Instance](glossary.md#GLOSSARY-INSTANCE).

Database superuser: A role having *superuser status* (see [Section 21.2](role-attributes.md "21.2. Role Attributes")).

Frequently referred to as *superuser*.

Data directory: The base directory on the file system of a [*[server](glossary.md#GLOSSARY-SERVER "Server")*](glossary.md#GLOSSARY-SERVER) that contains all data files and subdirectories associated with a [*[database cluster](glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*](glossary.md#GLOSSARY-DB-CLUSTER) (with the exception of [*[tablespaces](glossary.md#GLOSSARY-TABLESPACE "Tablespace")*](glossary.md#GLOSSARY-TABLESPACE), and optionally [*[WAL](glossary.md#GLOSSARY-WAL "Write-ahead log")*](glossary.md#GLOSSARY-WAL)). The environment variable `PGDATA` is commonly used to refer to the data directory.

A [*[cluster](glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*](glossary.md#GLOSSARY-DB-CLUSTER)'s storage space comprises the data directory plus any additional tablespaces.

For more information, see [Section 66.1](storage-file-layout.md "66.1. Database File Layout").

Data page: The basic structure used to store relation data. All pages are of the same size. Data pages are typically stored on disk, each in a specific file, and can be read to [*[shared buffers](glossary.md#GLOSSARY-SHARED-MEMORY "Shared memory")*](glossary.md#GLOSSARY-SHARED-MEMORY) where they can be modified, becoming *dirty*. They become clean when written to disk. New pages, which initially exist in memory only, are also dirty until written.

Datum: The internal representation of one value of an SQL data type.

Delete: An SQL command which removes [*[rows](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) from a given [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) or [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION).

For more information, see [DELETE](sql-delete.md "DELETE").

Domain: A user-defined data type that is based on another underlying data type. It acts the same as the underlying type except for possibly restricting the set of allowed values.

For more information, see [Section 8.18](domains.md "8.18. Domain Types").

Durability: The assurance that once a [*[transaction](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossary.md#GLOSSARY-TRANSACTION) has been [*[committed](glossary.md#GLOSSARY-COMMIT "Commit")*](glossary.md#GLOSSARY-COMMIT), the changes remain even after a system failure or crash. This is one of the ACID properties.

Epoch: See [Transaction ID](glossary.md#GLOSSARY-XID).

Extension: A software add-on package that can be installed on an [*[instance](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossary.md#GLOSSARY-INSTANCE) to get extra features.

For more information, see [Section 36.17](extend-extensions.md "36.17. Packaging Related Objects into an Extension").

File segment: A physical file which stores data for a given [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION). File segments are limited in size by a configuration value (typically 1 gigabyte), so if a relation exceeds that size, it is split into multiple segments.

For more information, see [Section 66.1](storage-file-layout.md "66.1. Database File Layout").

(Don't confuse this term with the similar term [*[WAL segment](glossary.md#GLOSSARY-WAL-FILE "WAL file")*](glossary.md#GLOSSARY-WAL-FILE)).

Foreign data wrapper: A means of representing data that is not contained in the local [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) so that it appears as if were in local [*[table(s)](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE). With a foreign data wrapper it is possible to define a [*[foreign server](glossary.md#GLOSSARY-FOREIGN-SERVER "Foreign server")*](glossary.md#GLOSSARY-FOREIGN-SERVER) and [*[foreign tables](glossary.md#GLOSSARY-FOREIGN-TABLE "Foreign table (relation)")*](glossary.md#GLOSSARY-FOREIGN-TABLE).

For more information, see [CREATE FOREIGN DATA WRAPPER](sql-createforeigndatawrapper.md "CREATE FOREIGN DATA WRAPPER").

Foreign key: A type of [*[constraint](glossary.md#GLOSSARY-CONSTRAINT "Constraint")*](glossary.md#GLOSSARY-CONSTRAINT) defined on one or more [*[columns](glossary.md#GLOSSARY-COLUMN "Column")*](glossary.md#GLOSSARY-COLUMN) in a [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) which requires the value(s) in those [*[columns](glossary.md#GLOSSARY-COLUMN "Column")*](glossary.md#GLOSSARY-COLUMN) to identify zero or one [*[row](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) in another (or, infrequently, the same) [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE).

Foreign server: A named collection of [*[foreign tables](glossary.md#GLOSSARY-FOREIGN-TABLE "Foreign table (relation)")*](glossary.md#GLOSSARY-FOREIGN-TABLE) which all use the same [*[foreign data wrapper](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER "Foreign data wrapper")*](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER) and have other configuration values in common.

For more information, see [CREATE SERVER](sql-createserver.md "CREATE SERVER").

Foreign table (relation): A [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) which appears to have [*[rows](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) and [*[columns](glossary.md#GLOSSARY-COLUMN "Column")*](glossary.md#GLOSSARY-COLUMN) similar to a regular [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE), but will forward requests for data through its [*[foreign data wrapper](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER "Foreign data wrapper")*](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER), which will return [*[result sets](glossary.md#GLOSSARY-RESULT-SET "Result set")*](glossary.md#GLOSSARY-RESULT-SET) structured according to the definition of the [*[foreign table](glossary.md#GLOSSARY-FOREIGN-TABLE "Foreign table (relation)")*](glossary.md#GLOSSARY-FOREIGN-TABLE).

For more information, see [CREATE FOREIGN TABLE](sql-createforeigntable.md "CREATE FOREIGN TABLE").

Fork: Each of the separate segmented file sets in which a relation is stored. The *main fork* is where the actual data resides. There also exist two secondary forks for metadata: the [*[free space map](glossary.md#GLOSSARY-FSM "Free space map (fork)")*](glossary.md#GLOSSARY-FSM) and the [*[visibility map](glossary.md#GLOSSARY-VM "Visibility map (fork)")*](glossary.md#GLOSSARY-VM). [*[Unlogged relations](glossary.md#GLOSSARY-UNLOGGED "Unlogged")*](glossary.md#GLOSSARY-UNLOGGED) also have an *init fork*.

Free space map (fork): A storage structure that keeps metadata about each data page of a table's main fork. The free space map entry for each page stores the amount of free space that's available for future tuples, and is structured to be efficiently searched for available space for a new tuple of a given size.

For more information, see [Section 66.3](storage-fsm.md "66.3. Free Space Map").

Function (routine): A type of routine that receives zero or more arguments, returns zero or more output values, and is constrained to run within one transaction. Functions are invoked as part of a query, for example via `SELECT`. Certain functions can return [*[sets](glossary.md#GLOSSARY-RESULT-SET "Result set")*](glossary.md#GLOSSARY-RESULT-SET); those are called *set-returning functions*.

Functions can also be used for [*[triggers](glossary.md#GLOSSARY-TRIGGER "Trigger")*](glossary.md#GLOSSARY-TRIGGER) to invoke.

For more information, see [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION").

GMT: See [UTC](glossary.md#GLOSSARY-UTC).

Grant: An SQL command that is used to allow a [*[user](glossary.md#GLOSSARY-USER "User")*](glossary.md#GLOSSARY-USER) or [*[role](glossary.md#GLOSSARY-ROLE "Role")*](glossary.md#GLOSSARY-ROLE) to access specific objects within the [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE).

For more information, see [GRANT](sql-grant.md "GRANT").

Heap: Contains the values of [*[row](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) attributes (i.e., the data) for a [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION). The heap is realized within one or more [*[file segments](glossary.md#GLOSSARY-FILE-SEGMENT "File segment")*](glossary.md#GLOSSARY-FILE-SEGMENT) in the relation's [*[main fork](glossary.md#GLOSSARY-FORK "Fork")*](glossary.md#GLOSSARY-FORK).

Host: A computer that communicates with other computers over a network. This is sometimes used as a synonym for [*[server](glossary.md#GLOSSARY-SERVER "Server")*](glossary.md#GLOSSARY-SERVER). It is also used to refer to a computer where [*[client processes](glossary.md#GLOSSARY-CLIENT "Client (process)")*](glossary.md#GLOSSARY-CLIENT) run.

Index (relation): A [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) that contains data derived from a [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) or [*[materialized view](glossary.md#GLOSSARY-MATERIALIZED-VIEW "Materialized view (relation)")*](glossary.md#GLOSSARY-MATERIALIZED-VIEW). Its internal structure supports fast retrieval of and access to the original data.

For more information, see [CREATE INDEX](sql-createindex.md "CREATE INDEX").

Incremental backup: A special [*[base backup](glossary.md#GLOSSARY-BASEBACKUP "Base Backup")*](glossary.md#GLOSSARY-BASEBACKUP) that for some files may contain only those pages that were modified since a previous backup, as opposed to the full contents of every file. Like base backups, it is generated by the tool [pg_basebackup](app-pgbasebackup.md "pg_basebackup").

To restore incremental backups the tool [pg_combinebackup](app-pgcombinebackup.md "pg_combinebackup") is used, which combines incremental backups with a base backup. Afterwards, recovery can use [*[WAL](glossary.md#GLOSSARY-WAL "Write-ahead log")*](glossary.md#GLOSSARY-WAL) to bring the [*[database cluster](glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*](glossary.md#GLOSSARY-DB-CLUSTER) to a consistent state.

For more information, see [Section 25.3.3](continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP "25.3.3. Making an Incremental Backup").

Input/Output (I/O): Input/Output (I/O) describes the communication between a program and peripheral devices. In the context of database systems, I/O commonly, but not exclusively, refers to interaction with storage devices or the network.

See Also [Asynchronous I/O](glossary.md#GLOSSARY-AIO).

Insert: An SQL command used to add new data into a [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE).

For more information, see [INSERT](sql-insert.md "INSERT").

Instance: A group of [*[backend](glossary.md#GLOSSARY-BACKEND "Backend (process)")*](glossary.md#GLOSSARY-BACKEND) and [*[auxiliary processes](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) that communicate using a common shared memory area. One [*[postmaster process](glossary.md#GLOSSARY-POSTMASTER "Postmaster (process)")*](glossary.md#GLOSSARY-POSTMASTER) manages the instance; one instance manages exactly one [*[database cluster](glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*](glossary.md#GLOSSARY-DB-CLUSTER) with all its databases. Many instances can run on the same [*[server](glossary.md#GLOSSARY-SERVER "Server")*](glossary.md#GLOSSARY-SERVER) as long as their TCP ports do not conflict.

The instance handles all key features of a DBMS: read and write access to files and shared memory, assurance of the ACID properties, [*[connections](glossary.md#GLOSSARY-CONNECTION "Connection")*](glossary.md#GLOSSARY-CONNECTION) to [*[client processes](glossary.md#GLOSSARY-CLIENT "Client (process)")*](glossary.md#GLOSSARY-CLIENT), privilege verification, crash recovery, replication, etc.

Isolation: The property that the effects of a transaction are not visible to [*[concurrent transactions](glossary.md#GLOSSARY-CONCURRENCY "Concurrency")*](glossary.md#GLOSSARY-CONCURRENCY) before it commits. This is one of the ACID properties.

For more information, see [Section 13.2](transaction-iso.md "13.2. Transaction Isolation").

Join: An operation and SQL keyword used in [*[queries](glossary.md#GLOSSARY-QUERY "Query")*](glossary.md#GLOSSARY-QUERY) for combining data from multiple [*[relations](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION).

Key: A means of identifying a [*[row](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) within a [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) or other [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) by values contained within one or more [*[attributes](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossary.md#GLOSSARY-ATTRIBUTE) in that relation.

Lock: A mechanism that allows a process to limit or prevent simultaneous access to a resource.

Log file: Log files contain human-readable text lines about events. Examples include login failures, long-running queries, etc.

For more information, see [Section 24.3](logfile-maintenance.md "24.3. Log File Maintenance").

Logged: A [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) is considered [*[logged](glossary.md#GLOSSARY-LOGGED "Logged")*](glossary.md#GLOSSARY-LOGGED) if changes to it are sent to the [*[WAL](glossary.md#GLOSSARY-WAL "Write-ahead log")*](glossary.md#GLOSSARY-WAL). By default, all regular tables are logged. A table can be specified as [*[unlogged](glossary.md#GLOSSARY-UNLOGGED "Unlogged")*](glossary.md#GLOSSARY-UNLOGGED) either at creation time or via the `ALTER TABLE` command.

Logger (process): An [*[auxiliary process](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) which, if enabled, writes information about database events into the current [*[log file](glossary.md#GLOSSARY-LOG-FILE "Log file")*](glossary.md#GLOSSARY-LOG-FILE). When reaching certain time- or volume-dependent criteria, a new log file is created. Also called *syslogger*.

For more information, see [Section 19.8](runtime-config-logging.md "19.8. Error Reporting and Logging").

Logical replication cluster: A set of publisher and subscriber instances with the publisher instance replicating changes to the subscriber instance.

Log record: Archaic term for a [*[WAL record](glossary.md#GLOSSARY-WAL-RECORD "WAL record")*](glossary.md#GLOSSARY-WAL-RECORD).

Log sequence number (LSN): Byte offset into the [*[WAL](glossary.md#GLOSSARY-WAL "Write-ahead log")*](glossary.md#GLOSSARY-WAL), increasing monotonically with each new [*[WAL record](glossary.md#GLOSSARY-WAL-RECORD "WAL record")*](glossary.md#GLOSSARY-WAL-RECORD).

For more information, see [`pg_lsn`](datatype-pg-lsn.md "8.20. pg_lsn Type") and [Section 28.6](wal-internals.md "28.6. WAL Internals").

LSN: See [Log sequence number](glossary.md#GLOSSARY-LOG-SEQUENCE-NUMBER).

Master (server): See [Primary (server)](glossary.md#GLOSSARY-PRIMARY-SERVER).

Materialized: The property that some information has been pre-computed and stored for later use, rather than computing it on-the-fly.

This term is used in [*[materialized view](glossary.md#GLOSSARY-MATERIALIZED-VIEW "Materialized view (relation)")*](glossary.md#GLOSSARY-MATERIALIZED-VIEW), to mean that the data derived from the view's query is stored on disk separately from the sources of that data.

This term is also used to refer to some multi-step queries to mean that the data resulting from executing a given step is stored in memory (with the possibility of spilling to disk), so that it can be read multiple times by another step.

Materialized view (relation): A [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) that is defined by a `SELECT` statement (just like a [*[view](glossary.md#GLOSSARY-VIEW "View")*](glossary.md#GLOSSARY-VIEW)), but stores data in the same way that a [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) does. It cannot be modified via `INSERT`, `UPDATE`, `DELETE`, or `MERGE` operations.

For more information, see [CREATE MATERIALIZED VIEW](sql-creatematerializedview.md "CREATE MATERIALIZED VIEW").

Merge: An SQL command used to conditionally add, modify, or remove [*[rows](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) in a given [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE), using data from a source [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION).

For more information, see [MERGE](sql-merge.md "MERGE").

Multi-version concurrency control (MVCC): A mechanism designed to allow several [*[transactions](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossary.md#GLOSSARY-TRANSACTION) to be reading and writing the same rows without one process causing other processes to stall. In PostgreSQL, MVCC is implemented by creating copies (*versions*) of [*[tuples](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) as they are modified; after transactions that can see the old versions terminate, those old versions need to be removed.

Null: A concept of non-existence that is a central tenet of relational database theory. It represents the absence of a definite value.

Optimizer: See [Query planner](glossary.md#GLOSSARY-PLANNER).

Parallel query: The ability to handle parts of executing a [*[query](glossary.md#GLOSSARY-QUERY "Query")*](glossary.md#GLOSSARY-QUERY) to take advantage of parallel processes on servers with multiple CPUs.

Partition: One of several disjoint (not overlapping) subsets of a larger set.: In reference to a [*[partitioned table](glossary.md#GLOSSARY-PARTITIONED-TABLE "Partitioned table (relation)")*](glossary.md#GLOSSARY-PARTITIONED-TABLE): One of the tables that each contain part of the data of the partitioned table, which is said to be the *parent*. The partition is itself a table, so it can also be queried directly; at the same time, a partition can sometimes be a partitioned table, allowing hierarchies to be created.: In reference to a [*[window function](glossary.md#GLOSSARY-WINDOW-FUNCTION "Window function (routine)")*](glossary.md#GLOSSARY-WINDOW-FUNCTION) in a [*[query](glossary.md#GLOSSARY-QUERY "Query")*](glossary.md#GLOSSARY-QUERY), a partition is a user-defined criterion that identifies which neighboring [*[rows](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) of the [*[query's result set](glossary.md#GLOSSARY-RESULT-SET "Result set")*](glossary.md#GLOSSARY-RESULT-SET) can be considered by the function.

Partitioned table (relation): A [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) that is in semantic terms the same as a [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE), but whose storage is distributed across several [*[partitions](glossary.md#GLOSSARY-PARTITION "Partition")*](glossary.md#GLOSSARY-PARTITION).

Postmaster (process): The very first process of an [*[instance](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossary.md#GLOSSARY-INSTANCE). It starts and manages the [*[auxiliary processes](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) and creates [*[backend processes](glossary.md#GLOSSARY-BACKEND "Backend (process)")*](glossary.md#GLOSSARY-BACKEND) on demand.

For more information, see [Section 18.3](server-start.md "18.3. Starting the Database Server").

Primary key: A special case of a [*[unique constraint](glossary.md#GLOSSARY-UNIQUE-CONSTRAINT "Unique constraint")*](glossary.md#GLOSSARY-UNIQUE-CONSTRAINT) defined on a [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) or other [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) that also guarantees that all of the [*[attributes](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossary.md#GLOSSARY-ATTRIBUTE) within the [*[primary key](glossary.md#GLOSSARY-PRIMARY-KEY "Primary key")*](glossary.md#GLOSSARY-PRIMARY-KEY) do not have [*[null](glossary.md#GLOSSARY-NULL "Null")*](glossary.md#GLOSSARY-NULL) values. As the name implies, there can be only one primary key per table, though it is possible to have multiple unique constraints that also have no null-capable attributes.

Primary (server): When two or more [*[databases](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) are linked via [*[replication](glossary.md#GLOSSARY-REPLICATION "Replication")*](glossary.md#GLOSSARY-REPLICATION), the [*[server](glossary.md#GLOSSARY-SERVER "Server")*](glossary.md#GLOSSARY-SERVER) that is considered the authoritative source of information is called the *primary*, also known as a *master*.

Procedure (routine): A type of routine. Their distinctive qualities are that they do not return values, and that they are allowed to make transactional statements such as `COMMIT` and `ROLLBACK`. They are invoked via the `CALL` command.

For more information, see [CREATE PROCEDURE](sql-createprocedure.md "CREATE PROCEDURE").

Query: A request sent by a client to a [*[backend](glossary.md#GLOSSARY-BACKEND "Backend (process)")*](glossary.md#GLOSSARY-BACKEND), usually to return results or to modify data on the database.

Query planner: The part of PostgreSQL that is devoted to determining (*planning*) the most efficient way to execute [*[queries](glossary.md#GLOSSARY-QUERY "Query")*](glossary.md#GLOSSARY-QUERY). Also known as *query optimizer*, *optimizer*, or simply *planner*.

Record: See [Tuple](glossary.md#GLOSSARY-TUPLE).

Recycling: See [WAL file](glossary.md#GLOSSARY-WAL-FILE).

Referential integrity: A means of restricting data in one [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) by a [*[foreign key](glossary.md#GLOSSARY-FOREIGN-KEY "Foreign key")*](glossary.md#GLOSSARY-FOREIGN-KEY) so that it must have matching data in another [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION).

Relation: The generic term for all objects in a [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) that have a name and a list of [*[attributes](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossary.md#GLOSSARY-ATTRIBUTE) defined in a specific order. [*[Tables](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE), [*[sequences](glossary.md#GLOSSARY-SEQUENCE "Sequence (relation)")*](glossary.md#GLOSSARY-SEQUENCE), [*[views](glossary.md#GLOSSARY-VIEW "View")*](glossary.md#GLOSSARY-VIEW), [*[foreign tables](glossary.md#GLOSSARY-FOREIGN-TABLE "Foreign table (relation)")*](glossary.md#GLOSSARY-FOREIGN-TABLE), [*[materialized views](glossary.md#GLOSSARY-MATERIALIZED-VIEW "Materialized view (relation)")*](glossary.md#GLOSSARY-MATERIALIZED-VIEW), composite types, and [*[indexes](glossary.md#GLOSSARY-INDEX "Index (relation)")*](glossary.md#GLOSSARY-INDEX) are all relations.

More generically, a relation is a set of tuples; for example, the result of a query is also a relation.

In PostgreSQL, *Class* is an archaic synonym for *relation*.

Replica (server): A [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) that is paired with a [*[primary](glossary.md#GLOSSARY-PRIMARY-SERVER "Primary (server)")*](glossary.md#GLOSSARY-PRIMARY-SERVER) database and is maintaining a copy of some or all of the primary database's data. The foremost reasons for doing this are to allow for greater access to that data, and to maintain availability of the data in the event that the [*[primary](glossary.md#GLOSSARY-PRIMARY-SERVER "Primary (server)")*](glossary.md#GLOSSARY-PRIMARY-SERVER) becomes unavailable.

Replication: The act of reproducing data on one [*[server](glossary.md#GLOSSARY-SERVER "Server")*](glossary.md#GLOSSARY-SERVER) onto another server called a [*[replica](glossary.md#GLOSSARY-REPLICA "Replica (server)")*](glossary.md#GLOSSARY-REPLICA). This can take the form of *physical replication*, where all file changes from one server are copied verbatim, or *logical replication* where a defined subset of data changes are conveyed using a higher-level representation.

Restartpoint: A variant of a [*[checkpoint](glossary.md#GLOSSARY-CHECKPOINT "Checkpoint")*](glossary.md#GLOSSARY-CHECKPOINT) performed on a [*[replica](glossary.md#GLOSSARY-REPLICA "Replica (server)")*](glossary.md#GLOSSARY-REPLICA).

For more information, see [Section 28.5](wal-configuration.md "28.5. WAL Configuration").

Result set: A [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) transmitted from a [*[backend process](glossary.md#GLOSSARY-BACKEND "Backend (process)")*](glossary.md#GLOSSARY-BACKEND) to a [*[client](glossary.md#GLOSSARY-CLIENT "Client (process)")*](glossary.md#GLOSSARY-CLIENT) upon the completion of an SQL command, usually a `SELECT` but it can be an `INSERT`, `UPDATE`, `DELETE`, or `MERGE` command if the `RETURNING` clause is specified.

The fact that a result set is a relation means that a query can be used in the definition of another query, becoming a *subquery*.


Revoke: A command to prevent access to a named set of [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) objects for a named list of [*[roles](glossary.md#GLOSSARY-ROLE "Role")*](glossary.md#GLOSSARY-ROLE).

For more information, see [REVOKE](sql-revoke.md "REVOKE").

Role: A collection of access privileges to the [*[instance](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE). Roles are themselves a privilege that can be granted to other roles. This is often done for convenience or to ensure completeness when multiple [*[users](glossary.md#GLOSSARY-USER "User")*](glossary.md#GLOSSARY-USER) need the same privileges.

For more information, see [CREATE ROLE](sql-createrole.md "CREATE ROLE").

Rollback: A command to undo all of the operations performed since the beginning of a [*[transaction](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossary.md#GLOSSARY-TRANSACTION).

For more information, see [ROLLBACK](sql-rollback.md "ROLLBACK").

Routine: A defined set of instructions stored in the database system that can be invoked for execution. A routine can be written in a variety of programming languages. Routines can be [*[functions](glossary.md#GLOSSARY-FUNCTION "Function (routine)")*](glossary.md#GLOSSARY-FUNCTION) (including set-returning functions and [*[trigger functions](glossary.md#GLOSSARY-TRIGGER "Trigger")*](glossary.md#GLOSSARY-TRIGGER)), [*[aggregate functions](glossary.md#GLOSSARY-AGGREGATE "Aggregate function (routine)")*](glossary.md#GLOSSARY-AGGREGATE), and [*[procedures](glossary.md#GLOSSARY-PROCEDURE "Procedure (routine)")*](glossary.md#GLOSSARY-PROCEDURE).

Many routines are already defined within PostgreSQL itself, but user-defined ones can also be added.

Row: See [Tuple](glossary.md#GLOSSARY-TUPLE).

Savepoint: A special mark in the sequence of steps in a [*[transaction](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossary.md#GLOSSARY-TRANSACTION). Data modifications after this point in time may be reverted to the time of the savepoint.

For more information, see [SAVEPOINT](sql-savepoint.md "SAVEPOINT").

Schema: A schema is a namespace for [*[SQL objects](glossary.md#GLOSSARY-SQL-OBJECT "SQL object")*](glossary.md#GLOSSARY-SQL-OBJECT), which all reside in the same [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE). Each SQL object must reside in exactly one schema.

All system-defined SQL objects reside in schema `pg_catalog`.: More generically, the term *schema* is used to mean all data descriptions ([*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) definitions, [*[constraints](glossary.md#GLOSSARY-CONSTRAINT "Constraint")*](glossary.md#GLOSSARY-CONSTRAINT), comments, etc.) for a given [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) or subset thereof.

For more information, see [Section 5.10](ddl-schemas.md "5.10. Schemas").

Segment: See [File segment](glossary.md#GLOSSARY-FILE-SEGMENT).

Select: The SQL command used to request data from a [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE). Normally, `SELECT` commands are not expected to modify the [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) in any way, but it is possible that [*[functions](glossary.md#GLOSSARY-FUNCTION "Function (routine)")*](glossary.md#GLOSSARY-FUNCTION) invoked within the query could have side effects that do modify data.

For more information, see [SELECT](sql-select.md "SELECT").

Sequence (relation): A type of relation that is used to generate values. Typically the generated values are sequential non-repeating numbers. They are commonly used to generate surrogate [*[primary key](glossary.md#GLOSSARY-PRIMARY-KEY "Primary key")*](glossary.md#GLOSSARY-PRIMARY-KEY) values.

Server: A computer on which PostgreSQL [*[instances](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossary.md#GLOSSARY-INSTANCE) run. The term *server* denotes real hardware, a container, or a *virtual machine*.

This term is sometimes used to refer to an instance or to a host.

Session: A state that allows a client and a backend to interact, communicating over a [*[connection](glossary.md#GLOSSARY-CONNECTION "Connection")*](glossary.md#GLOSSARY-CONNECTION).

Shared memory: RAM which is used by the processes common to an [*[instance](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossary.md#GLOSSARY-INSTANCE). It mirrors parts of [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) files, provides a transient area for [*[WAL records](glossary.md#GLOSSARY-WAL-RECORD "WAL record")*](glossary.md#GLOSSARY-WAL-RECORD), and stores additional common information. Note that shared memory belongs to the complete instance, not to a single database.

The largest part of shared memory is known as *shared buffers* and is used to mirror part of data files, organized into pages. When a page is modified, it is called a dirty page until it is written back to the file system.

For more information, see [Section 19.4.1](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-MEMORY "19.4.1. Memory").

SQL object: Any object that can be created with a `CREATE` command. Most objects are specific to one database, and are commonly known as *local objects*.

Most local objects reside in a specific [*[schema](glossary.md#GLOSSARY-SCHEMA "Schema")*](glossary.md#GLOSSARY-SCHEMA) in their containing database, such as [*[relations](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) (all types), [*[routines](glossary.md#GLOSSARY-FUNCTION "Function (routine)")*](glossary.md#GLOSSARY-FUNCTION) (all types), data types, etc. The names of such objects of the same type in the same schema are enforced to be unique.

There also exist local objects that do not reside in schemas; some examples are [*[extensions](glossary.md#GLOSSARY-EXTENSION "Extension")*](glossary.md#GLOSSARY-EXTENSION), [*[data type casts](glossary.md#GLOSSARY-CAST "Cast")*](glossary.md#GLOSSARY-CAST), and [*[foreign data wrappers](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER "Foreign data wrapper")*](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER). The names of such objects of the same type are enforced to be unique within the database.

Other object types, such as [*[roles](glossary.md#GLOSSARY-ROLE "Role")*](glossary.md#GLOSSARY-ROLE), [*[tablespaces](glossary.md#GLOSSARY-TABLESPACE "Tablespace")*](glossary.md#GLOSSARY-TABLESPACE), replication origins, subscriptions for logical replication, and databases themselves are not local SQL objects since they exist entirely outside of any specific database; they are called *global objects*. The names of such objects are enforced to be unique within the whole database cluster.

For more information, see [Section 22.1](manage-ag-overview.md "22.1. Overview").

SQL standard: A series of documents that define the SQL language.

Standby (server): See [Replica (server)](glossary.md#GLOSSARY-REPLICA).

Startup process: An [*[auxiliary process](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) that replays WAL during crash recovery and in a [*[physical replica](glossary.md#GLOSSARY-REPLICATION "Replication")*](glossary.md#GLOSSARY-REPLICATION).

(The name is historical: the startup process was named before replication was implemented; the name refers to its task as it relates to the server startup following a crash.)

Superuser: As used in this documentation, it is a synonym for [*[database superuser](glossary.md#GLOSSARY-DATABASE-SUPERUSER "Database superuser")*](glossary.md#GLOSSARY-DATABASE-SUPERUSER).

System catalog: A collection of [*[tables](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) which describe the structure of all [*[SQL objects](glossary.md#GLOSSARY-SQL-OBJECT "SQL object")*](glossary.md#GLOSSARY-SQL-OBJECT) of the instance. The system catalog resides in the schema `pg_catalog`. These tables contain data in internal representation and are not typically considered useful for user examination; a number of user-friendlier [*[views](glossary.md#GLOSSARY-VIEW "View")*](glossary.md#GLOSSARY-VIEW), also in schema `pg_catalog`, offer more convenient access to some of that information, while additional tables and views exist in schema `information_schema` (see [Chapter 35](information-schema.md "Chapter 35. The Information Schema")) that expose some of the same and additional information as mandated by the [*[SQL standard](glossary.md#GLOSSARY-SQL-STANDARD "SQL standard")*](glossary.md#GLOSSARY-SQL-STANDARD).

For more information, see [Section 5.10](ddl-schemas.md "5.10. Schemas").

Table: A collection of [*[tuples](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) having a common data structure (the same number of [*[attributes](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossary.md#GLOSSARY-ATTRIBUTE), in the same order, having the same name and type per position). A table is the most common form of [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) in PostgreSQL.

For more information, see [CREATE TABLE](sql-createtable.md "CREATE TABLE").

Tablespace: A named location on the server file system. All [*[SQL objects](glossary.md#GLOSSARY-SQL-OBJECT "SQL object")*](glossary.md#GLOSSARY-SQL-OBJECT) which require storage beyond their definition in the [*[system catalog](glossary.md#GLOSSARY-SYSTEM-CATALOG "System catalog")*](glossary.md#GLOSSARY-SYSTEM-CATALOG) must belong to a single tablespace. Initially, a database cluster contains a single usable tablespace which is used as the default for all SQL objects, called `pg_default`.

For more information, see [Section 22.6](manage-ag-tablespaces.md "22.6. Tablespaces").

Temporary table: [*[Tables](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) that exist either for the lifetime of a [*[session](glossary.md#GLOSSARY-SESSION "Session")*](glossary.md#GLOSSARY-SESSION) or a [*[transaction](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossary.md#GLOSSARY-TRANSACTION), as specified at the time of creation. The data in them is not visible to other sessions, and is not [*[logged](glossary.md#GLOSSARY-LOGGED "Logged")*](glossary.md#GLOSSARY-LOGGED). Temporary tables are often used to store intermediate data for a multi-step operation.

For more information, see [CREATE TABLE](sql-createtable.md "CREATE TABLE").

TOAST: A mechanism by which large attributes of table rows are split and stored in a secondary table, called the *TOAST table*. Each relation with large attributes has its own TOAST table.

For more information, see [Section 66.2](storage-toast.md "66.2. TOAST").

Transaction: A combination of commands that must act as a single [*[atomic](glossary.md#GLOSSARY-ATOMIC "Atomic")*](glossary.md#GLOSSARY-ATOMIC) command: they all succeed or all fail as a single unit, and their effects are not visible to other [*[sessions](glossary.md#GLOSSARY-SESSION "Session")*](glossary.md#GLOSSARY-SESSION) until the transaction is complete, and possibly even later, depending on the isolation level.

For more information, see [Section 13.2](transaction-iso.md "13.2. Transaction Isolation").

Transaction ID: The numerical, unique, sequentially-assigned identifier that each transaction receives when it first causes a database modification. Frequently abbreviated as *xid*. When stored on disk, xids are only 32-bits wide, so only approximately four billion write transaction IDs can be generated; to permit the system to run for longer than that, *epochs* are used, also 32 bits wide. When the counter reaches the maximum xid value, it starts over at `3` (values under that are reserved) and the epoch value is incremented by one. In some contexts, the epoch and xid values are considered together as a single 64-bit value; see [Section 67.1](transaction-id.md "67.1. Transactions and Identifiers") for more details.

For more information, see [Section 8.19](datatype-oid.md "8.19. Object Identifier Types").

Transactions per second (TPS): Average number of transactions that are executed per second, totaled across all sessions active for a measured run. This is used as a measure of the performance characteristics of an instance.

Trigger: A [*[function](glossary.md#GLOSSARY-FUNCTION "Function (routine)")*](glossary.md#GLOSSARY-FUNCTION) which can be defined to execute whenever a certain operation (`INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`) is applied to a [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION). A trigger executes within the same [*[transaction](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossary.md#GLOSSARY-TRANSACTION) as the statement which invoked it, and if the function fails, then the invoking statement also fails.

For more information, see [CREATE TRIGGER](sql-createtrigger.md "CREATE TRIGGER").

Tuple: A collection of [*[attributes](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossary.md#GLOSSARY-ATTRIBUTE) in a fixed order. That order may be defined by the [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) (or other [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION)) where the tuple is contained, in which case the tuple is often called a *row*. It may also be defined by the structure of a result set, in which case it is sometimes called a *record*.

Unique constraint: A type of [*[constraint](glossary.md#GLOSSARY-CONSTRAINT "Constraint")*](glossary.md#GLOSSARY-CONSTRAINT) defined on a [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) which restricts the values allowed in one or a combination of columns so that each value or combination of values can only appear once in the relation — that is, no other row in the relation contains values that are equal to those.

Because [*[null values](glossary.md#GLOSSARY-NULL "Null")*](glossary.md#GLOSSARY-NULL) are not considered equal to each other, multiple rows with null values are allowed to exist without violating the unique constraint.

Unlogged: The property of certain [*[relations](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) that the changes to them are not reflected in the [*[WAL](glossary.md#GLOSSARY-WAL "Write-ahead log")*](glossary.md#GLOSSARY-WAL). This disables replication and crash recovery for these relations.

The primary use of unlogged tables is for storing transient work data that must be shared across processes.

[*[Temporary tables](glossary.md#GLOSSARY-TEMPORARY-TABLE "Temporary table")*](glossary.md#GLOSSARY-TEMPORARY-TABLE) are always unlogged.

Update: An SQL command used to modify [*[rows](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) that may already exist in a specified [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE). It cannot create or remove rows.

For more information, see [UPDATE](sql-update.md "UPDATE").

User: A [*[role](glossary.md#GLOSSARY-ROLE "Role")*](glossary.md#GLOSSARY-ROLE) that has the *login privilege* (see [Section 21.2](role-attributes.md "21.2. Role Attributes")).

User mapping: The translation of login credentials in the local [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) to credentials in a remote data system defined by a [*[foreign data wrapper](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER "Foreign data wrapper")*](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER).

For more information, see [CREATE USER MAPPING](sql-createusermapping.md "CREATE USER MAPPING").

UTC: Universal Coordinated Time, the primary global time reference, approximately the time prevailing at the zero meridian of longitude. Often but inaccurately referred to as GMT (Greenwich Mean Time).

Vacuum: The process of removing outdated [*[tuple versions](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) from tables or materialized views, and other closely related processing required by PostgreSQL's implementation of [*[MVCC](glossary.md#GLOSSARY-MVCC "Multi-version concurrency control (MVCC)")*](glossary.md#GLOSSARY-MVCC). This can be initiated through the use of the `VACUUM` command, but can also be handled automatically via [*[autovacuum](glossary.md#GLOSSARY-AUTOVACUUM "Autovacuum (process)")*](glossary.md#GLOSSARY-AUTOVACUUM) processes.

For more information, see [Section 24.1](routine-vacuuming.md "24.1. Routine Vacuuming") .

View: A [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) that is defined by a `SELECT` statement, but has no storage of its own. Any time a query references a view, the definition of the view is substituted into the query as if the user had typed it as a subquery instead of the name of the view.

For more information, see [CREATE VIEW](sql-createview.md "CREATE VIEW").

Visibility map (fork): A storage structure that keeps metadata about each data page of a table's main fork. The visibility map entry for each page stores two bits: the first one (`all-visible`) indicates that all tuples in the page are visible to all transactions. The second one (`all-frozen`) indicates that all tuples in the page are marked frozen.

WAL: See [Write-ahead log](glossary.md#GLOSSARY-WAL).

WAL archiver (process): An [*[auxiliary process](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) which, if enabled, saves copies of [*[WAL files](glossary.md#GLOSSARY-WAL-FILE "WAL file")*](glossary.md#GLOSSARY-WAL-FILE) for the purpose of creating backups or keeping [*[replicas](glossary.md#GLOSSARY-REPLICA "Replica (server)")*](glossary.md#GLOSSARY-REPLICA) current.

For more information, see [Section 25.3](continuous-archiving.md "25.3. Continuous Archiving and Point-in-Time Recovery (PITR)").

WAL file: Also known as *WAL segment* or *WAL segment file*. Each of the sequentially-numbered files that provide storage space for [*[WAL](glossary.md#GLOSSARY-WAL "Write-ahead log")*](glossary.md#GLOSSARY-WAL). The files are all of the same predefined size and are written in sequential order, interspersing changes as they occur in multiple simultaneous sessions. If the system crashes, the files are read in order, and each of the changes is replayed to restore the system to the state it was in before the crash.

Each WAL file can be released after a [*[checkpoint](glossary.md#GLOSSARY-CHECKPOINT "Checkpoint")*](glossary.md#GLOSSARY-CHECKPOINT) writes all the changes in it to the corresponding data files. Releasing the file can be done either by deleting it, or by changing its name so that it will be used in the future, which is called *recycling*.

For more information, see [Section 28.6](wal-internals.md "28.6. WAL Internals").

WAL record: A low-level description of an individual data change. It contains sufficient information for the data change to be re-executed (*replayed*) in case a system failure causes the change to be lost. WAL records use a non-printable binary format.

For more information, see [Section 28.6](wal-internals.md "28.6. WAL Internals").

WAL receiver (process): An [*[auxiliary process](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) that runs on a [*[replica](glossary.md#GLOSSARY-REPLICA "Replica (server)")*](glossary.md#GLOSSARY-REPLICA) to receive WAL from the [*[primary server](glossary.md#GLOSSARY-PRIMARY-SERVER "Primary (server)")*](glossary.md#GLOSSARY-PRIMARY-SERVER) for replay by the [*[startup process](glossary.md#GLOSSARY-STARTUP-PROCESS "Startup process")*](glossary.md#GLOSSARY-STARTUP-PROCESS).

For more information, see [Section 26.2](warm-standby.md "26.2. Log-Shipping Standby Servers").

WAL segment: See [WAL file](glossary.md#GLOSSARY-WAL-FILE).

WAL sender (process): A special [*[backend process](glossary.md#GLOSSARY-BACKEND "Backend (process)")*](glossary.md#GLOSSARY-BACKEND) that streams WAL over a network. The receiving end can be a [*[WAL receiver](glossary.md#GLOSSARY-WAL-RECEIVER "WAL receiver (process)")*](glossary.md#GLOSSARY-WAL-RECEIVER) in a [*[replica](glossary.md#GLOSSARY-REPLICA "Replica (server)")*](glossary.md#GLOSSARY-REPLICA), [pg_receivewal](app-pgreceivewal.md "pg_receivewal"), or any other client program that speaks the replication protocol.

WAL summarizer (process): An [*[auxiliary process](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) that summarizes WAL data for [*[incremental backups](glossary.md#GLOSSARY-INCREMENTAL-BACKUP "Incremental backup")*](glossary.md#GLOSSARY-INCREMENTAL-BACKUP).

For more information, see [Section 19.5.7](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SUMMARIZATION "19.5.7. WAL Summarization").

WAL writer (process): An [*[auxiliary process](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) that writes [*[WAL records](glossary.md#GLOSSARY-WAL-RECORD "WAL record")*](glossary.md#GLOSSARY-WAL-RECORD) from [*[shared memory](glossary.md#GLOSSARY-SHARED-MEMORY "Shared memory")*](glossary.md#GLOSSARY-SHARED-MEMORY) to [*[WAL files](glossary.md#GLOSSARY-WAL-FILE "WAL file")*](glossary.md#GLOSSARY-WAL-FILE).

For more information, see [Section 19.5](runtime-config-wal.md "19.5. Write Ahead Log").

Window function (routine): A type of [*[function](glossary.md#GLOSSARY-FUNCTION "Function (routine)")*](glossary.md#GLOSSARY-FUNCTION) used in a [*[query](glossary.md#GLOSSARY-QUERY "Query")*](glossary.md#GLOSSARY-QUERY) that applies to a [*[partition](glossary.md#GLOSSARY-PARTITION "Partition")*](glossary.md#GLOSSARY-PARTITION) of the query's [*[result set](glossary.md#GLOSSARY-RESULT-SET "Result set")*](glossary.md#GLOSSARY-RESULT-SET); the function's result is based on values found in [*[rows](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) of the same partition or frame.

All [*[aggregate functions](glossary.md#GLOSSARY-AGGREGATE "Aggregate function (routine)")*](glossary.md#GLOSSARY-AGGREGATE) can be used as window functions, but window functions can also be used to, for example, give ranks to each of the rows in the partition. Also known as *analytic functions*.

For more information, see [Section 3.5](tutorial-window.md "3.5. Window Functions").

Write-ahead log: The journal that keeps track of the changes in the [*[database cluster](glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*](glossary.md#GLOSSARY-DB-CLUSTER) as user- and system-invoked operations take place. It comprises many individual [*[WAL records](glossary.md#GLOSSARY-WAL-RECORD "WAL record")*](glossary.md#GLOSSARY-WAL-RECORD) written sequentially to [*[WAL files](glossary.md#GLOSSARY-WAL-FILE "WAL file")*](glossary.md#GLOSSARY-WAL-FILE).
