from rest_framework import generics
from search_engine.models import Movie, Keyword
from search_engine.serializers import MovieSerializer, RankedMovieSerializer, KeywordSerializer
from django.http import HttpResponse

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
        queryset = Movie.objects.all()

        title = self.request.query_params.get('title')

        if title is not None:
            queryset = queryset.filter(title__exact=title)

        return queryset