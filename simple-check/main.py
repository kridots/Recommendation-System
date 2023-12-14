import numpy as np
import pandas as pd
import json
import ast
from  helpfunc import Helpful_func_movies as fltr
from sklearn.feature_extraction.text import CountVectorizer   #It is used to transform given text into vector
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer as ps
import pickle
import os

class MakeDirectory:
    def __init__(self):
        try:
            # Directory 
            directory1 = "picklebooks"
            directory2 = "picklemovie"
            
            # Parent Directory path 
            parent_dir = "../"
            # parent_dir = "../"
            
            # Path 
            path1 = os.path.join(parent_dir, directory1) 
            path2 = os.path.join(parent_dir, directory2) 
            
            # Create the directory 
            # 'GeeksForGeeks' in 
            # '/home / User / Documents' 
            os.mkdir(path1)
            os.mkdir(path2)
            print("Directory '% s' created" % directory1)
            print("Directory '% s' created" % directory2)
        except Exception as e:
            print("Error:>",e)

MakeDirectory()

class Movie_Recommend:
    def __init__(self):
        try:
            self.credits_df = pd.read_csv('data/movies/credits.csv')
            self.movies_df = pd.read_csv('data/movies/movies.csv')
            self.new_movie_df = self.movies_df.merge(self.credits_df, on='title')
            self.movies_df = self.movies_df.merge(self.credits_df, on='title')
            self.movies_df = self.movies_df[['movie_id','title','overview','genres','keywords','cast','crew']]
        except Exception as e:
            print("Error1:>", e)

    def data_prep(self):
        try:
            self.movies_df.dropna(inplace=True)
            self.movies_df['genres'] = self.movies_df['genres'].apply(lambda x: fltr.convert(x))
            self.movies_df['keywords'] = self.movies_df['keywords'].apply(lambda x: fltr.convert(x))
            self.movies_df['cast'] = self.movies_df['cast'].apply(lambda x: fltr.convert3(x))
            self.movies_df['crew'] = self.movies_df['crew'].apply(lambda x: fltr.fetch_director(x))
            self.movies_df['overview'] = self.movies_df['overview'].apply(lambda x:x.split())
            self.movies_df['genres'] = self.movies_df['genres'].apply(lambda x: [i.replace(' ','') for i in x])
            self.movies_df['keywords'] = self.movies_df['keywords'].apply(lambda x: [i.replace(' ','') for i in x])
            self.movies_df['cast'] = self.movies_df['cast'].apply(lambda x: [i.replace(' ','') for i in x])
            self.movies_df['crew'] = self.movies_df['crew'].apply(lambda x: [i.replace(' ','') for i in x])
            self.movies_df['tags'] = self.movies_df['overview']+self.movies_df['genres']+self.movies_df['keywords']+self.movies_df['cast']+self.movies_df['crew']
            self.new_df = self.movies_df[['movie_id','title','tags']]
            self.new_df['tags'] = self.new_df['tags'].apply(lambda x: ' '.join(x))
            self.new_df['tags'] = self.new_df['tags'].apply(lambda X:X.lower())
            cv = CountVectorizer(max_features= 5000, stop_words='english')
            vectors = cv.fit_transform(self.new_df['tags']).toarray()
            # print(vectors[0])
            self.new_df['tags'] = self.new_df['tags'].apply(fltr.stem)
            self.similarity = cosine_similarity(vectors)

        except Exception as e:
            print("Error2:>",e)
    
    
    # def model_perform(self):
        # try:
            
            # similarity = cosine_similarity(vectors)
            # enumerate converts data collection obj into enumerate obj that return obj contain counter as key for each value of obj
            # print(sorted(list(enumerate(similarity[0])), reverse=True, key=lambda x: x[1])[1:6])
        # except Exception as e:
        #     print("Error3:>",e)

    def pickle_create(self):
        try:
            pickle.dump(self.new_df, open('../picklemovie/new_df.pkl','wb'))
            pickle.dump(self.similarity, open('../picklemovie/similarity_scores.pkl','wb'))
            pickle.dump(self.new_movie_df, open('../picklemovie/new_movie_df.pkl','wb'))

        except Exception as e:
            print("Error:>",e)


movie_cheaker = Movie_Recommend()
movie_cheaker.data_prep()
# movie_cheaker.model_perform()
movie_cheaker.pickle_create()

class Book_Recommand:

    def __init__(self):
        self.books = pd.read_csv('data/archive/Books.csv', low_memory=False)
        self.users = pd.read_csv('data/archive/Users.csv', low_memory=False)
        self.ratings = pd.read_csv('data/archive/Ratings.csv', low_memory=False)

    def popularity_data_prep(self):
        try:
            self.ratings_with_name = self.ratings.merge(self.books, on='ISBN')
            num_rating_df = self.ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
            num_rating_df.rename(columns={'Book-Rating': 'num_ratings'}, inplace=True)
            avg_rating_df = self.ratings_with_name.groupby('Book-Title')['Book-Rating'].mean().reset_index()
            avg_rating_df.rename(columns={'Book-Rating': 'avg_rating'}, inplace=True)
            popularity_df = num_rating_df.merge(avg_rating_df, on='Book-Title')
            popularity_df = popularity_df[popularity_df['num_ratings'] >= 250].sort_values('avg_rating', ascending=False).head(50)
            self.popularity_df =  popularity_df.merge(self.books, on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Image-URL-M','num_ratings','avg_rating']]
            print(self.popularity_df)
        except Exception as e:
            print("Book-Error:>",e)

    def collaborative_data_prep(self):
        
        try:
            # Filtering User who has rated 200 or more book
            x = self.ratings_with_name.groupby('User-ID').count()['Book-Rating'] > 200
            padhe_likh_users = x[x].index
            filtered_rating = self.ratings_with_name[self.ratings_with_name['User-ID'].isin(padhe_likh_users)]
            y = filtered_rating.groupby('Book-Title').count()['Book-Rating'] >= 50
            famous_books = y[y].index
            final_ratings = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]
            self.pt = final_ratings.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
            self.pt.fillna(0, inplace=True)
            self.similarity_scores = cosine_similarity(self.pt)

        except Exception as e:
            print("Book-Error:>",e)

    def pickle_create(self):
        try:
            pickle.dump(self.popularity_df, open('../picklebooks/popular.pkl','wb'))
            pickle.dump(self.pt, open('../picklebooks/pt.pkl','wb'))
            pickle.dump(self.books, open('../picklebooks/books.pkl','wb'))
            pickle.dump(self.similarity_scores, open('../picklebooks/similarity_book.pkl','wb'))
            pickle.dump(self.ratings_with_name, open('../picklebooks/ratingwithname.pkl','wb'))

        except Exception as e:
            print("Error:>",e)

book_checker = Book_Recommand()
book_checker.popularity_data_prep()
book_checker.collaborative_data_prep()
book_checker.pickle_create()

