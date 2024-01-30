from django.shortcuts import render, HttpResponse
import numpy as np
import pickle
import json
from django.contrib.auth.decorators import login_required

# Movies Pickle
new_df = pickle.load(open('picklemovie/new_df.pkl','rb'))
similarity_score = pickle.load(open('picklemovie/similarity_scores.pkl','rb'))
new_movie_df = pickle.load(open('picklemovie/new_movie_df.pkl','rb'))

# Books Pickel
popular_df = pickle.load(open('picklebooks/popular.pkl','rb'))
pt = pickle.load(open('picklebooks/pt.pkl','rb'))
books = pickle.load(open('picklebooks/books.pkl','rb'))
similarity_books = pickle.load(open('picklebooks/similarity_book.pkl','rb'))
ratings_with_name = pickle.load(open('picklebooks/ratingwithname.pkl','rb'))    


# Create your views here.
@login_required(login_url="/accounts/login/")
def index(request):
    new_list = []

    for ind, row in popular_df.iterrows():
       
        new_list.append({
                            'image_url': row['Image-URL-M'],
                            'title': row['Book-Title'],
                            'num_ratings': row['num_ratings'],
                        })
    # print(new_list)
    return render(request, 'index.html',{'data': new_list} )
    # return render(request, 'index.html', dict(movie_name = list(new_df['title'])[1:16]))

@login_required(login_url="/accounts/login/")
def content_recommand(request):
    try:
        if request.method == 'POST':
            new_list= None
            user_input = request.POST['user_input']

             # Check if user_input is not empty and exists in the 'title' column
            # if user_input and any(new_df['title'] == user_input):
            #     return render(request, 'recommand.html')
            
            # movie_index = new_df[new_df['title'] == user_input].index[0]
            index = new_df[new_df['title'].str.contains(user_input,case=False)]
            print('index',index)
            if len(index)==0:
                return render(request, 'recommand.html', {'data': new_list})
            movie_index = index.index[0]
            distance = similarity_score[movie_index]
            movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

            new_list = []
            #genres_list_per_movie = []  # List to store genres for each movie

            for i in movies_list:
                listing = new_movie_df[new_movie_df['id'] == new_df.iloc[i[0]].movie_id]
                for genres_json in listing.genres:
                    genres_list = json.loads(genres_json.replace("'", "\""))
                    names_at_index_0 = [genre["name"] for genre in genres_list]

            
                for spok_lang_json in listing.spoken_languages:
                    lang_json = json.loads(spok_lang_json.replace("'", "\""))
                    name_lang_index0 = [spok["name"] for spok in lang_json]
                    # print(name_lang_index0)
                
                new_list.append({
                    'title': new_df.iloc[i[0]].title, 'overview': new_movie_df.iloc[i[0]].overview,'genres': names_at_index_0, "release_Date": new_movie_df.iloc[i[0]].release_date,"Spoken_Language": name_lang_index0
                })
                # print(new_list)

            return render(request, 'recommand.html', {'data': new_list})

    except Exception as e:
        print("Error:>",e)
    return render(request,'recommand.html')


@login_required(login_url="/accounts/login/")
def collaborative_maker(request):
    new_list = []
    try:
        if request.method == 'POST':
            user_input = request.POST['user_input']
            index = np.where(pt.index == user_input)[0][0]
            similar_items = sorted(list(enumerate(similarity_books[index])), key=lambda x: x[1], reverse=True)[1:6]
            
            # data = []
            # filter_data2 = []
            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))
                
                 # Fetch ratings data based on exact match of 'Book-Title'
                ratings_data = ratings_with_name[ratings_with_name['Book-Title'].isin(temp_df['Book-Title'])]
                
                rating_counts = ratings_data.groupby('Book-Title')['Book-Rating'].count().reset_index()
                # filter_data2.append(rating_counts[i]['Book-Rating'])
                # print(rating_counts['Book-Rating'])
                item.extend(list(rating_counts['Book-Rating']))

                # data.append(item)
                new_list.append({
                    'title': item[0],
                    'author': item[1],
                    'image_url': item[2],
                    "rating": item[3]
                })

            # print(new_list)
            return render(request, 'books/collaborative.html', {'data': new_list})

    except Exception as e:
        print("Error:>",e)
    return render(request, 'books/collaborative.html')


# def content_based_recommand(request):
#     try:
#         if request.method == 'POST':
#             new_list= None
#             user_input = request.POST['user_input']

#              # Check if user_input is not empty and exists in the 'title' column
#             # if user_input and any(new_df['title'] == user_input):
#             #     return render(request, 'recommand.html')
            
#             movie_index = new_df[new_df['title'] == user_input].index[0]
#             distance = similarity_score[movie_index]
#             movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

#             new_list = []
#             genres_list_per_movie = []  # List to store genres for each movie

#             for i in movies_list:
#                 listing = new_movie_df[new_movie_df['id'] == new_df.iloc[i[0]].movie_id]
#                 for genres_json in listing.genres:
#                     genres_list = json.loads(genres_json.replace("'", "\""))
#                     names_at_index_0 = [genre["name"] for genre in genres_list]

            
#                 for spok_lang_json in listing.spoken_languages:
#                     lang_json = json.loads(spok_lang_json.replace("'", "\""))
#                     name_lang_index0 = [spok["name"] for spok in lang_json]
#                     # print(name_lang_index0)
                
#                 new_list.append({
#                     'title': new_df.iloc[i[0]].title, 'overview': new_movie_df.iloc[i[0]].overview,'genres': names_at_index_0, "release_Date": new_movie_df.iloc[i[0]].release_date,"Spoken_Language": name_lang_index0
#                 })
#                 # print(new_list)

#     except Exception as e:
#         print("Error:>",e)
#     return render(request, 'recommand.html', {'data': new_list})
#     # return render(request, 'recommand.html', {'data': data})


# def collaborative_checker(request):
    # new_list = []
    # try:
    #     if request.method == 'POST':
    #         user_input = request.POST['user_input']
    #         index = np.where(pt.index == user_input)[0][0]
    #         similar_items = sorted(list(enumerate(similarity_books[index])), key=lambda x: x[1], reverse=True)[1:6]
            
    #         # data = []
    #         # filter_data2 = []
    #         for i in similar_items:
    #             item = []
    #             temp_df = books[books['Book-Title'] == pt.index[i[0]]]
    #             item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
    #             item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
    #             item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))
                
    #              # Fetch ratings data based on exact match of 'Book-Title'
    #             ratings_data = ratings_with_name[ratings_with_name['Book-Title'].isin(temp_df['Book-Title'])]
                
    #             rating_counts = ratings_data.groupby('Book-Title')['Book-Rating'].count().reset_index()
    #             # filter_data2.append(rating_counts[i]['Book-Rating'])
    #             # print(rating_counts['Book-Rating'])
    #             item.extend(list(rating_counts['Book-Rating']))

    #             # data.append(item)
    #             new_list.append({
    #                 'title': item[0],
    #                 'author': item[1],
    #                 'image_url': item[2],
    #                 "rating": item[3]
    #             })

    #         print(new_list)

    # except Exception as e:
    #     print("Error:>",e)
    # return render(request, 'books/collaborative.html', {'data': new_list})