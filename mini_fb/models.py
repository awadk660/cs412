# mini_fb/models.py
# Definte the data objects for our application
from django.db import models
from django.urls import reverse

class Profile(models.Model):
    '''Profile object'''

    # data attributes of an Article:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        statusMessages = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        return statusMessages
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})


class StatusMessage(models.Model):
    '''StatusMessage Object'''
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        '''Return the string representation of this message.'''
        return f'{self.message}'