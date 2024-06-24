Project Name: 
--Movie Recommendation System

Project Description;
Movie Recommendation System is a Data Science/Web Application Project;
Data Science constitutes about 30% of the project and Web Application constitutes about 70% of the project.

Project Aim: 
Over the time, as someone who loves to watch movies both alone and in cinemas, i've gotten to discover two features that could be great and aid movie productivity both personally(for users) and commercially(for cinemas) when made available, those two features are;
1. Ability to get similar movies for a previously watched movie;
Supposing i watched a very nice and interesting movie recently, what if i could get the names of the movies similar to the watched one and later get to watch them at my preferred choice?, How nice would it be?, 
With this feature i'll be able to watch movies of same genre again and keep on with the interesting/nice feeling i got from watching the first movie with the subsequent ones.
With this feature, Cinemas can keep showing nice & interesting movies for customers which will in turn promote business.
2. Ability to have a personal account that keeps track and learn of the names of movies a user has made similar recommendations for over history, with this the user will be able to get movie recommendations based on his previous movie recommendation history.

How the project works(Externally);
1. To use the web application for the first time, a user has to create an account on the account creation page.
2. When a user creates an account on the web application, he gets redirected to the home page, on the homepage the new user will see nothing other than a link that gets him to the recommender page.
3. When a user clicks gets to the recommender page, he is provided with a form that allows him to specify movie parameters which will be used in prediction of similar movies for the user; those movie parameters are..
I. Movie Name
AND
II. Movie Type, application supports 7 different movie types; which are;
a.Hollywood
b.Bollywood
c.British movies
d.Thai Movies
e.Chinese Movies
f.Nollywood 
g.TV Shows
4. When a user enters a movie and selects a movie type and click on the proceed button, the recommendation process is sent into action, after successful recommendation process, the user will be provided with movies similar to the entered one, and also the parameters of each recommended movies will also be provided along with it. Those parameters are.
a. Plot
b. Genre
c. IMDB Rating
d. Poster Picture
5. After a user makes a recommendation, the home page of that user's account would no longer be empty, rather it will contain movie recommendations for that user, which will be based on previous recommendation requests made by the user on the recommender page.


Technological Fields Adopted in Developing the Project
1. Web Scraping
The field was adopted for scrapping the movies data used in recommendation from the internet.

2. Data Science
The above was adopted for the following purposes;
1. Reading the scrapped movies data
2. Cleaning the scrapped movies data
3. Getting the needed features from the scrapped movies data

3. Web Application Development
This field is divided into two parts;
Frontend Development, this is the part a user will see on the web application
Backend Development, this is the part which contains codes that drives the frontend of the web application, which is hidden from the user

4. DevOps
This field adopted at the final stage of the project, known as web hosting.
The web hosting process was donw in order to make the project globally available to anyone with access to the internet.
The web hosting process involves the following process..
1. Getting a web hosting server;
2. Setting up the hosting server
3. Hosting the web application on the server;
4. Buying a domain for the web application;
5. Installing an ssl certificate for the web application


Technological tools employed in developing the project;
1. Python (Programming Language)
This is the major programming language that drives the data science and backend part of the project;
2. HTML (Markup Language)
3. CSS (Styling Language)
4. Bootstrap (CSS Framework)
5. Javascript (Programming Language)
6. ReactJS (Frontend Framework)
7. Django (Backend Framework)


How the web application works(Internally);
1. When the backend of the web application is started, the movies data are loaded and the appropriate data pre-processing are performed.
2. When a users enters a movie parameter(movie name and movie type)
3. A get requests is made from the frontend of the web application to the backend of the web application
4. When the backend recieves the get request which contains the movie name and movie type as its body, the backend starts the recommendation process
5. The first stage of the recommendation process involves getting the already processed data in step 1
6. After getting the processed data, it was passed to a function that performs movie querying based on what the user entered
7. In the movie querying function, the movie name and type specified by a user will be searched in two ways;
	a. Through a movie querier api, in case this one fails the we move on to the second way
	b. Through the processed training data passed to the invocation of the querier function
	..The api used is the tmdb search movie api, the documentation can be found on this link: https://developers.themoviedb.org/3/search/search-movies
	In case the movie could no be found through the api, The fallback method b works by performing complex string matching on each of the movies in the training dataset passed to the querier function. The complex matching operation was achieved with a python module called rapidfuzz
	At the end of the query, the tmdb id of the matched movie will be returned by the query function
8. After the query function is invoked and the tmdb id of the matched movie is returned by the function, the next function that was invoked is the fitting function, the fitting function does the actual recommendation operation, inside the fitting function a script that consumes an api is executed. This api is the tmdb recommendation api, the documentation can be found through this link; https://developers.themoviedb.org/3/movies/get-movie-recommendations
This api returns the list of movies similar to a specified movie name, after getting the list from the api, some processing operation has to be done, which are;
	a. Looping through each movie of the list
	b. Getting the tmdb id of the movie of a loop
	c. Converting the tmdb id to imdb id
	d. Saving the imdb id inside a predefined list
After the whole 4 processes, the new list which contains the imdb id of the recommended movies is returned by the fitting function.
9. At the end of everything, the list of the imdb ids of the recommended movies is returned to the frontend of the web application.
10. Inside the frontend of the web appilcation, the imdb ids are processed again in the following steps;
    a. For each imdb id in the list, the imdb get movie api is called, this api takes an imdb id of a movie and returns the whole movie details
    b. For each movie details returned, the needed parameters are extracted, which are;
       i. Movie Name
       ii. Movie Rating
       iii. Movie Genres
       iv. Movie Poster Image
11. Finally, by using the details extracted by the frontend of the web application, the recommended movies are rendered to the web browser for the end user to see.


Project Development Steps;
...Performing research on the project and how it can be achieved;
...Adopting a suitable algorithm for the Movie Recommendation objective;
		After series of researches, i discovered both the tmdb and imbd API, with these two application programming interfaces(APIs), i was able to adopt and implement different algorithms that made this project to be successful.
...Sourcing for data that would be used in training the adopted algorithm;]
		By using web scrapping libraries and tools of the python programming language, i was able to scrape training data used for this project; The below is a list of those web scrapping tools;
			i. Python Requests library; 
				This python library allow developers to make Http Requests with Python, with this library, i was able to make get requests to wikipedia page that host contents of all the hollywood, bollywood, nollywood , tc-shows, chinese movies, thai movies, british movies and k-dramas till date. 
			ii. Regular Expressions(regex)
				After making those http requests, i was able to parse through the content of those pages with another python tool known as regex(regular expressions). 
				After parsing out the movie names, i made series of get requests to the imdb movies search api, in order to get the parameters of each movies which i later complied together in a csv(Comma Separated Values) file.
...Training the developed built algorithm with the collected data;
		This stage is all about building the whole project, in this stage, different algorithms were written and tried with the data collected and the ones that worked best was finally chosen and used.
...Developing a backend for the web application of the project
		The backend of the web application was built with a python web framework known as Django. You can check the source code for more details.
...Developing a frontend for the web application of the project
		The backend of the web application was built with a javascript framework known as React JS. You can check the source code for more details.
...Deploying the whole project as a Web Application.
		This project was hosted on the heroku Paas (Pay as a service platform).
		The heroku platform provided us with a database known as Postgressql, which is a non-relational database, you can read more on it through this link; https://www.postgresql.org/about/
		The heroku platform also provided us with other utilities that makes our website to be accessible by anyone on the internet.
		You can read more on heroku with this link; https://en.wikipedia.org/wiki/Heroku
