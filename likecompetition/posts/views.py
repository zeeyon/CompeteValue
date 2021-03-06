from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from posts.models import *
from posts.forms import *
from posts.serializers import *
from posts.permissions import IsOwnerOrReadOnly
from rest_framework import generics, mixins, pagination, permissions, status


class PostAPIView(generics.RetrieveDestroyAPIView):
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

	def get_object(self):
		obj = get_object_or_404(Post, pk=self.kwargs['post_id'])
		self.check_object_permissions(self.request, obj)
		obj.scrapped = self.request.user.is_authenticated and Scrap.objects.filter(user=self.request.user, post=obj).exists()
		return obj

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class PostListView(generics.ListAPIView):
	serializer_class = PostSerializer

	def get_queryset(self):
		posts = Post.objects.all().order_by('-id')
		for post in posts:
			post.scrapped = self.request.user.is_authenticated and Scrap.objects.filter(user=self.request.user, post=post).exists()
		return posts


class PostDetailView(TemplateView):
	template_name = 'post_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['post_id'] = kwargs['post_id']
		return context


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = 'post_form.html'

	def get_success_url(self):
		return reverse_lazy('posts:post_detail', kwargs={'post_id': self.object.id})

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form, error_message='form is not valid :('))


class PostEditView(LoginRequiredMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = 'post_form.html'

	def get_success_url(self):
		return reverse_lazy('posts:post_detail', kwargs={'post_id': self.object.id})

	def get_object(self, *args, **kwargs):
		obj = super().get_object(*args, **kwargs)
		if not obj.user == self.request.user:
			raise PermissionDenied
		return obj

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form, error_message='form is not valid :('))


class CommentListCreateView(generics.ListAPIView):
	class CommentListPagination(pagination.PageNumberPagination):
		page_size = 1000

	serializer_class = CommentSerializer
	pagination_class = CommentListPagination

	def get_queryset(self):
		return Comment.objects.filter(post=self.kwargs['post_id']).order_by('id')

	def post(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs['post_id'])
		form = CommentForm(request.POST)
		if not form.is_valid():
			return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
		form.instance.post = post
		form.instance.user = request.user
		form.save()
		return HttpResponse(form.instance.id, status=status.HTTP_201_CREATED)


class CommentRetrieveDestroyView(generics.RetrieveDestroyAPIView):
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

	def get_object(self):
		obj = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
		self.check_object_permissions(self.request, obj)
		return obj

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class ScrapToggleView(mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
	serializer_class = ScrapSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

	def get_object(self):
		obj = get_object_or_404(Scrap, user=self.request.user, post=self.kwargs['post_id'])
		self.check_object_permissions(self.request, obj)
		return obj

	def post(self, request, *args, **kwargs):
		request.data.update(user=request.user.id, post=kwargs['post_id'])
		return self.create(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class SidoListView(generics.ListAPIView):
	serializer_class = SidoSerializer

	def get_queryset(self):
		return Sido.objects.all().order_by('id')


class SigunguListView(generics.ListAPIView):
	serializer_class = SigunguSerializer

	def get_queryset(self):
		return Sigungu.objects.filter(sido=self.kwargs['sido_id']).order_by('id')
