from .pre_fitting import prefit_compute
from .model import model_knn


def fit(queried_movie_type, standard_query_data):
    reply = model_knn(-1, *prefit_compute(queried_movie_type, standard_query_data))
    return reply[0]['imdbID'].values.tolist()
