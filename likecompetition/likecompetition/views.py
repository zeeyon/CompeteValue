from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.core.paginator import Paginator
from posts.models import Post

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

class IndexView(BaseView):
    def get(self, request, *args, **kwargs):
        page = self.kwargs.get('page')
        if page == None:
            return redirect('index_page', page=1)
        posts = Post.objects.all().order_by('-id')
        paginator = Paginator(posts, 5)
        posts = paginator.get_page(page)
        return render(request, 'index.html', {'posts': posts})
