from django.contrib import admin
from .models import Post, Comment, Scrap, City, Area # , Tag
from . import models


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'city', 'area', 'field', 'content')
    # list_filter = ('modify_dt',)
    # search_fields = ('title', 'content')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Scrap)
admin.site.register(City)
admin.site.register(Area)
