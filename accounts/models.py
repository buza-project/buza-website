from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

#Models will be added to the db

class Profile(models.Model):
	author_id = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_profile') #there is a 1-1 relation btn users and profile
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
	school= models.CharField(blank=True, null=True, max_length=100)
	interests = models.CharField(blank=True, null=True, max_length=300)	#users can pick from a range of topics
	bio = models.CharField(blank=True, null=True, max_length=250)
	grade = models.IntegerField(blank=True, default=7)
	reputation= models.IntegerField(blank=True, default=0)
	def __str__(self):
		return 'Profile for username {}'.format(self.user.username)
