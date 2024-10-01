from django.urls import path
from .views import signup, login_view, logout_view, home

urlpatterns = [
    path('', home, name='home'),  # Welcome/Home view
    path('register/', signup, name='signup'),  # Registration view
    path('login/', login_view, name='login'),  # Login view
    path('logout/', logout_view, name='logout'),  # Logout view
]
