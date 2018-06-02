from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
	# Register your models here.
	list_display = ['user', 'school', 'reputation']
admin.site.register(Profile, ProfileAdmin)
