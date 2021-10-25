# Data_Engineering

Google Sheets Movie Recommender ETL Pipeline


This project aims to recommened movies based on a shared watch list on google sheets, containing the movie title and year. From there a recommender system was created following Datacamp's tutorial. Afterwards the movies are loaded into the recommender function, which were then loaded into SQLite (a relational database managment system) (in progress). Automation via Apache Airflow coming soon!


DEPENDENCIES:
1. gspread
2. pandas
3. numpy
4. sqlalchemy
5. sqlite3
6. datetime
7. config (.py file containing api credentials for google sheets api and TMDB api, not uploaded here for security/privacy reasons)
8. credentials (.json file containing private key for the google sheets data, also not upload here)
9. TfidVectorizer from sklearn.feature_extraction.text
10. linear_kernel from sklearn.metrics.pairwise
11. CountVectorizer from sklearn.feature_extraction.text
12. cosine_similarity from sklearn.metrics.pairwise
13. literal_eval from ast
 

DETIALS:

The google sheets data was extracted into a pandas DataFrame which had columns for movie title and year.
The Datacamp recommender movie system bases its movie recommendations on a
