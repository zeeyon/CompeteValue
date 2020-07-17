from django.urls import path
from . import views

urlpatterns = [
    path('<int:post_id>', views.PostDetailView.as_view(), name='post_detail'),
    path('new', views.PostCreateView.as_view(), name='post_create'),
    path('<int:post_id>/edit', views.PostEditView.as_view(), name='post_edit'),
    path('<int:post_id>/comments', views.CommentView.as_view(), name='comment'),
    path('<int:post_id>/comments/<int:comment_id>', views.CommentView.as_view(), name='comment_detail'),
    path('scrap', views.ScrapView.as_view(), name='scrap_list'),
    path('<int:post_id>/scrap', views.ScrapView.as_view(), name='scrap_detail'),
]
