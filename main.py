import gspread
import pandas as pd
import sqlalchemy
import datetime
import _sqlite3
import config
import Movie
import Recommender

DATABASE_LOCATION = 'sqlite:///google_sheets_recommended_movies.sqlite'


# Extract

# Set time for automation
today = datetime.datetime.now()
last_week = today - datetime.timedelta(days=7)
last_week_unix_timestamp = int(last_week.timestamp()) * 1000

# Extracting movie data from google sheets
gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key(config.gspread['api_key'])
watchlist = sh.sheet1
record = pd.DataFrame(watchlist.get_all_records())

# Set print options to remove df ellipses
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# Transform

# List movie names to match into TMDB api to get matching names of movies and their details
movies_gspread = record[['Movie', 'Year']]

# Cleaning data to remove cells with empty strings
mask = ~movies_gspread.eq('').all(1)
movies_gspread = movies_gspread[mask]

metadata_df = pd.DataFrame()

for i in movies_gspread.iterrows():
    movie = str(i[1]['Movie'])
    year = str(i[1]['Year'])
    metadata = Movie.Movie(movie, year)
    metadata_df = metadata_df.append(metadata.df)

metadata_df = metadata_df.reset_index()

# Drop columns that are not needed in Recommender function
columns_to_drop = ['index', 'adult', 'backdrop_path', 'genre_ids', 'original_language',
                   'original_title', 'popularity', 'poster_path',
                   'video', 'vote_average', 'vote_count']
metadata_df = metadata_df.drop(columns_to_drop, axis=1)

# Import Recommender variables and functions to be used updated with google sheets data and new movie object movies
Recommender.metadata = Recommender.metadata.append(metadata_df, ignore_index=True).fillna('')

Recommender.metadata['soup'] = Recommender.metadata.apply(Recommender.create_soup, axis=1)

count_matrix = Recommender.count.fit_transform(Recommender.metadata['soup'])
cosine_sim2 = Recommender.cosine_similarity(count_matrix, count_matrix)

# Reset index of your main DataFrame and construct reverse mapping as before
Recommender.metadata = Recommender.metadata.reset_index()
indices = pd.Series(Recommender.metadata.index, index=Recommender.metadata['title'])

# Add reccc movies for metadata_df google movies
metadata_df['recommended_movies'] = metadata_df['title'].apply(
                                    lambda x: Recommender.get_recommendations(
                                        x, cosine_sim2, indices).values.tolist())

metadata_df['release_date'] = pd.to_datetime(metadata_df['release_date'])

# Load

engine = sqlalchemy.create_engine(DATABASE_LOCATION)
conn = _sqlite3.connect('google_sheets_recommended_movies.sqlite')
cursor = conn.cursor()

sql_query = """CREATE TABLE IF NOT EXISTS google_sheets_recommended_movies(
                id NUMERIC PRIMARY KEY,
                overview TEXT,
                release_date NUMERIC,
                title TEXT,
                director TEXT,
                cast TEXT,
                crew TEXT,
                genres TEXT,
                keywords TEXT,
                recommended_movies TEXT);
            """

cursor.execute(sql_query)
print('created table successfully')

sql = """INSERT INTO google_sheets_recommended_movies
        (id, overview, release_date, title, director, cast, crew, genres, keywords, recommended_movies)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""


for row in metadata_df.itertuples(index=False):
    cursor.execute(sql, (row.id, row.overview, row.release_date, row.title,
                         row.director, row.cast, row.crew, row.genres, row.keywords, row.recommended_movies))
    conn.commit()

print("Opened database successfully")

try:
    metadata_df.to_sql("google_sheets_recommended_movies", con=engine, index=False, if_exists='append')
except:
    print("Data already exists in the database")


conn.close()
print("Close database successfully")

# Job Scheduling coming soon
