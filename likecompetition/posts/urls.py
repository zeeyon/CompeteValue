from django.urls import path, re_path
from . import views

app_name = 'posts'

urlpatterns = [
    path('<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('new', views.PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit', views.PostEditView.as_view(), name='post_edit'),
    # path('<int:pk>/comments', views.CommentCreateView.as_view(), name='comment_create'),
    path('<int:pk>/comments/<int:comment_id>', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('scrap', views.ScrapView.as_view(), name='scrap_list'),
    path('me', views.MyPostView.as_view(), name='my_post'),
    path('<int:post_id>/scrap', views.ScrapView.as_view(), name='scrap_detail'),
    path('ajax_load_areas', views.LoadAreasView.as_view(), name='ajax_load_areas'),
    path('tag_autocomplete', views.TagAutocompleteView.as_view(), name='tag_autocomplete'),
]
