from django.test import TestCase
from search_engine.models import Movie, Keyword
from . import movie_searcher

# Model tests
class MovieKeywordsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        fighting = Keyword.objects.create(name='fighting')
        superhero = Keyword.objects.create(name='superhero')
        avengers = Movie.objects.create(title="Avengers")

        avengers.keywords.add(fighting)
        avengers.keywords.add(superhero)
    
    # Sanity check to make sure many-to-many relationship works
    def testKeywordsInMovie(self):
        avengers = Movie.objects.get(title='Avengers')
        superhero = Keyword.objects.get(name='superhero')
        fighting = Keyword.objects.get(name='fighting')
        # Test that avengers contains the two keywords
        self.assertIn(fighting, avengers.keywords.all())
        self.assertIn(superhero, avengers.keywords.all())
    
    # Sanity check to make sure many-to-many relationship works
    def testMovieInKeywords(self):
        avengers = Movie.objects.get(title='Avengers')
        superhero = Keyword.objects.get(name='superhero')
        fighting = Keyword.objects.get(name='fighting')
        # Test that both keywords contain the movie
        self.assertIn(avengers, superhero.movies.all())
        self.assertIn(avengers, fighting.movies.all())

# Movie searcher tests
class MovieSearcherTestCase(TestCase):
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

        self.searcher = movie_searcher.MovieSearcher(Movie.objects.all())

    def testSearchByTitle(self):
        results = self.searcher.search_movies(name="Space")

        self.assertEqual(len(results), 1)
        self.assertIn(self.space_jam, results)
    
    def testSearchByTitle(self):
        results = self.searcher.search_movies(keywords=["action"])
        results_list = list(results.all())

        expected_list = [self.interstellar, self.avengers]
        self.assertCountEqual(results_list, expected_list)
    
    def testSearchByLowVoteAverage(self):
        results = self.searcher.search_movies(low_vote_average=8)
        results_list = list(results.all())

        expected_list = [self.interstellar, self.avengers]
        self.assertCountEqual(results_list, expected_list)
    
    def testSearchByHighVoteAverage(self):
        results = self.searcher.search_movies(high_vote_average=9)
        results_list = list(results.all())

        expected_list = [self.space_jam, self.avengers]
        self.assertCountEqual(results_list, expected_list)

    def testSearchByLowAndHighVoteAverage(self):
        results = self.searcher.search_movies(low_vote_average=8, high_vote_average=9)

        self.assertEqual(len(results), 1)
        self.assertIn(self.avengers, results)
    
    def testCombination_TitleAndKeyword(self):
        results = self.searcher.search_movies(title="Avengers", keywords=["space"])
        results_list = list(results.all())

        expected_list = [self.avengers, self.interstellar, self.space_jam]
        self.assertCountEqual(results_list, expected_list)

    def testCombination_TitleAndVoteAverage(self):
        results = self.searcher.search_movies(title="Avengers", high_vote_average=7)
        results_list = list(results.all())

        expected_list = [self.space_jam, self.avengers]
        self.assertCountEqual(results_list, expected_list)

    def testCombination_TitleAndKeywordAndVoteAverage(self):
        results = self.searcher.search_movies(title="Avengers", high_vote_average=7, keywords=['space'])
        results_list = list(results.all())

        expected_list = [self.space_jam, self.avengers, self.interstellar]
        self.assertCountEqual(results_list, expected_list)

    def testCaseInsensitiveMatching(self):
        results = self.searcher.search_movies(title="avenGERS", keywords=['SpACE'])
        results_list = list(results.all())

        expected_list = [self.space_jam, self.avengers, self.interstellar]
        self.assertCountEqual(results_list, expected_list)
