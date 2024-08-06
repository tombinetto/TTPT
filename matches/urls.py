# matches/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.match_list, name='match_list'),  # Maps the root URL of the matches app to the match_list view
]
