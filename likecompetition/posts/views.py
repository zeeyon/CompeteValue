from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from .models import Post, Comment, Scrap, Area
from .forms import PostForm, CommentForm

class BaseView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        elif request.method == 'POST':
            method = request.POST.get('_method', 'POST')
            handler = getattr(self, method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

class PostDetailView(BaseView):
    def get(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        comments = Comment.objects.filter(post=post)
        form = CommentForm()
        Post.objects.filter(id=post_id).update(view_count=F('view_count')+1)
        return render(request, 'post_detail.html', {'post': post, 'form': form, 'comments': comments})

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        if request.user == post.user:
            post.delete()
        return redirect('index')

class PostCreateView(LoginRequiredMixin, BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, 'post_form.html', {'form': PostForm()})

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if not form.is_valid():
            return render(request, 'post_form.html', {'form': form, 'error_message': 'Error..'})
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('post_detail', post_id=post.id)

class PostEditView(LoginRequiredMixin, BaseView):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if not request.user == post.user:
            return redirect('index')
        return render(request, 'post_form.html', {'form': PostForm(instance=post), 'method': 'PUT'})

    def put(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if not request.user == post.user:
            return redirect('index')
        form = PostForm(request.POST, instance=post)
        if not form.is_valid():
            return render(request, 'post_form.html', {'form': form, 'method': 'PUT', 'error_message': 'Error..'})
        post = form.save(commit=False)
        post.save()
        return redirect('post_detail', post_id=post.id)

class CommentView(LoginRequiredMixin, BaseView):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
        return redirect('post_detail', post_id=post.id)

    def delete(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        if request.user == comment.user:
            comment.delete()
        return redirect('post_detail', post_id=comment.post.id)

class ScrapView(LoginRequiredMixin, BaseView):
    def get(self, request, *args, **kwargs):
        scraps = Scrap.objects.filter(user=request.user).order_by('-date')
        return render(request, 'scrap.html', {'scraps': scraps})

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        count = Scrap.objects.filter(user=request.user, post=post).count()
        if not count:
            scrap = Scrap(user=request.user, post=post)
            scrap.save()
        return redirect('post_detail', post_id=post_id)

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        scrap = get_object_or_404(Scrap, user=request.user, post=post)
        scrap.delete()
        return redirect('scrap_list')

def load_areas(request):
    city_id = request.GET.get('city_id')
    areas = Area.objects.filter(city_id=city_id).all()
    return render(request, 'ajax_post_areas_list.html', {'areas':areas})
