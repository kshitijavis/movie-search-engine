from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.MovieList.as_view(), name='movie_list'),
    path('movies/<int:pk>/', views.MovieDetail.as_view(), name='movie_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)