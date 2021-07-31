from django.db.models import F

class MovieSearcher:
    def __init__(self, queryset):
        self.queryset = queryset
    
    def search_movies(self, title = None, keywords = None,
                      low_vote_average = None, high_vote_average = None):
        self.queryset.update(match_score=0)

        search_matches = [self.get_title_matches(title),
                          *self.get_multiple_keyword_matches(keywords),
                          self.get_vote_average_matches(low_vote_average, high_vote_average)
        ]

        for match in search_matches:
            self.increment_match_score(match)

        return self.queryset.none().union(*search_matches)
    
    def get_summary_information(self, title = None, keywords = None,
                            low_vote_average = None, high_vote_average = None):
        summary = SummaryInformation()

        for match in self.get_title_matches(title):
            summary.add_match(match.id, 'title', match.title)
        
        # Iterate through every keyword and add summary information about all movies
        # that have keyword matches
        if keywords is not None:
            for keyword in keywords:
                for match in self.get_keyword_matches(keyword):
                    summary.add_match(match.id, 'keyword', keyword)

        for match in self.get_vote_average_matches(low_vote_average, high_vote_average):
            summary.add_match(match.id, 'vote_average', match.vote_average)

        return summary
    

    def increment_match_score(slf, queryset):
        queryset.update(match_score = F('match_score') + 1)

    def get_title_matches(self, title):
        if title is not None:
            return self.queryset.filter(title__icontains=title)
        return self.queryset.none()

    def get_multiple_keyword_matches(self, keywords):
        """
        Returns a list of keyword matches for every keyword in input list
        """
        empty_queryset = self.queryset.none()
        if keywords is None:
            return empty_queryset
        if not isinstance(keywords, list):
            raise ValueError("Input must be a list of keywords, not single keyword")
        
        return [self.get_keyword_matches(k) for k in keywords]


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
    """
    Stores information detailing how a movie matched a list of search criteria. Stores a 
    dictionary of movies and their corresponding Match Summary. For every movie, the 
    Match Summary is format like so:

    [
        {
            'type': <match_type>
            'contents': <match_contents>
        },
        {
            'type': <match_type>
            'contents': <match_contents>
        },
        ...
    ]

    <match_type> is one of the following match criteria: title, keyword, vote_average.
    <match_contents> provides context and reasoning for a given match. For example, if the match is
    of type title, the <match_contents> will provide the title of the movie that was matched.
    
    The SummaryInformation tracks movies by movie ID's. Therefore, in order to add a movie to the
    class, a the movie must have a unique ID.
    
    """
    def __init__(self):
        self.match_summaries = dict()
        self.match_scores = dict()

    def add_new_movie(self, movie_id):
        self.match_summaries[movie_id] = list()
        self.match_scores[movie_id] = 0

    def add_match(self, movie_id, match_type, match_contents, match_score = 0):
        if movie_id not in self.match_summaries:
            self.add_new_movie(movie_id)

        self.match_scores[movie_id] = match_score
        self.match_summaries[movie_id].append({
            'type': match_type,
            'contents': match_contents
        })

    def set_match_score(self, movie_id, match_score):
        if movie_id not in self.match_summaries:
            self.add_new_movie(movie_id)
        
        self.match_scores[movie_id] = match_score

    def get_match_summary(self, movie_id):
        return self.match_summaries[movie_id]

    def get_match_score(self, movie_id):
        return self.match_scores[movie_id]

    def get_movie_count(self):
        return len(self.match_summaries)

    def get_movie_ids(self):
        return self.match_summaries.keys()
    
    def __str__(self):
        return self.match_summaries.__str__()