from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from .models import Post, Comment, Sido, Sigungu, Scrap
from .forms import PostForm, CommentForm
from posts.serializers import *
from posts.permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework import generics, mixins, permissions, status


class PostAPIView(View):
	def delete(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs['post_id'])
		if request.user == post.user:
			post.delete()
		return HttpResponse(status=204)


class PostListView(generics.ListAPIView):
	serializer_class = PostSerializer

	def get_queryset(self):
		posts = Post.objects.all().order_by('-id')
		for post in posts:
			post.scrapped = self.request.user.is_authenticated and Scrap.objects.filter(user=self.request.user, post=post).exists()
		return posts


class PostDetailView(View):
	def get(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs['post_id'])
		comments = Comment.objects.filter(post=post)
		return render(request, 'post_detail.html', {'post': post, 'form': CommentForm(), 'comments': comments})


class PostCreateView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		return render(request, 'post_form.html', {'form': PostForm()})

	def post(self, request, *args, **kwargs):
		form = PostForm(request.POST)
		if not form.is_valid():
			return render(request, 'post_form.html', {'form': form, 'error_message': 'form is not valid :('})
		post = form.save(commit=False)
		post.user = request.user
		post.save()
		return redirect('posts:post_detail', post_id=post.id)


class PostEditView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs['post_id'])
		if not request.user == post.user:
			return redirect('index')
		return render(request, 'post_form.html', {'form': PostForm(instance=post)})

	def post(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs['post_id'])
		if not request.user == post.user:
			return redirect('index')
		form = PostForm(request.POST, instance=post)
		if not form.is_valid():
			return render(request, 'post_form.html', {'form': form, 'error_message': 'form is not valid :('})
		form.save()
		return redirect('posts:post_detail', post_id=post.id)


class CommentCreateView(LoginRequiredMixin, CreateView):
	form_class = CommentForm

	def form_valid(self, form):
		form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
		form.instance.user = self.request.user
		form.save()
		return HttpResponse(status=status.HTTP_201_CREATED)


class CommentDeleteView(generics.DestroyAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

	def get_object(self):
		obj = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
		self.check_object_permissions(self.request, obj)
		return obj

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class MyScrapView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		return HttpResponse() # 수정 예정


class ScrapToggleView(mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
	serializer_class = ScrapSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

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
		return Sido.objects.all()


class SigunguListView(generics.ListAPIView):
	serializer_class = SigunguSerializer

	def get_queryset(self):
		return Sigungu.objects.filter(sido=self.kwargs['sido_id'])
