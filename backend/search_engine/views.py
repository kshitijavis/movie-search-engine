from django.http import HttpResponse
from rest_framework import generics
from search_engine.models import Movie, Keyword
from search_engine.serializers import MovieSerializer

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
