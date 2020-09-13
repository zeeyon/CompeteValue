from django.urls import path
from . import views

urlpatterns = [
	path('signup', views.signup, name='signup'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name='logout'),
	path('mypage', views.mypage, name='mypage'),
	path('me', views.MyUserView.as_view(), name='my_user')
]
