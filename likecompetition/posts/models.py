from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from hitcount.models import HitCountMixin


class City(models.Model):
	name = models.CharField(max_length=40)

	def __str__(self):
		return self.name


class Area(models.Model):
	city = models.ForeignKey(City, on_delete=models.CASCADE)
	name = models.CharField(max_length=40)

	def __str__(self):
		return self.name


FIELD_CHOICES=(
	('web','웹'),
	('android','안드로이드'),
	('ios','iOS'),
	('game','게임'),
	('ml','머신러닝'),
	('bigdata','빅데이터'),
	('iot','IoT'),
	('blockchain','블록체인'),
	('vr','가상현실'),
	('etc','기타'),
)


class Post(models.Model, HitCountMixin):
	title = models.CharField(max_length=50, null=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
	area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True) 
	field = MultiSelectField(choices=FIELD_CHOICES)
	content = models.TextField(default='')
	
	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	content = models.TextField(default='')

	def __str__(self):
		return self.content


class Scrap(models.Model):
	class Meta:
		unique_together = ('user', 'post')

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.nickname + "|" + self.post.title
