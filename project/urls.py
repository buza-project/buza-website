"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


from boards import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # users
    # url(r'^', account_views.user_login, name='user_login'),
    url(r'^account/', include('accounts.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),

    # boards
    # url(r'^$', views.home, name='home'),
    url(r'^questions/(?P<subject>\d+)/$', views.board_questions_view,
        name='board_questions'),
    url(r'^question/(?P<id>\d+)/(?P<slug>\d+)/$', views.question_view,
        name='board_questions'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
