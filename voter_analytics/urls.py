## mini_fb/urls.py
## description: URL patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from . import views
from .views import *

# all of the URLs that are part of this app
urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
        path('graphs/', GraphsView.as_view(), name='graphs'),
]
