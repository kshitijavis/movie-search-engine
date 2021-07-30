from django.test import TestCase, Client
from search_engine.views import RankedMovieSearch
from search_engine.models import Movie, Keyword
import ast

class RankedMovieSearchTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Build test database once for all test method
        interstellar = Movie.objects.create(title="Interstellar", vote_average=9.8)
        space_jam = Movie.objects.create(title="Space Jam", vote_average=6.7)
        avengers = Movie.objects.create(title="Avengers", vote_average=8.7)

        space = Keyword.objects.create(name="space")
        sports = Keyword.objects.create(name="sports")
        action = Keyword.objects.create(name="action")
        fighting = Keyword.objects.create(name="fighting")

        interstellar.keywords.add(space, action)
        space_jam.keywords.add(space, sports)
        avengers.keywords.add(action, fighting)
    
    def setUp(self):
        # Retrieve movie objects from database for every test method to avoid
        # code repitition
        self.interstellar = Movie.objects.get(title="Interstellar")
        self.space_jam = Movie.objects.get(title="Space Jam")
        self.avengers = Movie.objects.get(title="Avengers")

        self.client = Client()

    def testTitleQueryParam(self):
        get = self.client.get('/searchengine/movies/search/', {'title': 'Avengers'})
        get_content = get.json()
        search_results = get_content['results']
        match_summary = search_results[0]['match_summary']

        self.assertEqual(len(search_results), 1)
        self.assertEqual(len(match_summary), 1)
    
    def testMultipleKeywordQueryParam(self):
        get = self.client.get('/searchengine/movies/search/', {'keyword': ['action', 'space']})
        get_content = get.json()
        search_results = get_content['results']

        print(search_results)