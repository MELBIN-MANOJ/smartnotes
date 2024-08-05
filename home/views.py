from django.views import View
from django.views.generic import TemplateView, CreateView

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import logout


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'home/register.html'
    success_url = '/smart/notes/'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes.list')
        return super().get(request, *args, **kwargs)


class LoginInterfaceView(LoginView):
    template_name = 'home/login.html'


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class HomeView(TemplateView):
    template_name = 'home/welcome.html'

