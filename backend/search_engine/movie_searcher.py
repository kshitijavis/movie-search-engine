from django.db.models import Q

class MovieSearcher:
    def __init__(self, queryset):
        self.queryset = queryset
    
    def search_movies(self, title = None, keyword = None,
                      low_vote_average = None, high_vote_average = None):
        query = Q()
        if title is not None:
            query |= Q(title__icontains=title)
        if keyword is not None:
            query |= Q(keywords__name__iexact=keyword)
        
        if low_vote_average is not None and high_vote_average is not None:
            query |= Q(vote_average__gte=low_vote_average) & Q(vote_average__lte=high_vote_average)
        elif low_vote_average is not None:
            query |= Q(vote_average__gte=low_vote_average)
        elif high_vote_average is not None:
            query |= Q(vote_average__lte=high_vote_average)

        matched_movies = self.queryset.filter(query)
        return matched_movies