from django import forms
from .models import Notes


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('title', 'text')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-3', 'placeholder': 'Enter title'}),
            'text': forms.Textarea(attrs={'class': 'form-control my-3', 'placeholder': 'Enter text'}),
        }