"""
URL configuration for NotesApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from notes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('smart/', include('notes.urls')),


    path('adminpanel/edit_note/<int:pk>/', views.edit_note, name='edit_note'),
    path('adminpanel/delete_note/<int:pk>/', views.delete_note, name='delete_note'),
    path('adminpanel/dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('adminpanel/manage_notes/', views.manage_notes, name="manage_notes"),
    path('adminpanel/manage_categories/', views.manage_categories, name="manage_categories"),
    path('adminpanel/manage_users/', views.manage_users, name="manage_users"),
    path('adminpanel/edit_user/<int:id>/', views.edit_user, name="edit_user"),
    path('adminpanel/delete_user/<int:id>/', views.delete_user, name="delete_user"),


    path('adminpanel/edit_category/<int:pk>/', views.edit_category, name="edit_category"),
    path('adminpanel/delete_category/<int:pk>/', views.delete_category, name="delete_category"),
    # Change this line in your urlpatterns
    path('adminpanel/notes-statistics/', views.notes_statistics, name='notes_statistics'),

]
