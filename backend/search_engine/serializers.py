from rest_framework import serializers

from .models import Keyword, Movie

class MovieSerializer(serializers.ModelSerializer):
    # Since Keyword objects are small (only have IDs and names),
    # it's convenient to relate keywords by their name
    keywords = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Keyword.objects.all())
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'tagline', 'overview', 'vote_average', 'keywords']