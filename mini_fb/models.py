# mini_fb/models.py
# Definte the data objects for our application
from django.db import models

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