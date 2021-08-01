from rest_framework import generics
from search_engine.models import Movie, Keyword
from search_engine.serializers import MovieSerializer, RankedMovieSerializer, KeywordSerializer
from django.http import HttpResponse
from search_engine.movie_searcher import MovieSearcher, SummaryInformation

# Create your views here.
def index(request):
    return HttpResponse("Hello World")

class MovieList(generics.ListAPIView):
    """
    List all movies
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetail(generics.RetrieveUpdateAPIView):
    """
    Get details about a single movie
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class KeywordList(generics.ListAPIView):
    """
    List all keywords
    """
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class RankedMovieSearch(generics.ListAPIView):
    serializer_class = RankedMovieSerializer

    def get_queryset(self):
        title, keywords, vote_lower_bound, vote_upper_bound = self.get_query_params(self.request)

        movie_searcher = MovieSearcher(Movie.objects.all())
        search_results = movie_searcher.search_movies(
            title, keywords, vote_lower_bound, vote_upper_bound
<<<<<<< HEAD
        ).order_by('-match_score', 'title')
=======
        ).order_by('match_score', 'title')
>>>>>>> 1dbff3f... Add ordering to movie search results
        return search_results.all()

    def get_serializer_context(self):
        title, keywords, vote_lower_bound, vote_upper_bound = self.get_query_params(self.request)

        movie_searcher = MovieSearcher(Movie.objects.all())
        summary_information = movie_searcher.get_summary_information(
            title, keywords, vote_lower_bound, vote_upper_bound
        )

        context = super(RankedMovieSearch, self).get_serializer_context()
        context.update({"match_summary": summary_information})
        return context
        
    def get_query_params(self, request):
        title = request.query_params.get('title')
        keywords = request.query_params.getlist('keyword') # Get list of keyword params
        vote_lower_bound = request.query_params.get('vote_lower_bound')
        vote_upper_bound = request.query_params.get('vote_upper_bound')

        return (title, keywords, vote_lower_bound, vote_upper_bound)