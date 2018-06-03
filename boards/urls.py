from django.conf.urls import url
# from django.contrib.auth import authenticate, login, logout

from . import views

urlpatterns = [
	url(r'^questions/$', views.all_questions, name='all_questions'),
	url(r'^all/$', views.all_boards, name='all_boards'),
	url(r'^my-subjects/$', views.my_boards, name='my_boards'),
	url(r'^users/$', views.all_users, name='users'),
	url(r'^ask-question/$', views.ask_question, name='ask_question'),
	url(r'^edit/(?P<question_id>\d+)/(?P<question_slug>[\-\w]+)/$',
		views.edit_question, name='edit_question'),
	url(r'^(?P<board_name>[\w|\W]+)/(?P<question_id>\d+)/(?P<question_slug>[\-\w]+)/$',
		views.view_question, name='view_question'),
	url(r'^(?P<question_id>\d+)/(?P<question_slug>[\-\w]+)/$',
		views.view_question, name='view_question'),

	url(r'^(?P<board_name>[\w|\W]+)/$', views.board_questions, name='board_questions'),
	url(r'^(?P<board_name>[\-\w]+)/$', views.board_questions, name='board_questions'),


	# url(r'^question/(?P<id>\d+)/(?P<slug>\d+)/$', views.question_view, name='board_questions'),
]
