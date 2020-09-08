from django import forms
from .models import Post, Comment, Area


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'city', 'area', 'field', 'content']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.instance.city:
			self.fields['area'].queryset = Area.objects.filter(city_id=self.instance.city.id)
		else:
			self.fields['area'].queryset = Area.objects.none()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Add a comment...'}),
        }
