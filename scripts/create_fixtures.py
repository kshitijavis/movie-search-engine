import pandas as pd
import json
import ast

def main():
    # Read files as dataframe
    dfMovies = pd.read_csv("data/movies_metadata.csv")
    dfKeywords = pd.read_csv("data/keywords.csv")

    # Convert dataframe into Django data fixtures
    movieFixtures = buildMovieFixture(dfMovies)
    keywordFixtures = buildKeywordFixture(dfKeywords)
    movieKeywordFixtures = buildMovieKeywordFixture(dfKeywords)

    # Save fixtures in search_engine directory
    searchEngineDirectory = "backend/search_engine/"
    with open(searchEngineDirectory + "fixtures/movies.json", 'w') as f:
        json.dump(movieFixtures, f, indent=2)
    
    with open(searchEngineDirectory + "fixtures/keywords.json", 'w') as f:
        json.dump(keywordFixtures, f, indent=2)
    
    with open(searchEngineDirectory + "fixtures/movie_keywords.json", 'w') as f:
        json.dump(movieKeywordFixtures, f, indent=2)

def buildMovieFixture(dfMovies):
    modelName = "search_engine.movie"
    defaultValues = {"title": '', "tagline": '', "overview":'', "vote_average": ''}

    # Convert every row of dataframe into fixture entry, keeping only necessary columns
    moviesFixtures = [None] * len(dfMovies)
    for index, row in dfMovies.iterrows():
        filteredRow = row[['title','tagline','overview','vote_average']]
        filteredRow.fillna(value=defaultValues, inplace=True)
        fields = filteredRow.to_dict()

        entry = buildFixtureEntry(modelName, row['id'], fields)
        moviesFixtures[index] = entry
    
    return moviesFixtures

def buildKeywordFixture(dfKeywords):
    modelName = "search_engine.keyword"

    # Use dictionary to extract all unique keyword-id pairs
    idKeywords = dict()
    for jsonEntry in dfKeywords['keywords']:
        # For every entry, iterate through keyords in json and add to dict
        keywordData = ast.literal_eval(jsonEntry)
        for keyword in keywordData:
            id = keyword['id']
            name = keyword['name']
            idKeywords[id] = name
    
    # Convert keyword-id dictionary into Django fixture
    keywordFixtures = []
    for id in idKeywords:
        fields = {
            'name': idKeywords[id]
        }
        entry = buildFixtureEntry(modelName, id, fields)
        keywordFixtures.append(entry)
    
    return keywordFixtures

def buildMovieKeywordFixture(dfKeywords):
    modelName = "search_engine.movie_keywords"

    primaryKey = 1
    fixtures = []
    for index, row in dfKeywords.iterrows():
        movieId = row['id']
        # For every entry, iterate through keyords in json and add to dict
        keywordData = ast.literal_eval(row['keywords'])
        for keyword in keywordData:
            keywordId = keyword['id']
            fields = {
                "movie_id": movieId,
                "keyword_id": keywordId,
            }
            entry = buildFixtureEntry(modelName, primaryKey, fields)
            primaryKey += 1
            fixtures.append(entry)
    
    return fixtures

def buildFixtureEntry(modelName, primaryKey, fields):
    return {
        "model": modelName,
        "pk": primaryKey,
        "fields": fields
    }

if __name__ == '__main__':
    main()