from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponse
from .models import Post, Comment, Scrap, Area #, Tag
from .forms import PostForm, CommentForm
from dal import autocomplete
from taggit.models import Tag
from django.urls import reverse_lazy, reverse
from likecompetition.views import OwnerOnlyMixin
from hitcount.views import HitCountDetailView

class PostDetailView(HitCountDetailView):
    template_name = 'posts/post_detail.html'
    model = Post
    count_hit = True

class TagAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return Tag.objects.none()
        qs = Tag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'posts/post_form.html'
    form_class = PostForm
    model = Post
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostEditView(OwnerOnlyMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostDeleteView(OwnerOnlyMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('index')

class CommentView(LoginRequiredMixin, View):
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

class ScrapView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        scraps = Scrap.objects.filter(user=request.user).order_by('-date')
        return render(request, 'scrap.html', {'scraps': scraps})

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        if not Scrap.objects.filter(user=request.user, post=post).exists():
            scrap = Scrap(user=request.user, post=post)
            scrap.save()
        return HttpResponse()

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        scrap = get_object_or_404(Scrap, user=request.user, post=post)
        scrap.delete()
        return HttpResponse()

class LoadAreasView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            city_id = request.GET.get('city_id')
            areas = Area.objects.filter(city_id=city_id).all()
        return render(request, 'ajax_post_areas_list.html', {'areas':areas})