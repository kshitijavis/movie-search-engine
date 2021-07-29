# movie-search-engine

## Installation
### Setup MySQL Database
The following steps will create a MySQL user and database where movie data will be stored. This guide will 

1) Login to your MySQL server interactive prompt and crete a new database
    ```
    CREATE DATABASE <database name>;
    ```
2) Create a new user that Django can use to access your new database
    ```
    CREATE USER <username>@'%' IDENTIFIED BY <password>;
    ```
3) Grant privileges for the new user to the new database
    ```
    GRANT ALL ON <database name>.* to <username>@'%';
    ```
4) Flush privileges
    ```
    FLUSH PRIVILEGES;
    ```
### Set Environment Variables
To connect Django to a MySQL database, you will need to add detabase information to a `.env` file
Create a `.env` in `backend/backend` and populate it like so
```
DATABASE_NAME=<database name>
DATABASE_USER=<database username>
DATABASE_PASSWORD=<database password>
DATABASE_HOST=<database host>
DATABASE_PORT=<port that database is running on>
```
## Testing
Running the project test suite requires a test database. Create the database by running the following MySQL commands.
```
GRANT ALL ON test_<database name>.* to <username>@'%';
FLUSH PRIVILEGES;
```
Where <database name> is the name of the database created while installing this app. Note that the test database name prepends `test_` to the application database.
## Notes
The following error sometimes occurres on MacOS systems when connecting to MySQL
```
ImportError: dlopen(.../.venv/lib/python3.8/site-packages/MySQLdb/_mysql.cpython-38-darwin.so, 2): Library not loaded: @rpath/libmysqlclient.21.dylib
...
Reason: image not found
```

If this error occurs, add the following to your bash/zsh configuration file
```
export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/
```