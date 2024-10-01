from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Category, Notes

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from . forms import NotesForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse


class NotesDeleteView(LoginRequiredMixin, DeleteView):
    model = Notes
    success_url = '/smart/notes/'
    template_name = 'notes/notes_delete.html'
    login_url = "/login"

    def get_queryset(self):
        return self.request.user.notes.all()


class NotesUpdateView(LoginRequiredMixin, UpdateView):
    model = Notes
    success_url = '/smart/notes/'
    form_class = NotesForm
    login_url = "/login"

    def get_queryset(self):
        return self.request.user.notes.all()


class NotesCreateView(LoginRequiredMixin, CreateView):
    model = Notes
    success_url = '/smart/notes/'
    form_class = NotesForm
    login_url = "/login"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    template_name = "notes/notes_view.html"
    context_object_name = "notes"
    login_url = "/login"

    def get_queryset(self):
        queryset = self.request.user.notes.all()
        search_query = self.request.GET.get('q', '')
        category_id = self.request.GET.get('category')  # Get the selected category ID

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(text__icontains=search_query))
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)  # Filter by selected category
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        note_id = self.request.GET.get('note_id')  # Get the note ID from query parameters
        
        if note_id:
            context['note'] = get_object_or_404(Notes, pk=note_id)
        
        # Fetch all categories for the dropdown
        context['categories'] = Category.objects.all()
        return context
    


# Initialize the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Add this new view to your views.py file
def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        
        # Generate a response using Gemini
        response = model.generate_content(user_input)
        
        return JsonResponse({'response': response.text})
    
    return render(request,'notes/chatbot.html')





from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .models import Notes, Category
from django.contrib.auth.models import User

# Restrict access to the admin dashboard for superusers only
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser, login_url='/login/')
def admin_dashboard(request):
    # Context for dashboard
    context = {
        'notes_count': Notes.objects.count(),
        'categories_count': Category.objects.count(),
        'users_count': User.objects.count(),
        'latest_notes': Notes.objects.order_by('-created')[:5],  # Show latest notes
    }
    return render(request, 'admin_dashboard/dashboard.html', context)

@user_passes_test(is_superuser, login_url='/login/')
def manage_notes(request):
    notes = Notes.objects.all()
    return render(request, 'admin_dashboard/manage_notes.html', {'notes': notes})

@user_passes_test(is_superuser, login_url='/login/')
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'admin_dashboard/manage_categories.html', {'categories': categories})

@user_passes_test(is_superuser, login_url='/login/')
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin_dashboard/manage_users.html', {'users': users})


from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Notes, Category  # Ensure you import your models
from .forms import NotesForm  # Ensure you import your NotesForm

def manage_users(request):
    users_list = User.objects.all().order_by('-date_joined')
    paginator = Paginator(users_list, 10)  # Show 10 users per page

    page = request.GET.get('page')
    users = paginator.get_page(page)

    return render(request, 'admin_dashboard/manage_users.html', {'users': users})

def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        is_superuser = request.POST.get('is_superuser') == 'on'
        
        user.username = username
        user.email = email
        user.is_superuser = is_superuser
        user.save()
        
        messages.success(request, 'User updated successfully!')
        return redirect('manage_users')  # Redirect to the user management page after edit
    
    return render(request, 'admin_dashboard/edit_user.html', {'user': user})

def delete_user(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('manage_users')  # Redirect to the user management page after deletion

    return render(request, 'admin_dashboard/delete_user.html', {'user': user})

# Edit Notes View
def edit_note(request, pk):
    # Ensure this correctly retrieves the note that belongs to the user
    note = get_object_or_404(Notes, pk=pk)
    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('manage_notes')  # Redirect to the notes management view
    else:
        form = NotesForm(instance=note)
    return render(request, 'admin_dashboard/edit_note.html', {'form': form, 'note': note})


# Delete Notes View
def delete_note(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('manage_notes')  # Redirect to the notes management view
    return render(request, 'admin_dashboard/delete_note.html', {'note': note})


# Edit Categories View
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        messages.success(request, 'Category updated successfully!')
        return redirect('manage_categories')  # Redirect to the category management page
    return render(request, 'admin_dashboard/edit_category.html', {'category': category})

# Delete Categories View
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('manage_categories')  # Redirect to the category management page
    return render(request, 'admin_dashboard/delete_category.html', {'category': category})

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from .models import Notes, User

@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def notes_statistics(request):
    # Get count of notes per category
    notes_per_category = Notes.objects.values('category__name').annotate(count=Count('id')).order_by('category__name')
    user_data = User.objects.annotate(note_count=Count('notes')).values('username', 'note_count')

    categories = [entry['category__name'] for entry in notes_per_category]
    counts = [entry['count'] for entry in notes_per_category]
    users = [data['username'] for data in user_data]
    user_counts = [data['note_count'] for data in user_data]

    # Time-based data (mock data for demonstration)
    time_labels = ['January', 'February', 'March', 'April', 'May']  # Example labels
    time_counts = [5, 10, 15, 8, 12]  # Example counts

    context = {
        'categories': categories,
        'counts': counts,
        'users': users,
        'user_counts': user_counts,
        'users_and_counts': zip(users, user_counts),
        'time_labels': time_labels,
        'time_counts': time_counts,
    }
    return render(request, 'admin_dashboard/notes_statistics.html', context)

