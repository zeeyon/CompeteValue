from django import forms
from .models import Post, Comment, Sido, Sigungu


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['area', 'field', 'content']


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']
		widgets = {
			'content': forms.Textarea(attrs={'placeholder': 'Add a comment...'}),
		}
