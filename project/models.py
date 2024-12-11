# project/models.py
# Definte the data objects for our application
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Profile(models.Model):
    fitness_goals = [
        ('lose', 'Lose Weight'),
        ('maintain', 'Maintain Weight'),
        ('gain', 'Gain Weight'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    age = models.PositiveIntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    gender = models.TextField()
    fitness_goal = models.TextField(choices=fitness_goals)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile')

    def __str__(self):
        return self.name
    
class Workout(models.Model):
    workout_types = [
        ('cardio', 'Cardio'),
        ('strength', 'Strength'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    date = models.DateField()
    type = models.TextField(choices=workout_types)

    def __str__(self):
        return f"{self.user} - {self.date} - {self.type}"
    
class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    reps = models.PositiveIntegerField(null=True, blank=True)
    sets = models.PositiveIntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    distance = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Distance covered (e.g., km or miles)")
    time = models.DurationField(null=True, blank=True, help_text="Time spent (e.g., HH:MM:SS)")

    def __str__(self):
        return self.name
    
class Meal(models.Model):
    meal_types = [('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack')]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals')
    date = models.DateField()
    meal_type = models.TextField(choices=meal_types)
    calories = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} - {self.meal_type} {self.date}"
