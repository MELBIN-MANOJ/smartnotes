from django.contrib import admin
from . import models

class NotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created', 'user')  # Include category, created, and user fields
    list_filter = ('category', 'user')  # Add filtering by category and user
    search_fields = ('title', 'text')  # Enable search functionality for title and text

admin.site.register(models.Notes, NotesAdmin)

# Don't forget to register the Category model as well
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Display ID and name in the admin panel

admin.site.register(models.Category, CategoryAdmin)  # Register the Category model

