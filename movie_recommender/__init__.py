import pandas as pd
import os
import numpy as np

data_dir = os.path.join(os.path.dirname(__file__), 'data')
hollywood_data = pd.read_csv(os.path.join(data_dir, "hollywood.txt"),error_bad_lines=False,index_col=False)
bollywood_data = pd.read_csv(os.path.join(data_dir, "bollywood.txt"),error_bad_lines=False,index_col=False)
british_data = pd.read_csv(os.path.join(data_dir, "british.txt"),error_bad_lines=False,index_col=False)
chinese_data = pd.read_csv(os.path.join(data_dir, "chinese.txt"),error_bad_lines=False,index_col=False)
korean_data = pd.read_csv(os.path.join(data_dir, "korean.txt"),error_bad_lines=False,index_col=False)
nollywood_data = pd.read_csv(os.path.join(data_dir, "nollywood.txt"),error_bad_lines=False,index_col=False)
thai_data = pd.read_csv(os.path.join(data_dir, "thai.txt"),error_bad_lines=False,index_col=False)
am_shows_data = pd.read_csv(os.path.join(data_dir, "america_tv_show.txt"),error_bad_lines=False,index_col=False)
k_drama_data = pd.read_csv(os.path.join(data_dir, "korean_drama.txt"),error_bad_lines=False,index_col=False)


def parse_year_show(x):
    try:
        return int(x.split('–')[0]) >= 2005
    except:
        return False

hollywood_data.drop_duplicates(subset=['imdbID'], keep='first', inplace=True, ignore_index=True)
bollywood_data.drop_duplicates(subset=['imdbID'], keep='first', inplace=True, ignore_index=True)
nollywood_data.drop_duplicates(subset=['imdbID'], keep='first', inplace=True, ignore_index=True)
british_data.drop_duplicates(subset=['imdbID'], keep='first', inplace=True, ignore_index=True)
chinese_data.drop_duplicates(subset=['imdbID'], keep='first', inplace=True, ignore_index=True)
korean_data.drop_duplicates(subset=['imdbID'], keep='first', inplace=True, ignore_index=True)
thai_data.drop_duplicates(subset=['imdbID'], keep='first', inplace=True, ignore_index=True)
k_drama_data.drop_duplicates(subset=['imdbID'], keep='first', inplace=True, ignore_index=True)
am_shows_data.drop_duplicates(subset=['imdbID'], keep='first', inplace=True, ignore_index=True)


dict_tags_movies = {"hollywood":(hollywood_data['title'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + hollywood_data['year'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") + ", " + hollywood_data['actors'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+ ", " + hollywood_data['Plot'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") + ":" + hollywood_data['imdbID'].astype(np.str_)).values,
                         "bollywood": (bollywood_data['title'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + bollywood_data['year'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + bollywood_data['actors'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+", " + bollywood_data['Plot'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+":" + bollywood_data['imdbID'].astype(np.str_)).values,
                         "nollywood": (nollywood_data['title'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + nollywood_data['year'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + nollywood_data['actors'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+", " + nollywood_data['Plot'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+":" + nollywood_data['imdbID'].astype(np.str_)).values,
                         "british movies": (british_data['title'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + british_data['year'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + british_data['actors'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+", " + british_data['Plot'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+":" + british_data['imdbID'].astype(np.str_)).values,
                         "chinese movies" :(chinese_data['title'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + chinese_data['year'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + chinese_data['actors'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+", " + chinese_data['Plot'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+":" + chinese_data['imdbID'].astype(np.str_)).values,
                         "korean movies": (korean_data['title'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + korean_data['year'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + korean_data['actors'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+", " + korean_data['Plot'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+":" + korean_data['imdbID'].astype(np.str_)).values,
                         "thai movies" : (thai_data['title'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + thai_data['year'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + thai_data['actors'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+", " + thai_data['Plot'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+":" + thai_data['imdbID'].astype(np.str_)).values
                        }

dict_tags_series = {"tv-show": (am_shows_data['title'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + am_shows_data['year'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+", " + am_shows_data['actors'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+", " + am_shows_data['Plot'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+ ":" + am_shows_data['imdbID'].astype(np.str_)).values,
                    "korean drama": (k_drama_data['title'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "") +", " + k_drama_data['year'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+", " + k_drama_data['actors'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+", " + k_drama_data['Plot'].astype(np.str_).str.lower().str.replace(".", "").str.replace(",", "").str.replace("-", "")+ ":" + k_drama_data['imdbID'].astype(np.str_)).values
                    }    

def filter_year(year, limit=1990):
    try:
        return int(year) >= limit
    except:
        try:
            return int(year.split('–')[0]) >= limit
        except:
            return False

def parse_year(year):
    try:
        return int(year)
    except:
        return int(year.split('–')[0])

hollywood_data = hollywood_data[hollywood_data["year"]>=1990]
bollywood_data = bollywood_data[bollywood_data["year"]>=1990]
british_data = british_data[british_data["year"].apply(lambda x: filter_year(x))]
chinese_data = chinese_data[chinese_data["year"].apply(lambda x: filter_year(x,1970))]
nollywood_data = nollywood_data[nollywood_data["year"].apply(lambda x: filter_year(x))]
korean_data = korean_data[korean_data["year"].apply(lambda x: filter_year(x))]
thai_data = thai_data[thai_data["year"].apply(lambda x: filter_year(x))]
bollywood_data = bollywood_data[bollywood_data["year"].apply(lambda x: filter_year(x))]
hollywood_data = hollywood_data[hollywood_data["year"].apply(lambda x: filter_year(x))]

british_data['year'] = british_data["year"].apply(parse_year).astype(np.int64)
chinese_data['year'] = chinese_data["year"].apply(parse_year).astype(np.int64)
nollywood_data['year'] = nollywood_data["year"].apply(parse_year).astype(np.int64)
korean_data['year'] = korean_data["year"].apply(parse_year).astype(np.int64)
thai_data['year'] = thai_data["year"].apply(parse_year).astype(np.int64)
bollywood_data['year'] = bollywood_data["year"].apply(parse_year).astype(np.int64)
hollywood_data['year'] = hollywood_data["year"].apply(parse_year).astype(np.int64)


dict_data = {
	"hollywood":hollywood_data,
	"bollywood":bollywood_data,
	"tv-show": am_shows_data,
    "british movies":british_data,
    "chinese movies":chinese_data,
    "korean movies":korean_data,
    "nollywood":nollywood_data,
    "thai movies":thai_data,
    "korean drama":k_drama_data
}