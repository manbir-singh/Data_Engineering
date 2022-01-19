# Data_Engineering

Google Sheets Movie Recommender Data Pipeline (ETL)


This project aims to recommend movies based on a shared watch list on google sheets, containing the movie title and year. From there a recommender system was created following Datacamp's tutorial. The functionality of this recommender was extended to allow recommendations for new movies. Furthermore, a Movie Class was created using object oriented programming (OOP) to transform the movie data by adding more detailed metadata using the requests library and TMDB API. Afterwards the movies are loaded into the recommender function, which were then loaded into SQLite (a relational database management system) (in progress). Automation via Apache Airflow coming soon!


DEPENDENCIES:
1. gspread
2. pandas
3. numpy
4. requests
5. sqlalchemy
6. sqlite3
7. datetime
8. config (.py file containing api credentials for google sheets api and TMDB api, not uploaded here for security/privacy reasons)
9. credentials (.json file containing private key for the google sheets data, also not upload here)
10. TfidVectorizer from sklearn.feature_extraction.text
11. linear_kernel from sklearn.metrics.pairwise
12. CountVectorizer from sklearn.feature_extraction.text
13. cosine_similarity from sklearn.metrics.pairwise
14. literal_eval from ast
15. Movie Dataset for Recommender (https://www.kaggle.com/rounakbanik/the-movies-dataset)
 


DETAILS:

EXTRACT:
The google sheets data was extracted into a pandas DataFrame which had columns for movie title and year using the gspread api and requests package.
The Datacamp recommender movie system bases its movie recommendations on a folder of CSV files containing movie, keywords, and cast and crew details.
With that being said, this recommender can only recommend movies within the CSV file, and not new movies as an error will occur.

TRANSFORM:
Therefore we needed to combine the google sheets data with the pandas DataFrame that holds movie dataset CSV files.
In order to do so, the google sheets data needs to be transformed to include the same level of detail that the CSV files have and that the recommender uses(id, title, overview, release_date, director, cast, crew, genres, keywords, soup).
This was done using the requests library with the TMDB api.
As a result the Movie Class was created, which takes in a movie title and year and returns a dictionary with the full movie details, ready to be merged with the Recommender's movie metadata DataFrame.

The google sheets data was fed into the Movie Class, in which the returned dictionaries were appeneded into a metadata_df DataFrame in main.py, and finally merged with the Recommender's metadata DataFrame.
Then the Recommender's metadata with the google sheets movies were fed into the recommender function to return recommended movies
We have finally extended the use of Datacamps limited recommender system!
Furthermore the recommended movies were added as a column to the main metadata_df.

LOAD:
Finally, the metadata_df in main.py was loaded into a SQLite database using sqlalchemy.
SQL queries were used to Create the table in the database and then insert the data into the table (in progress, there is a syntax error when inserting data that I cannot seem to fix).


NOTES:
The movie class can be used standalone as an extension of the TMDB api, to retrieve complete movie data, and is stored into a pandas dataframe.

Although it was out of the scope for this project, the recommender function can also be extended even more by creating a movie object that is neither in the google sheets or the recommender's CSV to ultimately recommend ANY movie. You can simply take a movie title and year, create the movie object run the recommender's attributes and functions in main.py to append to the CSV metadata dataframe. Then run the recommender function to get the new titles recommended movie. I was unable to run the function more than once due to a lack of ram on my device. 
