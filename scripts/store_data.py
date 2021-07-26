"""

This script takes data the files movies_metadata.csv and keywords.csv from
the data directory and stores them in a MySQL database, as specified in the
environment variables in the .env file.

"""
from json import load
from dotenv import load_dotenv
import os
import pandas as pd
import ast
import sqlalchemy

def main():
    # Get database authentication parameters
    load_dotenv()
    dbName = os.getenv("DATABASE_NAME")
    dbUser = os.getenv("DATABASE_USER")
    dbPassword = os.getenv("DATABASE_PASSWORD")
    dbHost = os.getenv("DATABASE_HOST")
    dbPort = os.getenv("DATABASE_PORT")

    dfMovies = pd.read_csv("data/movies_metadata.csv")
    dfKeywords = pd.read_csv("data/keywords.csv")

    cleanedMovies = cleanMoviesDf(dfMovies)
    allKeywords = extractAllKeywords(dfKeywords)
    movieKeywordJunction = buildMovieKeywordJunction(dfKeywords)

    engine = sqlalchemy.create_engine(f'mysql://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{dbName}')
    cleanedMovies.to_sql('search_engine_movie', con=engine, if_exists='append', index=False)
    allKeywords.to_sql('search_engine_keyword', con=engine, if_exists='append', index=False)
    movieKeywordJunction.to_sql('search_engine_movie_keywords', con=engine, if_exists='append', index=False)


def cleanMoviesDf(dfMovies):
    """
    Cleans up a movies dataframe pulled from movies_metadata.csv

    Args:
      dfMovies : A movies dataframe pulled directly from movies_metadata.csv without any prior filtering

    Returns:
      A pandas dataframe with only the columns "id", "title", "tagline", "overview", and "vote_average"
      For all columns above, replaces null values with empty strings or 0
      The original dataframe was found to have invalid and duplicate ids, which are all dropped
    """
    defaultValues = {"title": '', "tagline": '', "overview":'', "vote_average": 0}
    dfMovies = dfMovies.fillna(value=defaultValues)
    dfMovies['id'] = pd.to_numeric(dfMovies['id'], errors='coerce', downcast='integer')
    dfMovies = dfMovies.drop_duplicates(subset=['id']).dropna(subset=['id'])
    return dfMovies[['id', 'title','tagline','overview','vote_average']]

def extractAllKeywords(dfKeywords):
    """
    Retrives a dataframe of all keyword names and their corresponding ids. Iterates through all entires in
    the file keywords.csv and then iterates through all JSON entries of each row. Each iteration yeilds a
    keyword name-id pair that is added to the returned dataframe

    Args:
      dfKeywords : A keywords dataframe pulled directly from movies_metadata.csv without any prior filtering

    Returns:
      A pandas dataframe with only the columns "id" and "name"
    """
    # Use dictionary to extract all unique keyword-id pairs
    idKeywords = dict()
    for jsonEntry in dfKeywords['keywords']:
        # For every entry, iterate through keyords in json and add to dict
        keywordData = ast.literal_eval(jsonEntry)
        for keyword in keywordData:
            id = keyword['id']
            name = keyword['name']
            idKeywords[id] = name
            
    return pd.DataFrame(idKeywords.items(), columns=['id','name'])

def buildMovieKeywordJunction(dfKeywords):
    """
    Cretes a junction table to build a many-to-many relationship between movies and keywords
    Iterates through every keyword in keywords.csv and finds all pairs between movie_ids and keywords_ids

    Args:
      dfKeywords : A keywords dataframe pulled directly from movies_metadata.csv without any prior filtering

    Returns:
      A pandas dataframe with the columns "movie_ids" and "keyword_ids". Every row represents one relationship
      between movies and keywords.
      Duplicate relationships are dropped from the table before returning
    """
    movieKeywordIds = []
    for index, row in dfKeywords.iterrows():
        movieId = row['id']
        # For every entry, iterate through keyords in json and add to dataframe
        keywordData = ast.literal_eval(row['keywords'])
        for keyword in keywordData:
            keywordId = keyword['id']
            movieKeywordIds.append((movieId, keywordId))
    
    movieKeywordJunction = pd.DataFrame(movieKeywordIds, columns=['movie_id', 'keyword_id']).drop_duplicates()
    return movieKeywordJunction

if __name__ == '__main__':
    main()