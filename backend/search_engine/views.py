from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from search_engine.models import Movie
from search_engine.serializers import MovieSerializer

# Create your views here.
@api_view(['GET'])
def index(request):
    return HttpResponse("Hello World")

@api_view(['GET', 'POST'])
def movie_list(request, format=None):
    """
    List all movies, or create a new movie
    """

    if request.method == 'GET':
        movies = Movie.objects.order_by('-vote_average')[:100]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def movie_detail(request, pk, format=None):
    """
    Get details about a single movie
    """
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'POST':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
