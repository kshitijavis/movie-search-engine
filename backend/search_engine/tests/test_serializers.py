from django.test import TestCase
from search_engine.serializers import RankedMovieSerializer
from search_engine.models import Movie, Keyword
from search_engine.movie_searcher import MovieSearcher

class RankedMovieSerializerTestCase(TestCase):
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

        self.searcher = MovieSearcher(Movie.objects.all())

    def testSearchByTitle(self):
        results = self.searcher.search_movies(title="Space")

        self.assertEqual(len(results), 1)
        self.assertIn(self.space_jam, results)
    
    def testSerializerDataLength(self):
        search_results = self.searcher.search_movies(title="Avengers", keywords=["action"])
        match_summary = self.searcher.get_summary_information(title="Avengers", keywords=["action"])

        serializer = RankedMovieSerializer(search_results, many=True, 
                                           context={"match_summary": match_summary})

        self.assertEqual(len(serializer.data), 2)