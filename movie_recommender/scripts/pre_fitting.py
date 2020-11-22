from .. import dict_data
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from rapidfuzz import fuzz,process

def prefit_compute(queried_movie_type, standard_query_data):
    standard_train_data = dict_data[queried_movie_type.lower()]
    if queried_movie_type.lower() in ["tv-show","korean drama"]:
        queried_movie_type = "series"
    else:
        queried_movie_type = 'movie'

    train_data = standard_train_data.copy()
    
    if queried_movie_type == 'movie':
        try:
            standard_query_data[8] = int(standard_query_data[8].split('–')[0])
        except:
            pass
    train_data = train_data[train_data['imdbID'] != standard_query_data[0]]
    train_data_with_query = train_data.append(pd.Series(index=train_data.columns, data=standard_query_data),ignore_index=True)
    if queried_movie_type != "series":
        train_data_with_query.drop('BoxOffice',axis=1,inplace=True)
    column_unknown = ['directors','writers', 'actors', 'production', 'country', 'language','Plot','Rated','Type','Genre']
    for c in column_unknown:
        try:
            train_data_with_query[c].fillna('Unknown',inplace=True)
        except:
            pass
    if queried_movie_type == 'movie':
        column_median = ['imdbRating', 'rottenTomatoRating','metacriticRating','duration','year']
    else:
        column_median = ['imdbRating','duration', 'totalSeasons']
    for c in column_median:
        
        try:
            train_data_with_query[c].fillna(train_data_with_query[c].median(),inplace=True)
        except Exception as err:
            raise err
    if queried_movie_type == 'movie':
        column_zero = ['oscarNominations',
               'noOfAwards', 'noOfNominations','imdbVotes']
    else:
        column_zero = ['noOfNominations','imdbVotes','noOfAwards']
    for c in column_zero:
        try:
            train_data_with_query[c].fillna(0,inplace=True)
        except:
            pass
    if queried_movie_type == 'movie':
        column_mode = []
    else:
        column_mode = ['year']
    for c in column_mode:
        try:
            train_data_with_query[c].fillna(train_data_with_query[c].mode()[0],inplace=True)
        except Exception as err:
            raise err

    def eucld_dist(a,b):
        return (abs(a-b))

    def extract_unique_nominations(x):
        try:
            for (value, nomination) in re.findall(r'(\d+?):([a-zA-Z\s]+);', x, re.IGNORECASE):
                list_special_awards.append(nomination)
        except:
            pass
        return x
        
    def extract_nom_val(x,nom):
        try:
            res = re.findall(fr'(\d+?):{nom}', x, re.IGNORECASE)
            if res:
                return int(res[0]) 
            else:
                return 0
        except:
            pass
    if queried_movie_type.lower() == 'series':
        list_special_awards = ['Golden Globe', 'Primetime Emmy']
    #     movies_data_am_show['specialNominations'].apply(extract_unique_nominations)
        list_special_awards = list(set(list_special_awards))
        for spec_nom in list_special_awards:
            train_data_with_query[spec_nom] = train_data_with_query['specialNominations'].apply(lambda x: extract_nom_val(x,spec_nom))
            column_zero.append(spec_nom)
            train_data_with_query[spec_nom].fillna(0,inplace=True)

    if queried_movie_type == 'series':
        train_data_with_query['year'] = train_data_with_query['year'].apply(lambda x: int(x.split('–')[0]))
        column_zero.append('year');

    dict_cols_init = dict((j,i) for i,j in enumerate(train_data_with_query.columns))

    train_data_with_query.iloc[-1,3] = np.float64(train_data_with_query.iloc[-1,3])

    train_data_with_query['imdbRating']*=10

    standard_query_data = train_data_with_query.iloc[-1,:]

    train_data_with_query['actor_fuzz'] = train_data_with_query['actors'].apply(lambda x:fuzz.token_sort_ratio(standard_query_data[dict_cols_init['actors']],x))
    dict_cols_init['actor_fuzz'] = len(dict_cols_init.values())
    column_median.append('actor_fuzz')
    train_data_with_query['language_fuzz'] = train_data_with_query['language'].apply(lambda x:fuzz.token_sort_ratio(standard_query_data[dict_cols_init['language']],x))
    dict_cols_init['language_fuzz'] = len(dict_cols_init.values())
    column_median.append('language_fuzz')
    train_data_with_query['rated_fuzz'] = train_data_with_query['Rated'].apply(lambda x:fuzz.token_sort_ratio(standard_query_data[dict_cols_init['Rated']],x))
    dict_cols_init['rated_fuzz'] = len(dict_cols_init.values())
    column_median.append('rated_fuzz')
    train_data_with_query['type_fuzz'] = train_data_with_query['Type'].apply(lambda x:fuzz.token_sort_ratio(standard_query_data[dict_cols_init['Type']],x))
    dict_cols_init['type_fuzz'] = len(dict_cols_init.values())
    column_median.append('type_fuzz')
    train_data_with_query['plot_fuzz'] = train_data_with_query['Plot'].apply(lambda x:fuzz.token_sort_ratio(standard_query_data[dict_cols_init['Plot']],x))
    dict_cols_init['plot_fuzz'] = len(dict_cols_init.values())
    column_median.append('plot_fuzz')
    train_data_with_query['genre_fuzz'] = train_data_with_query['Genre'].apply(lambda x:fuzz.token_sort_ratio(standard_query_data[dict_cols_init['Genre']],x))
    dict_cols_init['genre_fuzz'] = len(dict_cols_init.values())
    column_median.append('genre_fuzz')
    train_data_with_query['country_fuzz'] = train_data_with_query['country'].apply(lambda x:fuzz.token_sort_ratio(standard_query_data[dict_cols_init['country']],x))
    dict_cols_init['country_fuzz'] = len(dict_cols_init.values())
    column_median.append('country_fuzz')
    train_data_with_query['title_fuzz'] = train_data_with_query['title'].apply(lambda x:fuzz.token_sort_ratio(standard_query_data[dict_cols_init['title']],x))
    dict_cols_init['title_fuzz'] = len(dict_cols_init.values())
    column_median.append('title_fuzz')

    def scale_data(x, col):
        return ((x/train_data_with_query[col].max()) * 100)
    if queried_movie_type == 'series':
        train_data_with_query['plot_fuzz'] = train_data_with_query['plot_fuzz'].apply(lambda x: 0 if (x <70) else x)
        train_data_with_query['genre_fuzz'] = train_data_with_query['genre_fuzz'].apply(lambda x: 0 if (x <70) else x)
        train_data_with_query['rated_fuzz'] = train_data_with_query['rated_fuzz'].apply(lambda x: 0 if (x <100) else x)
        train_data_with_query['actor_fuzz'] = train_data_with_query['actor_fuzz'].apply(lambda x: 0 if (x <80) else x)
        train_data_with_query['title_fuzz'] = train_data_with_query['title_fuzz'].apply(lambda x: 0 if (x <80) else x)
        train_data_with_query['noOfAwards'] =  train_data_with_query['noOfAwards'].apply(lambda x: scale_data(x, 'noOfAwards'))
        train_data_with_query['noOfNominations'] =  train_data_with_query['noOfAwards'].apply(lambda x: scale_data(x, 'noOfNominations'))
        train_data_with_query['imdbVotes'] =  train_data_with_query['imdbVotes'].apply(lambda x: scale_data(x, 'imdbVotes'))
        # train_data_with_query['Primetime Emmy'] =  train_data_with_query['Primetime Emmy'].apply(lambda x: scale_data(x, 'Primetime Emmy'))
        # train_data_with_query['Golden Globe'] =  train_data_with_query['Primetime Emmy'].apply(lambda x: scale_data(x, 'Golden Globe'))
    else:
        train_data_with_query['title_fuzz'] = train_data_with_query['title_fuzz'].apply(lambda x: 0 if (x <80) else x)
    train_data_with_query.sort_values(by="title_fuzz", ascending=False).head(10)


    if queried_movie_type == 'series':
        train_data_with_query['total_season_dist'] = train_data_with_query['totalSeasons'].apply(lambda x:eucld_dist(x, standard_query_data[dict_cols_init['totalSeasons']]))
        column_median.append('total_season_dist')


    column_genres = ['Action',
           'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
           'Documentary', 'Drama', 'Family', 'Fantasy', 'FilmNoir', 'GameShow',
           'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'RealityTV',
           'Romance', 'SciFi', 'Short', 'Sport', 'TalkShow', 'Thriller', 'War',
           'Western']

    def parse_genre(x):
        try:
            if int(x) in [0,1]:
                return int[x]
            else:
                return 0;
        except:
            return 0
    for col in column_genres:
        train_data_with_query[col] = train_data_with_query[col].fillna(0)


    a = train_data_with_query.copy()


    scaler = StandardScaler()

    to_be_standardized_features = column_median+column_zero
    to_be_standardized_data = train_data_with_query[to_be_standardized_features]


    train_data_with_query_standardized = scaler.fit_transform(to_be_standardized_data)


    for id_, c in enumerate(to_be_standardized_features):
        train_data_with_query[c] = train_data_with_query_standardized[:,id_]


    dict_cols_final = dict((j,i) for i,j in enumerate(train_data_with_query.columns))

    if queried_movie_type == 'movie':
        distance_template = [
            [1, [12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39], 'c','d1',-1],
            [2, [50,52,53,54,55,3,4,5,6,7,8,10,11,51], 'e','d1',1]
        ]
    else:
        distance_template = [
    #         [1, [*list(range(10,38))], 'c','d2',-1],
            [2, [54,55,52,50,8,9,4,3], 'e','d1',1]
        ]
    train_data_2d = train_data_with_query.iloc[:-1,:].values
    labels = train_data_with_query.columns
    train_data_movie_titles_1d = train_data_with_query.iloc[:-1,:]['title'].values
    query_data_1d = train_data_with_query.iloc[-1,:].values
    return [train_data_2d, query_data_1d,train_data_movie_titles_1d,distance_template, labels]