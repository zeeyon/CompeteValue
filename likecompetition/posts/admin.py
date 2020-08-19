from django.contrib import admin
from .models import Post, Comment, Scrap, City, Area # , Tag
from . import models


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'city','area','field','content', 'tag_list')
    # list_filter = ('modify_dt',)
    # search_fields = ('title', 'content')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):         
        return ', '.join(o.name for o in obj.tags.all())


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Scrap)
admin.site.register(City)
admin.site.register(Area)