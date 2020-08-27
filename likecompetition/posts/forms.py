from django import forms
from .models import Post, Comment, Area
from dal import autocomplete
from taggit.models import Tag
from multiselectfield import MultiSelectField
from likecompetition.settings import FIELD_CHOICES

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','city','area','field','tags','content']
        widgets = {
            'tags':autocomplete.TagSelect2(url='posts:tag_autocomplete'),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['area'].queryset = Area.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            try:
                self.fields['area'].queryset = self.instance.city.arefa_set.order_by('name')
            except:
                pass

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

# class SearchForm(forms.Form):
#     searchfield = MultiSelectField(choices=FIELD_CHOICES)

