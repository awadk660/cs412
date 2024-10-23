## mini_fb/urls.py
## description: URL patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', views.ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile', views.CreateProfileView.as_view(), name="create_profile_form"),
    path('profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
    path('profile/<int:pk>/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete/', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update/', views.UpdateStatusMessageView.as_view(), name='update_status'),

]