from likecompetition import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Comment, Scrap, Area
from .forms import PostForm, CommentForm
from dal import autocomplete
from taggit.models import Tag
from django.urls import reverse_lazy, reverse
from likecompetition.views import OwnerOnlyMixin
from hitcount.views import HitCountDetailView
from django.contrib import messages
from likecompetition.settings import FIELD_CHOICES


class PostDetailView(LoginRequiredMixin, HitCountDetailView):
    template_name = 'posts/post_detail.html'
    model = Post
    count_hit = True 

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):	
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user	
        context['comments'] = self.object.comment_set.all()
        return context

    def post(self, request, *args, **kwargs):	
        self.object = self.get_object()	
        form = self.get_form()		

        if form.is_valid():			
            return self.form_valid(form)
        else:			
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)	
        comment.post = get_object_or_404(Post, pk=self.object.pk) 
        comment.user = self.request.user
        comment.save()
        return super(PostDetailView, self).form_valid(form)

    # delete도 여기서


class CommentCreateView(LoginRequiredMixin, FormMixin):
    form_class = CommentForm
    # PostDetailView와 CommentCreateView를 분리해주세요


class TagAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return Tag.objects.none()
        qs = Tag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
    template_name = 'posts/post_form.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostEditView(OwnerOnlyMixin, UpdateView):
    template_name = 'posts/post_form.html'
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CommentDeleteView(OwnerOnlyMixin, View):
    model = Comment

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        comment.delete()
        return HttpResponse()


class ScrapView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = []
        for scrap in Scrap.objects.filter(user=request.user).order_by('-date'):
            posts.append(scrap.post)
        for post in posts:
            post.scrapped = 'true'
        return render(request, 'scrap.html', {'posts': posts})

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if not Scrap.objects.filter(user=request.user, post=post).exists():
            scrap = Scrap(user=request.user, post=post)
            scrap.save()
        return HttpResponse()

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        scrap = get_object_or_404(Scrap, user=request.user, post=post)
        scrap.delete()
        return HttpResponse()


class MyPostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(user=request.user).order_by('-date')
        for post in posts:
            post.scrapped = 'true' if request.user.is_authenticated and Scrap.objects.filter(user=request.user, post=post).exists() else 'false'
        return render(request, 'scrap.html', {'posts': posts})


class LoadAreasView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            city_id = request.GET.get('city_id')
            areas = Area.objects.filter(city_id=city_id).all()
        return render(request, 'ajax_post_areas_list.html', {'areas':areas})
