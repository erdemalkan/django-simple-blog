from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'title', 'slug', 'created', 'published', 'edit']
    list_display_links = ['id', 'title', 'edit']
    list_filter = ['created']
    search_fields = ['title', 'body']

    class Meta:
        model = Post