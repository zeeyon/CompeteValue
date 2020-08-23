from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('mypage/<str:user_name>', views.mypage, name='mypage'),
    path('setting', views.setting, name='setting'),
    path('test', views.test, name='test'),
]
