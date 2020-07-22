from django.contrib import admin
from .models import Post, Comment, Scrap, City, Area

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Scrap)
admin.site.register(City)
admin.site.register(Area)