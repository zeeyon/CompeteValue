from django.urls import path
from . import views

#urlpatterns = += 

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('activate/<str:token>', views.email_auth, name='email_auth'),

    path('mypage/<str:user_name>', views.mypage, name='mypage'),    
    path('setting/profile', views.set_profile, name='set_profile'),
    path('setting/account', views.set_account, name='set_account'),
    path('setting/password', views.set_password, name='set_password'),
    #path('setting/', views.setting, name='setting'),
    path('test', views.test, name='test'),
]

