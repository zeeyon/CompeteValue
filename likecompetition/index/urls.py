from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # index
    path('<int:page>', views.index, name='index'), # index pagination
    path('post/<int:post_id>', views.post, name='post'), # post.html
    path('create/post', views.create_post, name='create_post'), # create_post 함수
    path('update/post/<int:post_id>', views.update_post, name='update_post'), # update_post 함수
    path('delete/post/<int:post_id>', views.delete_post, name='delete_post'), # delete_post 함수
    path('delete/comment/<int:comment_id>', views.delete_comment, name='delete_comment'), # delete_post 함수
    path('scrap/', views.scrap, name='scrap'), # scrap한 post 조회
    path('create/scrap/<int:post_id>', views.create_scrap, name='create_scrap'), # create_scrap 함수
    path('delete/scrap/<int:scrap_id>', views.delete_scrap, name='delete_scrap'), # delete_scrap 함수
]
