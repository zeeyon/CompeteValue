from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    GENDER_CHOICES = {
        ('male','Male'),
        ('female','Female'),
    }
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    age = models.IntegerField(null=True)
    CITY_CHOICES = {
        ('Seoul','서울특별시'),
        ('Incheon','인천광역시'),
    }
    # AREA_CHOICES = [{
    #     ('Seoul', (
    #             ('gangnam-gu','강남구'),
    #             ('gangdong-gu','강동구'),
    #         )
    #     )
    # },{
    #     ('Incheon', (
    #             ('gyeyang-gu','계양구'),
    #             ('nam-gu','남구'),
    #         )
    #     )
    # }]
    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    # area = models.CharField(max_length=50, choices=AREA_CHOICES[AREA_CHOICES.index(city)]) 
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
