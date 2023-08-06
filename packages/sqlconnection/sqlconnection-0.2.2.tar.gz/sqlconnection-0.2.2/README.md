SQL Adapter for Connection and Query Handling


## System Dependency

* Python 3.6.8
* pipenv


## Development Setup

1) Clone the repo 
2) cd sqlconnection
3) pipenv install
4) pipenv shell

Start developing

# Package sqlconnection
python version must be 3.6.8
### Build
python setup.py build

### Distribute
python setup.py sdist

### Dependency
* psycopg2-binary>=2.8.4

### Use 
It wil load environment variable automatically, so all you need to do is make sure these environment variables are present. 
It will also autoload .env ( example .env.dist , rename it to .env) file before running, so you can also put these variables in your .env file. 

Needed Environment variables are 

```
# Sql
SQL_TYPE=postgres
SQL_USER=user_name
SQL_PASSWORD=user_password
SQL_HOST=localhost
SQL_PORT=5432
SQL_DATABASE=database_name

```

```
from sqlconnection import postgresql
from sqlconection import postgresql_queries

psql = postgresql.Postgres()

postgresql_queries.execute_query(psql.connection, query)

When all done , please do psql.close_connection()

```




