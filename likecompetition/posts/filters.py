from .models import Post
from .forms import PostForm
from django import forms
from django_filters import FilterSet, MultipleChoiceFilter
from likecompetition.settings import FIELD_CHOICES

class PostFilter(FilterSet):
    field = MultipleChoiceFilter(choices=FIELD_CHOICES)
    
    class Meta:
        model = Post
        fields = ['field',]
