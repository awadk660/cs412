# mini_fb/views.py
# description: write view functions to handle URL requests for the mini_fb app

from django.shortcuts import render, redirect
from .models import Profile
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from django.urls import reverse

class ShowAllProfilesView(ListView):
    template_name = 'mini_fb/show_all_profiles.html'
    model = Profile
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    '''Display 1 profile'''
    model = Profile
    template_name="mini_fb/show_profile.html"
    context_object_name = "profile"

class CreateProfileView(CreateView):
    template_name="mini_fb/create_profile_form.html"
    form_class = CreateProfileForm
    model = Profile

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        return self.object.get_absolute_url()

class CreateStatusMessageView(CreateView):
    template_name="mini_fb/create_status_form.html"
    form_class = CreateStatusMessageForm
    model = StatusMessage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''method called after form is validated, but before saving to DB'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile

        return super().form_valid(form)
    
    def get_success_url(self):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse('show_profile', kwargs={'pk':profile.pk})