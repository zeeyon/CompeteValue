from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # index
    path('<int:page>', views.index, name='index'), # index pagination
    path('post/<int:post_id>', views.post, name='post'), # post.html
    path('create/', views.create_post, name='create_post'), # create_post 함수
    path('update/<int:post_id>', views.update_post, name='update_post'), # update_post 함수
    path('delete/<int:post_id>', views.delete_post, name='delete_post'), # delete_post 함수
]
