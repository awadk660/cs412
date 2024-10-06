# mini_fb/views.py
# description: write view functions to handle URL requests for the mini_fb app

from django.shortcuts import render, redirect
from .models import Profile
from django.views.generic import ListView

class ShowAllProfilesView(ListView):
    template_name = 'mini_fb/show_all_profiles.html'
    model = Profile
    context_object_name = 'profiles'