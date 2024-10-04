from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from models import Notes, Category

class NotesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test Category')
        self.note = Notes.objects.create(title='Test Note', text='This is a test note.', user=self.user, category=self.category)

    def test_note_creation(self):
        note = Notes.objects.get(title='Test Note')
        self.assertEqual(note.text, 'This is a test note.')

    def test_notes_list_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('notes.list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
