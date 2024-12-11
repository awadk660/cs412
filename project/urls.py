from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home page that redirects based on login status
    path('', views.HomePageView.as_view(), name="home"),
    path('create_profile', views.CreateUserView.as_view(), name="create_user_form"),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),

    # Profile or dashboard
    path('profile/<int:pk>/', views.ProfileView.as_view(), name="profile"),

    # create a workout associated to profile pk
    path('profile/<int:pk>/create_workout/', views.CreateWorkout.as_view(),name="create_workout"),

    # get the detailed view of the workout including the exercises for that workout
    path('view_workout/<int:pk>/', views.ViewWorkout.as_view(), name='view_workout'),

    # create exercise and add it to workout
    path('workout/<int:pk>/add_exercise/', views.CreateExercise.as_view(), name='add_exercise'),

    # create a meal
    path('profile/<int:pk>/log_meal/', views.CreateMeal.as_view(), name='add_meal'),

    #view graphs with analytics
    path('profile/<int:pk>/graph/', views.GraphsView.as_view(), name='graphs'),

    #view all workouts
    path('profile/<int:pk>/all_workouts/', views.ViewAllWorkouts.as_view(), name='all_workouts'),
]
