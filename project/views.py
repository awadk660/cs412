from ast import List
from threading import local
import time
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from datetime import datetime
from pytz import timezone
from django.utils.timezone import localdate, now
import plotly
import plotly.express as px
import pandas as pd
from collections import defaultdict

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile', pk=request.user.pk)
        return redirect('login')

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.project_profile
        workouts = Workout.objects.filter(user=request.user).order_by('-date')
        meals = Meal.objects.filter(user=request.user).order_by('-date')
        today = localdate()
        print("TODAY", today)
        today_workouts = workouts.filter(date=today)
        today_meals = meals.filter(date=today)
        # meals = meals[:4]
        fitness_goal = profile.fitness_goal
        daily_calorie_goal = 2000
        if fitness_goal == "Lose Weight":
            daily_calorie_goal = 1800
        elif fitness_goal == "Maintain Weight":
            daily_calorie_goal = 2400
        elif fitness_goal == "Gain Weight":
            daily_calorie_goal = 3000
        total_calories_today = 0
        for meal in today_meals:
            total_calories_today += meal.calories
        workouts = workouts[:4]
        context = {
            'user': request.user,
            'workouts': workouts,
            'meals': meals,
            'today_workouts': today_workouts,
            'today_meals': today_meals,
            'daily_calorie_goal': daily_calorie_goal,
            'total_calories_today': total_calories_today,
        }
        return render(request, template_name='project/profile.html', context=context)

class CreateUserView(CreateView, LoginRequiredMixin):
    template_name="project/create_user_form.html"
    form_class = CreateUserForm
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
        return reverse('profile', kwargs={'pk': self.object.user.pk})

class CreateWorkout(CreateView, LoginRequiredMixin):
    template_name="project/create_workout.html"
    form_class = CreateWorkoutForm
    model = Workout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['user_form'] = CreateWorkoutForm()
        return context

    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        form.instance.user = user
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect to the user's profile after successful form submission
        return reverse('profile', kwargs={'pk': self.object.user.pk})
    
class ViewWorkout(LoginRequiredMixin, DetailView):
    model = Workout
    template_name = "project/view_workout.html"
    context_object_name = "workout"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercises'] = Exercise.objects.filter(workout=self.object)
        return context
    
class CreateExercise(LoginRequiredMixin, CreateView):
    template_name="project/create_exercise.html"
    form_class = CreateExerciseForm
    model = Exercise

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        workout = get_object_or_404(Workout, pk=self.kwargs['pk'], user=self.request.user)
        kwargs['workout_type'] = workout.type  # Pass workout type to the form
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workout'] = get_object_or_404(Workout, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        workout = get_object_or_404(Workout, pk=self.kwargs['pk'])
        print("ASSOCIATED WORKOUT", workout)
        form.instance.workout = workout
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        return reverse('view_workout', kwargs={'pk': self.object.workout.pk})
    
class CreateMeal(LoginRequiredMixin, CreateView):
    template_name="project/create_meal.html"
    form_class = CreateMealForm
    model = Meal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = CreateMealForm()
        return context

    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        form.instance.user = user
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect to the user's profile after successful form submission
        return reverse('profile', kwargs={'pk': self.object.user.pk})
    
class GraphsView(View):
    template_name = "project/graphs.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = {}

        workouts = Workout.objects.filter(user=user).order_by('-date')
        cardio_exercises = Exercise.objects.filter(workout__in=workouts, workout__type='cardio').order_by('workout__date')
        strength_exercises = Exercise.objects.filter(workout__in=workouts, workout__type='strength').order_by('workout__date')
        if cardio_exercises.exists():
            cardio_data = []
            for exercise in cardio_exercises:
                if exercise.time and exercise.distance:
                    pace = float(exercise.distance) / exercise.time.total_seconds() * 3600  # Normalize to pace (e.g., km/h)
                    cardio_data.append({'date': exercise.workout.date, 'pace': pace})
            cardio_df = pd.DataFrame(cardio_data)
            fig1 = px.line(cardio_df, x='date', y='pace', title="Cardio Pace Over Time", labels={'pace': 'Pace (mph)'})
            context['CardioGraph'] = plotly.offline.plot(fig1, auto_open=False, output_type='div')
        
        if strength_exercises.exists():
            strength_data = []
            for exercise in strength_exercises:
                if exercise.weight and exercise.sets and exercise.reps:
                    total_weight = exercise.weight * exercise.sets * exercise.reps
                    strength_data.append({'date': exercise.workout.date, 'total_weight': total_weight})
            strength_df = pd.DataFrame(strength_data)
            fig2 = px.bar(strength_df, x='date', y='total_weight', title="Strength Training: Total Weight Lifted Over Time")
            context['StrengthGraph'] = plotly.offline.plot(fig2, auto_open=False, output_type='div')

        context['longest_streak'] = self.calculate_longest_streak(workouts)
        context['calorie_goal_days'] = self.calculate_calorie_goal_days(user)
        context['most_weight_lifted'] = max(
            [exercise.weight * exercise.sets * exercise.reps for exercise in strength_exercises if exercise.weight and exercise.sets and exercise.reps], 
            default=0
        )

        return context
    
    def calculate_longest_streak(self, workouts):
        dates = sorted(workouts.values_list('date', flat=True))
        longest_streak = 0
        current_streak = 1

        for i in range(1, len(dates)):
            if (dates[i] - dates[i - 1]).days == 1:
                current_streak += 1
            else:
                longest_streak = max(longest_streak, current_streak)
                current_streak = 1

        return max(longest_streak, current_streak)

    def calculate_calorie_goal_days(self, user):
        '''calculate the total amount of days the user met their calorie goals'''
        fitness_goal = user.project_profile.fitness_goal
        calorie_goal = {
            "Lose Weight": 1800,
            "Maintain Weight": 2400,
            "Gain Weight": 3000,
        }.get(fitness_goal, 2000)
        meals = Meal.objects.filter(user=user)
        print("MEALSSSS",meals)
        meals_by_day = defaultdict(list)
        for meal in meals:
            meals_by_day[meal.date].append(meal)
        total = 0
        for day, day_meals in meals_by_day.items():
            total_calories = sum(meal.calories for meal in day_meals)
            if total_calories >= calorie_goal:
                total += 1
        return total


    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

class ViewAllWorkouts(ListView):
    model = Workout
    template_name = "project/all_workouts.html"
    context_object_name = "workouts"
    paginate_by = 20

    def get_queryset(self):
        '''Return all workouts ordered by date.'''
        return Workout.objects.all().order_by('-date')