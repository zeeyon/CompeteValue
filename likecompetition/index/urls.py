from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:page>', views.IndexView.as_view(), name='index_page'),
    path('posts/<int:post_id>', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/new', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:post_id>/edit', views.PostEditView.as_view(), name='post_edit'),
    path('posts/<int:post_id>/comments', views.CommentView.as_view(), name='comment'),
    path('posts/<int:post_id>/comments/<int:comment_id>', views.CommentDetailView.as_view(), name='comment_detail'),
    path('scrap/', views.scrap, name='scrap'),
    path('create/scrap/<int:post_id>', views.create_scrap, name='create_scrap'),
    path('delete/scrap/<int:scrap_id>', views.delete_scrap, name='delete_scrap'),
]
