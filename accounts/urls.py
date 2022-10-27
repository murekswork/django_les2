from django.urls import path, include
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path('profile/', AccountOverviewView, name='profile'),
    path('profile/update/', UpdateProfileView, name='profile_edit'),
    path('signup/', SignUpView, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),

]