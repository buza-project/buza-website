from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import include, path

import project.urls
from buza import views


urlpatterns = [
    # url(r'^login/$', views.user_login, name='login')
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
    path(r'users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.logged_out, name='logout'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(
        r'^password_change/done/$',
        views.password_change_done,
        name='password_change_done',
    ),

    url(
        r'^password_reset/$',
        auth_views.password_reset,
        {'template_name': 'registration/password_reset_form_user.html'},
        name='password_reset',
    ),
    url(
        r'^password_reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'registration/password_reset_done_index.html'},
        name='password_reset_done',
    ),
    url(
        r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm_user.html'},
        name='password_reset_confirm',
    ),
    url(
        r'^password-reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'registration/password_reset_complete_user.html'},
        name='password_reset_complete',
    ),

    # Fall back to older project urls.
    path('', include(project.urls)),  # TODO: Migrate
]
