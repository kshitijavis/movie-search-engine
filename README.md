# movie-search-engine

## Installation
### Get the Data
1) Clone this repository onto your local machine. The root of this project will be the `movie-search-engine` directory.
    ```
    git clone https://github.com/kshitijavis/movie-search-engine.git movie-search-engine
    ```
2) This app uses two datasets from the [Movies Dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset) on Kaggle. From Kaggle, download the `movies_metadata.csv` and `keywords.csv` files. Create a `data` directory in the root of your project and move the two files into the new directory.
### Setup MySQL Database
The following steps will create a MySQL user and database where movie data will be stored.

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
To connect Django to a MySQL database, you will need to add database information to a `.env` file
Create a `.env` in the root of your project and populate it like so
```
DATABASE_NAME=<database name>
DATABASE_USER=<database username>
DATABASE_PASSWORD=<database password>
DATABASE_HOST=<database host>
DATABASE_PORT=<port that database is running on>
```
Replace all fields wrapped in the angle brackets with your new database credentials.
### Add Tables and Data to Database
1) Make sure you have **python3** downloaded.
2) In your command line, navigate to the root of this project.
3) Navigate to the backend directory
    ```
    cd backend
    ```
4) Setup tables in your database as specified in the Python Django configuration. This is done through Django migrations
    ```
    python manage.py migrate
    ```
5) Navigate to back to root directory and then to `scripts` directory.
    ```
    cd ..
    ```
6) Run `store_data.py` script in the `scripts` directory using Python. This will populate your new database tables with the data in your `.csv` files.
    ```
    python scripts/store_data.py
    ```
    If you have trouble running this script, make sure your [environment variables](#set-environment-variables) are setup correctly in your `.env` file and your [data is correctly stored](#get-the-data) in a `data` directory.
### Setup Dependencies
1) In your command line, navigate to the root of this project
2) Install python dependencies as specified in `requirements.txt`. You may want to install dependencies in a virtual environment.
    ```
    pip install -r requirements.txt
    ```
3) Navigate to the frontend directory. Then install node dependencies.
    ```
    cd frontend
    npm install
    ```
### Running the Search Engine
5) Run the backend Django server
    ```
    python mange.py runserver
    ```
6) Navigate to the frontend directory
    ```
    cd ..
    cd frontend
    ```
7) Run the client server
    ```
    npm start
    ```
8) The movie search engine should now be running locally on `localhost:3000`
## Optional: Add Image Search
The `/movies/<id>` endpoint on the React App gives detailed information about a given movie. The app also uses Google Custom Search Engine (GCSE) to find and display a cover image of the movie. To set up image-rendering, follow these steps.
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

## Optional: Testing
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
