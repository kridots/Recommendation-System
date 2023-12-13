import ast
from nltk.stem.porter import PorterStemmer

class Helpful_func_movies:
    ps = PorterStemmer()
    def __init__(self) -> None:
        pass

    @staticmethod
    def convert(obj):
        L=[]
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L
    
    @staticmethod
    def convert3(obj):
        L=[]
        counter=0
        for i in ast.literal_eval(obj):
            if counter != 3:
                L.append(i['name'])
                counter += 1
            else:
                break
        return L
    
    @staticmethod
    def fetch_director(obj):
        L=[]
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
        return L
    
    # @staticmethod
    # def stem(text):
    #     y=[]
    #     for i in text.split():
    #         y.append(ps.stem(i))
    #     return " ".join(y)
    @staticmethod
    def stem(text):
        y = [Helpful_func_movies.ps.stem(i) for i in text.split()]
        return " ".join(y)
    
