import requests
from dotenv import load_dotenv
import os

def SearchMovieImage(movie_title):
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    engine_id = os.getenv("GOOGLE_ENGINE_ID")

    query = {
        'key': api_key,
        'cx': engine_id,
        'q': movie_title,
        'searchType': 'Image',
    }


    url = "https://www.googleapis.com/customsearch/v1"
    response = requests.get(url, params=query)
    return response.json()

    