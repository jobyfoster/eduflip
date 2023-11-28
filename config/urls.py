from django.contrib import admin
from django.urls import path
from app import views as app_views
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin URLs
    path("admin/", admin.site.urls),
    # App URLs
    path("", app_views.home_view, name="home"),
    path("generate/", app_views.generate_flashcards_view, name="generate_flashcards"),
    path("study/", app_views.search_flashcards, name="search_flashcards"),
    path("study/<str:set_id>/", app_views.flashcard_set_view, name="flashcard_set"),
    path(
        "study/unfavorite/<str:set_id>/",
        app_views.remove_from_favorites,
        name="unfavorite_flashcard_set",
    ),
    path(
        "study/favorite/<str:set_id>/",
        app_views.add_to_favorites,
        name="favorite_flashcard_set",
    ),
    path("flashcards/", app_views.user_flashcards, name="user_flashcards"),
    # User Authentication and Management URLs
    path("register/", user_views.register, name="register"),
    path("settings/", user_views.settings, name="settings"),
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
]
