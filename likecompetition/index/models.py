from django.db import models

class Post(models.Model):

    title = models.CharField(max_length=50,null=False)
    date = models.DateTimeField(auto_now_add=True) # 사용자가 직접 입력하지 않아도 자동으로 시간 받아오기
    content = models.TextField(default='') # default='', content에 아무것도 안써도 null에러가 나지 않음

    def __str__(self): # title: 사용자가 입력한대로 string 불러오기
        return self.title

    # content내용 중 앞부분 일부만 가져오기, 나중에 index로 넘길때 불필요 시 삭제
    # def summary(self):
    #     return self.content[:30]