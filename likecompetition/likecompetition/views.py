from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.core.paginator import Paginator
from posts.models import Post, Scrap

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
