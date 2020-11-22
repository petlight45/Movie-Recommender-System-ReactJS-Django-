import requests
import re
from rapidfuzz import fuzz, process
import numpy as np

def get_name_movie(queried_movie_name, train_movies_1d,movie_type):
	def compile_meta_show(imdbID=np.nan,title=np.nan,url=np.nan,imdbRating=np.nan,imdbVotes=np.nan,duration=np.nan,year=np.nan,noOfAwards=np.nan,noOfNominations=np.nan,Action=0,Adult=0,Adventure=0,Animation=0,Biography=0,Comedy=0,Crime=0,Documentary=0,Drama=0,Family=0,Fantasy=0,FilmNoir=0,GameShow=0,History=0,Horror=0,Music=0,Musical=0,Mystery=0,News=0,RealityTV=0,Romance=0,SciFi=0,Short=0,Sport=0,TalkShow=0,Thriller=0,War=0,Western=0,directors=np.nan,writers=np.nan,actors=np.nan,country=np.nan,language=np.nan,Type=np.nan,Plot=np.nan,Rated=np.nan,Genre=np.nan,totalSeasons=np.nan,specialNominations=np.nan):
		url = f'http://www.imdb.com/title/{imdbID}/'
		return [imdbID,title,url,imdbRating,imdbVotes,duration,year,specialNominations,noOfAwards,noOfNominations,Action,Adult,Adventure,Animation,Biography,Comedy,Crime,Documentary,Drama,Family,Fantasy,FilmNoir,GameShow,History,Horror,Music,Musical,Mystery,News,RealityTV,Romance,SciFi,Short,Sport,TalkShow,Thriller,War,Western,directors,writers,actors,country,language,Type,Plot,Rated,Genre,totalSeasons]
    
	def compile_meta(imdbID = np.nan,title = np.nan,url = np.nan,imdbRating = np.nan,
                     rottenTomatoRating = np.nan,metacriticRating = np.nan,
                     imdbVotes = np.nan,duration = np.nan,year = np.nan,
                     oscarNominations = np.nan,noOfAwards = np.nan,noOfNominations = np.nan,Action = 0,Adult = 0,Adventure = 0,
                     Animation = 0,Biography = 0,Comedy = 0,Crime = 0,Documentary = 0,Drama = 0,Family = 0,Fantasy = 0,
                     FilmNoir = 0,GameShow = 0,History = 0,Horror = 0,Music = 0,Musical = 0,Mystery = 0,News = 0,
                     RealityTV = 0,Romance = 0,SciFi = 0,Short = 0,Sport = 0,TalkShow = 0,Thriller = 0,War = 0,
                     Western = 0,directors = np.nan,writers = np.nan,actors = np.nan,production = np.nan,
                     country=np.nan,language=np.nan,Type=np.nan,Plot=np.nan,BoxOffice=np.nan,Rated=np.nan,Genre=np.nan):
		url = f'http://www.imdb.com/title/{imdbID}/'
		return [imdbID,title,url,imdbRating,rottenTomatoRating,metacriticRating,
						 imdbVotes,duration,year,oscarNominations,noOfAwards,noOfNominations,
                         Action,Adult,Adventure,Animation,Biography,Comedy,Crime,Documentary,
                         Drama,Family,Fantasy,FilmNoir,GameShow,History,Horror,Music,Musical,
                         Mystery,News,RealityTV,Romance,SciFi,Short,Sport,TalkShow,Thriller,
                         War,Western,directors,writers,actors,production,country,language,
                         Type,Plot,BoxOffice,Rated,Genre
                         ]

	def get_meta(movie_id,type_):
		url = "https://movie-database-imdb-alternative.p.rapidapi.com/"
		headers = {
		'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com",
		'x-rapidapi-key': "ce15ebaf8dmshfb3801d1cfa22dcp1f4c05jsn1dad2b361974"
		}
		querystring = {"i": f"{movie_id}", "r": "json",'type':type_}
		response = requests.request("GET", url, headers=headers, params=querystring)

		return (response.json())
	def get_id(m_name,type_):
		url = "https://movie-database-imdb-alternative.p.rapidapi.com/"
		headers = {
		    'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com",
		    'x-rapidapi-key': "ce15ebaf8dmshfb3801d1cfa22dcp1f4c05jsn1dad2b361974"
		    }
		querystring = {"page":"1","r":"json","s":f"{m_name}",'type':type_}
		response = requests.request("GET", url, headers=headers, params=querystring)

		return (response.json()['Search'][0]['imdbID'])
	try:
		m_id = get_id(queried_movie_name,movie_type)
	except KeyError as err:
		m_id = process.extractOne(queried_movie_name.lower(), train_movies_1d,scorer=fuzz.token_set_ratio)[0].split(":")[-1]
	except ConnectionError as err:
		return (None, 'Connection Error')
	except:
		return (None, 'Unknown error encountered')
	try:
		movie_meta = get_meta(m_id,movie_type)
		if movie_type != "series":      
			log_obj = dict()
			log_obj['imdbID'] = movie_meta['imdbID']
			log_obj['title'] = movie_meta['Title'].replace(',',"-")
			dict_ratings = {
				'Internet Movie Database': {'name': 'imdbRating', 'pattern': r'(.+?)/'},
				'Rotten Tomatoes': {'name': 'rottenTomatoRating', 'pattern': r'(.+?)%'},
				'Metacritic': {'name': 'metacriticRating', 'pattern': r'(.+?)/'}
			}
			for i, j in [(i['Source'], i['Value']) for i in movie_meta['Ratings']]:
				log_obj[dict_ratings[i]['name']] = float(re.findall(dict_ratings[i]['pattern'], j)[0])
			try:
				log_obj['imdbVotes'] = int(movie_meta['imdbVotes'].replace(',', ''))
			except:
				pass
			try:
				log_obj['duration'] = int(re.findall(r'(\d+)', movie_meta['Runtime'])[0]) * 60
			except:
				pass
			log_obj['year'] = movie_meta['Year']
			nomination_text = movie_meta['Awards']
			if 'Oscar' in nomination_text:
				log_obj['oscarNominations'] = int(re.findall(r'(\d+) Oscar', nomination_text, re.IGNORECASE)[0])
			if 'nominations' in nomination_text:
				log_obj['noOfNominations'] = int(
					re.findall(r'(\d+) nominations', nomination_text, re.IGNORECASE)[0])
			if 'wins' in nomination_text:
				log_obj['noOfAwards'] = int(re.findall(r'(\d+) wins', nomination_text, re.IGNORECASE)[0])
			for i in movie_meta['Genre'].split(','):
				log_obj[i.replace(' ', '').replace('-', '')] = 1
			log_obj['directors'] = movie_meta['Director'].replace(",", '-').replace("N/A", '')
			log_obj['writers'] = movie_meta['Writer'].replace(",", '-').replace("N/A", '')
			log_obj['actors'] = movie_meta['Actors'].replace(",", '-').replace("N/A", '')
			try:
				log_obj['production'] = movie_meta['Production'].replace(",", '-').replace("N/A", '')
			except:
				pass
			log_obj['country'] = movie_meta['Country'].replace(",", '-').replace("N/A", '')
			log_obj['language'] = movie_meta['Language'].replace(",", '-').replace("N/A", '')
			log_obj['Plot'] = movie_meta['Plot'].replace(",", '-').replace("N/A", '')
			log_obj['Type'] = movie_meta['Type'].replace(",", '-').replace("N/A", '')
			log_obj['Rated'] = movie_meta['Rated'].replace(",", '-').replace("N/A", '')
			try:
				log_obj['BoxOffice'] = movie_meta['BoxOffice'].replace(",", '-').replace("N/A", '')
			except:
				pass
			log_obj['Genre'] = movie_meta['Genre'].replace(",", '-').replace("N/A", '')
			return (compile_meta(**log_obj),None)
		else:
			log_obj = dict()
			log_obj['imdbID'] = movie_meta['imdbID']
			log_obj['title'] = movie_meta['Title'].replace(',',"-")
			dict_ratings = {
				'Internet Movie Database': {'name': 'imdbRating', 'pattern': r'(.+?)/'}
			}
			for i, j in [(i['Source'], i['Value']) for i in movie_meta['Ratings']]:
				try:
					log_obj[dict_ratings[i]['name']] = float(re.findall(dict_ratings[i]['pattern'], j)[0])
				except:
					pass
			try:
				log_obj['imdbVotes'] = int(movie_meta['imdbVotes'].replace(',', ''))
			except:
				pass
			try:
				log_obj['duration'] = int(re.findall(r'(\d+)', movie_meta['Runtime'])[0]) * 60
			except:
				pass
			log_obj['year'] = movie_meta['Year']
			nomination_text = movie_meta['Awards']
			log_obj['specialNominations'] = 'None'
			log_obj['noOfNominations'] = 0
			log_obj['noOfAwards'] = 0
			if 'nominated for' in nomination_text.lower():

				for (value,nomination) in re.findall(r'(\d+?)\s([a-zA-Z\s]+)', nomination_text, re.IGNORECASE):
					if not('nomination' in nomination or 'win' in nomination):
						log_obj['specialNominations'] += f'{value}:{nomination};'
			if 'nomination' in nomination_text:
				log_obj['noOfNominations'] = int(re.findall(r'(\d+) nomination', nomination_text, re.IGNORECASE)[0])
			if 'win' in nomination_text:
				log_obj['noOfAwards'] = int(re.findall(r'(\d+) win', nomination_text, re.IGNORECASE)[0])
			for i in movie_meta['Genre'].split(','):
				log_obj[i.replace(' ', '').replace('-', '')] = 1
			log_obj['directors'] = movie_meta['Director'].replace(",", '-')
			log_obj['writers'] = movie_meta['Writer'].replace(",", '-')
			log_obj['actors'] = movie_meta['Actors'].replace(",", '-')
			log_obj['country'] = movie_meta['Country'].replace(",", '-')
			log_obj['language'] = movie_meta['Language'].replace(",", '-')
			log_obj['Plot'] = movie_meta['Plot'].replace(",", '-')
			log_obj['Type'] = movie_meta['Type'].replace(",", '-')
			log_obj['Rated'] = movie_meta['Rated'].replace(",", '-')
			log_obj['Genre'] = movie_meta['Genre'].replace(",", '-')
			try:
				log_obj['totalSeasons'] = int(movie_meta['totalSeasons'])
			except:
				pass
			return (compile_meta_show(**log_obj),None)
	except ConnectionError as err:
		return (None, 'Connection Error')
	except Exception as err:
		raise err
		return (None,'Unknown error encountered')