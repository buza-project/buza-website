import django.contrib.auth.urls
from django.conf.urls import url
from django.urls import include, path
from django.views import generic

import project.urls
from buza import views


urlpatterns = [
    path('', generic.RedirectView.as_view(pattern_name='questions'), name='home'),

    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
    path(r'users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),

    path('auth/', include(django.contrib.auth.urls)),

    # Fall back to older project urls.
    path('', include(project.urls)),  # TODO: Migrate
]
