from django.contrib import admin
from .models import Post, Comment, Scrap, Sido, Sigungu
from . import models


class PostAdmin(admin.ModelAdmin):
	list_display = ('user', 'date', 'area', 'field', 'content')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Scrap)
admin.site.register(Sido)
admin.site.register(Sigungu)
