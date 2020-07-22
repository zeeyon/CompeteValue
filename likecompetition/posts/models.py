from django.db import models
from django.conf import settings

class City(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Area(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=50, choices={
        ('male','남자'),
        ('female','여자'),
    })
    age = models.IntegerField(null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, blank=True, null=True) 
    content = models.TextField(default='')
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
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
