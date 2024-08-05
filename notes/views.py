from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Notes

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from . forms import NotesForm
from django.contrib.auth.mixins import LoginRequiredMixin


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
        return self.request.user.notes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        note_id = self.kwargs.get('pk')
        if note_id:
            context['note'] = get_object_or_404(Notes, pk=note_id)
        return context