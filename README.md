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
## Optional: Add Image Search
The `/movies/<id>` endpoint on the React App lists details about a movie. The app also uses Google Custom Search Engine (GCSE) to find and display a cover image of the movie. To set up image-rendering, follow these steps.
1) Visit [GCSE API](https://developers.google.com/custom-search/v1/overview). Scroll down and click the blue **Get a Key** button. This will prompt you to sign in using Google credentials.
2) Once signed in, you should see a prompt to _Enable Custom Search API_. Click the drop down and press _+ Create a new Project_. Type in "Movie Search Engine" and hit next.
3) You should receive an API Key. This needs to be added as an environment variable. Open up `.env` at the root of this project and add the following:
```
GOOGLE_API_KEY=<your API key>
```
4) Visit your [GCSE Control Panel](https://programmablesearchengine.google.com/cse/all) and press the **Add** button. Enter "images.google.com" under _Sites to search_. Click **Create**
5) On the next page, hit the **Control Panel** button. Then look for _Search engine ID_. This ID will also need to be added to our environment variables. Add this to `.env`
```
GOOGLE_ENGINE_ID=<search engine id>
```
6) Back on the Control Panel page in your browser, scroll down to _Image_ search switch the toggle to **On**. Similarly, scroll down to _Search the entire web_ and switch that toggle to **On**.

Now, the first image that GCSE finds for a given movie will be displayed on the app.



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