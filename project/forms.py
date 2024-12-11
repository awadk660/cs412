from ast import arg
from .models import *
from django import forms

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'age', 'height', 'weight', 'gender', 'fitness_goal']


class CreateWorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['type', 'date']
        widgets = {
            'date': forms.DateInput(
                    attrs={
                        'class': 'form-control',
                        'type': 'date',
                    }
                ),
        }

class CreateExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'sets', 'reps', 'weight', 'distance', 'time']
        widgets = {
            'time': forms.TextInput(attrs={
                'placeholder': 'HH:MM:SS (e.g., 00:10:00 for 10 minutes)'
            }),
        }
    def __init__(self, *args, **kwargs):
        # to initialize the right type of inputs based on workout type
        self.workout_type = kwargs.pop('workout_type', None)
        print("WORKOUT TYPE", self.workout_type)
        super(CreateExerciseForm, self).__init__(*args, **kwargs)

        if self.workout_type == 'strength':
            # Show only strength-related fields
            self.fields['distance'].widget = forms.HiddenInput()
            self.fields['time'].widget = forms.HiddenInput()
            self.fields['distance'].required = False
            self.fields['time'].required = False
        elif self.workout_type == 'cardio':
            # Show only cardio-related fields
            self.fields['reps'].widget = forms.HiddenInput()
            self.fields['sets'].widget = forms.HiddenInput()
            self.fields['weight'].widget = forms.HiddenInput()
            self.fields['reps'].required = False
            self.fields['sets'].required = False
            self.fields['weight'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        if self.workout_type == 'strength':
            reps = cleaned_data.get('reps')
            sets = cleaned_data.get('sets')
            weight = cleaned_data.get('weight')

            if reps is None or sets is None or weight is None:
                raise forms.ValidationError("Strength exercises must have reps, sets, and weight.")
            if reps <= 0 or sets <= 0 or weight <= 0:
                raise forms.ValidationError("Reps, sets, and weight must be positive numbers.")
        elif self.workout_type == 'cardio':
            distance = cleaned_data.get('distance')
            time = cleaned_data.get('time')
            if distance is None or time is None:
                raise forms.ValidationError("Cardio exercises must have distance and duration.")
            if distance <= 0:
                raise forms.ValidationError("Distance must be a positive number.")
            if time.total_seconds() <= 0:
                raise forms.ValidationError("Duration must be a positive time.")
        return cleaned_data

class CreateMealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['date', 'meal_type', 'calories', 'description']
        widgets = {
            'date': forms.DateInput(
                    attrs={
                        'class': 'form-control',
                        'type': 'date',
                    }
                ),
        }


