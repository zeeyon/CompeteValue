from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True) # 사용자가 직접 입력하지 않아도 자동으로 시간 받아오기
    content = models.TextField(default='') # default='', content에 아무것도 안 써도 null 에러가 나지 않음
    view_count = models.IntegerField(default=0) # 조회수

    def __str__(self): # title: 사용자가 입력한대로 string 불러오기
        return self.title

    # content 내용 중 앞부분 일부만 가져오기, 나중에 index로 넘길때 불필요 시 삭제
    # def summary(self):
    #     return self.content[:30]

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True) # 사용자가 직접 입력하지 않아도 자동으로 시간 받아오기
    content = models.TextField(default='') # default='', content에 아무것도 안 써도 null 에러가 나지 않음

class Scrap(models.Model):
    class Meta:
        unique_together = ('user', 'post')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True) # 사용자가 직접 입력하지 않아도 자동으로 시간 받아오기
