from rest_framework import serializers

from .models import Keyword, Movie

class MovieSerializer(serializers.ModelSerializer):
    # Since Keyword objects are small (only have IDs and names),
    # it's convenient to relate keywords by their name
    keywords = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Keyword.objects.all())
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'tagline', 'overview', 'vote_average', 'keywords']

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'name']

class RankedMovieSerializer(serializers.ModelSerializer):
    keywords = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Keyword.objects.all())
    
    # Every Movie model is paired with a match_sumary and match)scire. A movies match_summary
    # is a list of dictionaries, each describing the type and contents of the match
    # A match_score describes how closely a movie matches the search criteria
    match_summary = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'tagline', 'overview', 'vote_average', 
                  'keywords', 'match_summary', 'match_score']

    def get_match_summary(self, obj):
        # A SummaryMatch object is passed through context and the correct summary for this
        # movie is retrieved by Movie id (obj.id)
        return self.context['match_summary'].get_match_summary(obj.id)