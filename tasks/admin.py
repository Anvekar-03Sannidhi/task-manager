from django.contrib import admin
from .models import Task #importing Task model from models.py to register it in admin panel

# Register your models here.
admin.site.register(Task)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'deadline') #fields to display in admin panel list view
    list_filter = ('status', 'priority') #filters for status and priority in admin panel
    search_fields = ('title') #search functionality for title in admin panel