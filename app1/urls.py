from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('recommand/',views.content_recommand,name='content-recommand'),
    # path('newrecommand/',views.content_based_recommand,name='content_recommand'),
    path('collaborative/',views.collaborative_maker,name='collaborative-filter'),
    # path('collaborativerecommand/',views.collaborative_checker,name='collaborative_recommand'),
]