import django.contrib.auth.urls
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from buza import views


urlpatterns = [

    # social-auth-app-django
    path(r'^login/', include('social_django.urls', namespace='social')),

    url(r'about/privacy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    url(r'about/tos/', views.TermsOfService.as_view(), name='terms-of-service'),
    # Django auth
    path('auth/', include(django.contrib.auth.urls)),

    path('', views.HomePageView.as_view(), name='home'),

    # user related paths
    url(r'^register/$', views.register, name='register'),
    path(r'users/<int:pk>/update/', views.UserUpdate.as_view(), name='user-update'),
    path(r'users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),

    # subject related paths
    path('subjects/<int:pk>/', views.SubjectDetail.as_view(), name='subject-detail'),

    # question related paths
    path('questions/', views.QuestionList.as_view(), name='question-list'),
    path('questions/<int:pk>/', views.QuestionDetail.as_view(), name='question-detail'),
    path(
        'questions/<int:subject_pk>/ask/',
        views.QuestionCreate.as_view(),
        name='question-create',
    ),
    path(
        'questions/<int:pk>/edit/',
        views.QuestionUpdate.as_view(),
        name='question-update',
    ),

    # answer related paths
    path(
        'answers/<int:pk>/edit/',
        views.AnswerUpdate.as_view(),
        name='answer-update',
    ),
    path(
        'questions/<int:question_pk>/answer/',
        views.AnswerCreate.as_view(),
        name='answer-create',
    ),
    # Django admin
    url(r'^admin/', admin.site.urls),

]
