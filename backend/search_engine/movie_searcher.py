from django.db.models import Q

class MovieSearcher:
    # Given search parameters title, keyword, vote_average
    # Create a list of movies that match at least one of the parameters
    # Such that every entry in the list contains summary information about
    # how it matched the criteria.
    # Such that movies are ordered by the number of criteria they matched 
    def __init__(self, queryset):
        self.queryset = queryset
    
    def search_movies(self, title = None, keywords = None,
                      low_vote_average = None, high_vote_average = None):
        matched_movies = (
            self.get_title_matches(title) |
            self.get_multiple_keyword_matches(keywords) |
            self.get_vote_average_matches(low_vote_average, high_vote_average)
        ).distinct()
        return matched_movies
    
    def get_summary_information(self, title = None, keyword = None,
                            low_vote_average = None, high_vote_average = None):
        summary = SummaryInformation()

        for match in self.get_title_matches(title):
            summary.add_match(match.id, 'title', match.title)
        
        for match in self.get_keyword_matches(keyword):
            summary.add_match(match.id, 'keyword', keyword)

        for match in self.get_vote_average_matches(low_vote_average, high_vote_average):
            summary.add_match(match.id, 'vote_average', match.vote_average)

        return summary

    def get_title_matches(self, title):
        if title is not None:
            return self.queryset.filter(title__icontains=title)
        return self.queryset.none()

    def get_multiple_keyword_matches(self, keywords):
        empty_queryset = self.queryset.none()
        if keywords is None:
            return empty_queryset
        
        individual_matches = [self.get_keyword_matches(k) for k in keywords]
        return empty_queryset.union(*individual_matches)


    def get_keyword_matches(self, keyword):
        if keyword is not None:
            return self.queryset.filter(keywords__name__iexact=keyword)
        return self.queryset.none()
    
    def get_vote_average_matches(self, vote_lower_bound, vote_upper_bound):
        if vote_lower_bound is not None and vote_upper_bound is not None:
            return self.queryset.filter(
                vote_average__gte=vote_lower_bound
            ).filter(
                vote_average__lte=vote_upper_bound
            )
        elif vote_lower_bound is not None:
            return self.queryset.filter(vote_average__gte=vote_lower_bound)
        elif vote_upper_bound is not None:
            return self.queryset.filter(vote_average__lte=vote_upper_bound)
        
        return self.queryset.none()


class SummaryInformation:
    def __init__(self):
        self.summary = dict()

    def add_match(self, movie_id, match_type, match_contents):
        if movie_id not in self.summary:
            self.summary[movie_id] = list()

        self.summary[movie_id].append({
            'type': match_type,
            'contents': match_contents
        })
    
    def __str__(self):
        return self.summary.__str__()