from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('mypage', views.mypage, name='mypage'),
    path('activate/<str:token>', views.email_auth, name='email_auth'),

    
    path('test', views.test, name='test'),
]
