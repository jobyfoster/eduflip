"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from app import views as app_views
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", app_views.home_view, name="home"),
    path("generate/", app_views.generate_flashcards_view, name="generate_flashcards"),
    path("study/", app_views.search_flashcards, name="find_flashcards"),
    path("study/<str:set_id>/", app_views.flashcard_set_view, name="flashcard_set"),
    path("flashcards/", app_views.user_flashcards, name="user_flashcards"),
    path("register/", user_views.register, name="register"),
    path(
        "settings/",
        user_views.settings,
        name="settings",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("admin/", admin.site.urls),
]
