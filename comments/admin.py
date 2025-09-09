from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'content', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at', 'article')
    search_fields = ('content', 'author__username', 'article__title')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('article', 'author', 'content', 'parent')
        }),
        ('Метаданные', {
            'fields': ('is_approved', 'created_at', 'updated_at')
        }),
    )
