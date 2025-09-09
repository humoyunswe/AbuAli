from django.contrib import admin

# Register your models here.
from .models import Candidates


@admin.register(Candidates)
class CandidatesAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('created_at',)
