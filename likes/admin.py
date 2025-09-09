from django.contrib import admin
from .models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('created_at', 'article')
    search_fields = ('user__username', 'article__title')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'article')
        }),
        ('Метаданные', {
            'fields': ('created_at',)
        }),
    )
