# mini_fb/views.py
# description: write view functions to handle URL requests for the mini_fb app

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class ShowAllProfilesView(ListView):
    template_name = 'mini_fb/show_all_profiles.html'
    model = Profile
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    '''Display 1 profile'''
    model = Profile
    template_name="mini_fb/show_profile.html"
    context_object_name = "profile"

    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')

class CreateProfileView(CreateView, LoginRequiredMixin):
    template_name="mini_fb/create_profile_form.html"
    form_class = CreateProfileForm
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            form.instance.user = user
            form.save()
            result = super().form_valid(form)
            login(self.request, user)
            return result

    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        return self.object.get_absolute_url()

class CreateStatusMessageView(CreateView, LoginRequiredMixin):
    template_name="mini_fb/create_status_form.html"
    form_class = CreateStatusMessageForm
    model = StatusMessage

    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')

    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.profile = profile
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.request.user.profile.pk})
    
class UpdateProfileView(UpdateView, LoginRequiredMixin):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
            

class DeleteStatusMessageView(DeleteView, LoginRequiredMixin):
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status_message"

    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')

    def get_success_url(self):
        profile = self.object.profile
        return reverse('show_profile', kwargs={'pk':profile.pk})

class UpdateStatusMessageView(UpdateView, LoginRequiredMixin):
    model = StatusMessage
    template_name= "mini_fb/update_status_form.html"
    context_object_name = "status_message"
    form_class = CreateStatusMessageForm

    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')

    def get_success_url(self):
        profile = self.object.profile
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
class CreateFriendView(View, LoginRequiredMixin):

    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        other_pk = self.kwargs['other_pk']
        
        other_profile = get_object_or_404(Profile, pk=other_pk)

        profile.add_friend(other=other_profile)
        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(ListView):
    '''Display friend suggestions for a profile'''
    model = Profile
    template_name="mini_fb/friend_suggestions.html"
    context_object_name="friend_suggestions"

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return profile.get_friend_suggestions()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user)
        return context


class ShowNewsFeedView(ListView, LoginRequiredMixin):
    model = StatusMessage
    template_name="mini_fb/news_feed.html"
    context_object_name = "news_feed"

    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return profile.get_news_feed()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user)
        return context


