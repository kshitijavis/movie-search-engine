from django.test import TestCase
from search_engine.models import Movie, Keyword

# Model Tests
class MovieKeywordsTestCase(TestCase):
    def setUp(self):
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