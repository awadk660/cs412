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
    
    def get_friends(self):
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)
        friendsList = [friend.profile2 for friend in friends_as_profile1] + [friend.profile1 for friend in friends_as_profile2]
        unique = list(set(friendsList)) # remove duplicate friends
        return unique
    
    def get_friend_suggestions(self):
        all_profiles = Profile.objects.exclude(pk=self.pk)
        currfriends = self.get_friends()
        suggestions = all_profiles.exclude(pk__in=[friend.pk for friend in currfriends])
        return suggestions.order_by('?')[:5] # randomize the queryset and pick the first 5

    
    def add_friend(self, other):
        if self == other:
            return

        if Friend.objects.filter(profile1=self, profile2=other).exists() or Friend.objects.filter(profile1=other, profile2=self).exists():
            return "already friends"
        
        Friend.objects.create(profile1 = self, profile2 = other)
    
    def get_news_feed(self):
        news_feed = []
        own_status_messages = StatusMessage.objects.filter(profile=self)
        news_feed += own_status_messages

        friends = self.get_friends()
        for friend in friends:
            friend_status_messages = StatusMessage.objects.filter(profile=friend)
            news_feed += friend_status_messages
        
        news_feed = sorted(news_feed, key=lambda x: x.timestamp, reverse=True) #sort it by timestamp

        return news_feed


class StatusMessage(models.Model):
    '''StatusMessage Object'''
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        '''Return the string representation of this message.'''
        return f'{self.message}'
    
    def get_images(self):
        '''Returns all images associated with the status message'''
        return Image.objects.filter(status_message = self)

class Image(models.Model):
    '''Image Object'''
    file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)

    def __str__(self):
        '''Return the string representation of this image.'''
        return f'Image for {self.status_message} uploaded at {self.timestamp}'

class Friend(models.Model):
    '''Friend Object Model'''
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Returns string representation of friendship'''
        return f'{self.profile1} & {self.profile2}'