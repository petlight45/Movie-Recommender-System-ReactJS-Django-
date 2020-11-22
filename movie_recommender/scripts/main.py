from .fitting import fit
from .. import dict_tags_movies,dict_tags_series
from .movie_querier import get_name_movie

def get_recommendations_(movie_tag, movie_type):
	movie_tag = movie_tag[0]
	movie_type = movie_type[0]
	print(f"\n\n{movie_tag}\n{movie_type}")
	if movie_type.lower() in ["tv-show","korean drama"]:
		movie_type_ = "series"
	else:
		movie_type_ = 'movie'
	standard_query_data = get_name_movie(movie_tag,dict_tags_movies[movie_type.lower()] if movie_type_ == "movie" else dict_tags_series[movie_type.lower()] ,movie_type_)
	if standard_query_data[0]:
		return [fit(movie_type, standard_query_data[0]),standard_query_data[0][0]]
	else:
		return standard_query_data