from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Post, Comment, Scrap, Area
from .forms import PostForm, CommentForm
from likecompetition.serializers import PostSerializer
from rest_framework import generics


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

	def delete(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs['post_id'])
		if request.user == post.user:
			post.delete()
		return HttpResponse()


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


class CommentCreateView(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs['post_id'])
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.user = request.user
			comment.save()
		return redirect('posts:post_detail', post_id=post.id)


class CommentDeleteView(LoginRequiredMixin, View):
	def delete(self, request, *args, **kwargs):
		comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
		if request.user == comment.user:
			comment.delete()
		return HttpResponse()


class MyScrapView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		scraps = Scrap.objects.filter(user=request.user).order_by('-date')
		return render(request, 'scrap.html', {'scraps': scraps})


class ScrapToggleView(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs['post_id'])
		scrap = Scrap(user=request.user, post=post)
		scrap.save()
		return HttpResponse()

	def delete(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs['post_id'])
		scrap = get_object_or_404(Scrap, user=request.user, post=post)
		scrap.delete()
		return HttpResponse()


class LoadAreasView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		areas = Area.objects.filter(city_id=kwargs['city_id'])
		return render(request, 'area_list.html', {'areas': areas})
