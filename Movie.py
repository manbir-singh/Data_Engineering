import config
import requests
import pandas as pd


# Set print options to remove df ellipses
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class Movie:
    def __init__(self, movie, year):
        self.movie = movie
        self.year = year
        self.df = pd.DataFrame()
        self.credits_dict = {}
        self.request_list = []
        self.list_of_genres = {28: 'Action', 12: 'Adventure', 16: 'Animation', 35: 'Comedy', 80: 'Crime',
                               90: 'Documentary', 18: 'Drama', 10751: 'Family', 14: 'Fantasy', 36: 'History',
                               27: 'Horror', 10402: 'Music', 9648: 'Mystery', 10749: 'Romance', 878: 'Science Fiction',
                               10770: 'TV Movie', 53: 'Thriller', 10752: 'War', 37: 'Western'}
        self.run()  # Run all methods of Movie class automatically

    def __str__(self):
        return str(self.movie) + ' ' + str(self.year)

    def request_response(self):
        """Retrieve the requested metadata for the given movie and corresponding year.
        Filter based on multiple criteria;
        movie -> to get the movie title
        year -> filter through given movie from only that year
        vote_count -> filter through multiple results with same movie title and year
        """
        r = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' +
                         config.tmdb['tmdb_key'] + '&query=' + self.movie).json()
        # Do not add any metadata to the request list if the movie does not exist, or incorrect title/year are given
        if r['total_results'] != 0:
            metadata = r['results']
            # Use filter function to prevent using a nested for loop to filter exact movie needed
            metadata_filtered = filter(lambda metadata: metadata['original_title'] == self.movie and
                                                        metadata['release_date'][:4] == self.year and
                                                        metadata['vote_count'] > 0, metadata)
            self.request_list.append(list(metadata_filtered))
            return self.request_list[0]

    def get_credits(self):
        """ Get the credits and cast for the given movie."""
        if bool(self.request_list) is False or bool(self.request_list[0]) is False:
            pass
        else:
            movie_id = self.request_list[0][0]['id']
            r = requests.get('https://api.themoviedb.org/3/movie/' + str(movie_id)
                             + '/credits?api_key=' + config.tmdb['tmdb_key'] + '&language=en-US').json()
            return self.credits_dict.update(r)

    def get_director(self):
        # Get the get_credits info and filter for director
        if bool(self.credits_dict) is False:
            pass
        else:
            potential_director = self.credits_dict['crew']
            director = filter(lambda potential_director: potential_director['known_for_department'] == 'Directing',
                              potential_director)
            # Return the main director arbitrarily
            result = list(director)[0]['name'].lower().replace(' ', '').replace('.', '').replace(',', '')
            self.request_list[0][0]['director'] = result
            return result

    def get_cast(self):
        """Return the top 3 cast members for the given movie credits
        """
        if bool(self.credits_dict) is False:
            pass
        else:
            potential_cast = self.credits_dict['cast']
            cast = filter(lambda potential_cast: potential_cast['known_for_department'] == 'Acting', potential_cast)
            # Could have error if list length is less than 3 =, but since when do movies only have less than 3 actors?
            cast = list(cast)
            names = []
            for cast_member in cast:
                names.append(cast_member['name'].lower().replace(' ', '').replace('.', '').replace(',', ''))
            self.request_list[0][0]['cast'] = names[:3]
            return names[:3]

    def get_crew(self):
        """Return the crew for a movie.
        """
        if bool(self.credits_dict) is False:
            pass
        else:
            crew = self.credits_dict['crew']
            self.request_list[0][0]['crew'] = crew
            return crew

    def get_genre(self):
        if bool(self.request_list) is False or bool(self.request_list[0]) is False:
            pass
        else:
            genre_ids = self.request_list[0][0]['genre_ids']
            genre_list = []
            for i in genre_ids:
                genre_list.append(self.list_of_genres[i].lower())
            self.request_list[0][0]['genres'] = genre_list
            return genre_list

    def get_keywords(self):
        if bool(self.request_list) is False or bool(self.request_list[0]) is False:
            pass
        else:
            movie_id = self.request_list[0][0]['id']
            r = requests.get(('https://api.themoviedb.org/3/movie/' + str(movie_id) +
                              '/keywords?api_key={}').format(config.tmdb['tmdb_key'])).json()
            keywords_list_dict = r['keywords']
            keywords = []
            for i in keywords_list_dict:
                keywords.append(i['name'].lower().replace(' ', '').replace(',', '')
                                .replace('.', '').replace('(', '').replace(')', ''))
            self.request_list[0][0]['keywords'] = keywords
            return keywords

    def dataframe_builder(self):
        if bool(self.request_list) is False or bool(self.request_list[0]) is False:
            pass
        else:
            df = pd.DataFrame().from_dict(self.request_list[0])
            self.df = df
            return self.df

    def run(self):
        self.request_response()
        self.get_credits()
        self.get_director()
        self.get_cast()
        self.get_crew()
        self.get_genre()
        self.get_keywords()
        self.dataframe_builder()
