from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # index 
    path('create/', views.create, name='create'), # create.html
    path('post/<int:post_id>', views.post, name='post'), # post.html
    path('update/', views.update, name='update'), # update.html
    path('postcreate/', views.postcreate, name='postcreate'), # create 함수
    path('postupdate/<int:post_id>', views.postupdate, name='postupdate'), # update 함수
    path('postdelete/<int:post_id>', views.postdelete, name='postdelete'), # delete 함수
]
