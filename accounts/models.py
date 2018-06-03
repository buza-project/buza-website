from django.db import models
from django.conf import settings
from boards.models import Board

# Models will be added to the db


class Profile(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL, related_name='user_profile',
		on_delete=models.CASCADE)  # there is a 1-1 relation btn users and profile
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
	school = models.CharField(blank=True, null=True, max_length=100)
	interests = models.CharField(blank=True, null=True, max_length=300)
	# users can pick from a range of topics
	bio = models.CharField(blank=True, null=True, max_length=250)
	grade = models.IntegerField(blank=True, default=7)
	reputation = models.IntegerField(blank=True, default=0)

	# users can have multiple boards
	boards = models.ManyToManyField(Board, related_name="my_boards")

	def __str__(self):
		return 'Profile for user {}'.format(self.user)

