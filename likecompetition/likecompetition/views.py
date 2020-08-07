from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.core.paginator import Paginator
from posts.models import Post, Scrap

class IndexView(View):
    def get(self, request, *args, **kwargs):
        page = self.kwargs.get('page')
        if page == None:
            return redirect('index_page', page=1)
        posts = Post.objects.all().order_by('-id')
        paginator = Paginator(posts, 20)
        posts = paginator.get_page(page)
        for post in posts:
            post.scrapped = 'true' if request.user.is_authenticated and Scrap.objects.filter(user=request.user, post=post).exists() else 'false'
        return render(request, 'index.html', {'posts': posts})
