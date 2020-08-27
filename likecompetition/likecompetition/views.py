from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.core.paginator import Paginator
from django.contrib.auth.mixins import AccessMixin
from posts.models import Post, Scrap
from django.views.generic.edit import FormView
from posts.filters import PostFilter

class IndexView(View):
    def get(self, request, *args, **kwargs):
        page = self.kwargs.get('page')
        if page == None:
            return redirect('index_page', page=1)
        posts = Post.objects.all().order_by('-id')
        # posts = PostFilter(request.GET, queryset=posts)
        paginator = Paginator(posts, 20)
        posts = paginator.get_page(page)
        for post in posts:
            post.scrapped = 'true' if request.user.is_authenticated and Scrap.objects.filter(user=request.user, post=post).exists() else 'false'
        return render(request, 'index.html', {'posts': posts})

# class IndexView(View):

#     def get(self, request, *args, **kwargs):
#         page = self.kwargs.get('page')
#         if page == None:
#             return redirect('index_page', page=1)
#         posts = Post.objects.all().order_by('-id')
#         paginator = Paginator(posts, 20)
#         posts = paginator.get_page(page)
#         for post in posts:
#             post.scrapped = 'true' if request.user.is_authenticated and Scrap.objects.filter(user=request.user, post=post).exists() else 'false'
#         return render(request, 'index.html', {'posts': posts})

class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "User only can update/delete the object"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
