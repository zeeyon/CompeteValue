from django import forms
from .models import Post, Comment, Area

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','gender','age','city','area','content']
    
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
                self.fields['area'].queryset = self.instance.city.area_set.order_by('name')
            except:
                pass

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
