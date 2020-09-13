from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
	path('', views.PostListView.as_view(), name='post_list'),
	path('new', views.PostCreateView.as_view(), name='post_create'),
	path('<int:post_id>', views.PostAPIView.as_view(), name='post_api'),
	path('<int:post_id>/detail', views.PostDetailView.as_view(), name='post_detail'),
	path('<int:pk>/edit', views.PostEditView.as_view(), name='post_edit'),
	path('<int:post_id>/comments', views.CommentListCreateView.as_view(), name='comment_list_create'),
	path('comments/<int:comment_id>', views.CommentRetrieveDestroyView.as_view(), name='comment_retrieve_destroy'),
	# path('scrap', views.MyScrapView.as_view(), name='my_scrap'),
	path('<int:post_id>/scrap', views.ScrapToggleView.as_view(), name='scrap_detail'),
    path('sidos', views.SidoListView.as_view(), name='sido_list'),
	path('sidos/<int:sido_id>', views.SigunguListView.as_view(), name='sigungu_list'),
]
