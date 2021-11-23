from django.contrib import admin
from .models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    list_display_links = ['title', 'author']
    search_fields = ['id', 'title', 'author', 'date_created']
    list_filter = ['date_created']


admin.site.register(BlogPost, BlogPostAdmin)
