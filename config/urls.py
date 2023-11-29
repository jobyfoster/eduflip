from django.contrib import admin
from django.urls import path
from app import views as app_views
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin URLs
    path("admin/", admin.site.urls),
    # Home Page URL
    path("", app_views.home_view, name="home"),
    # Flashcard Creation URL
    path(
        "create-flashcards/",
        app_views.generate_flashcards_view,
        name="create_flashcards",
    ),
    # Flashcard Studying and Searching URL
    path("browse-flashcards/", app_views.search_flashcards, name="browse_flashcards"),
    path(
        "flashcards/<str:set_id>/",
        app_views.flashcard_set_view,
        name="view_flashcard_set",
    ),
    # Flashcard Favorites Management URLs
    path(
        "remove-favorite/<str:set_id>/",
        app_views.remove_from_favorites,
        name="remove_favorite",
    ),
    path("add-favorite/<str:set_id>/", app_views.add_to_favorites, name="add_favorite"),
    # Flashcard Deletion URL
    path(
        "delete-flashcards/<str:set_id>/",
        app_views.delete_flashcard_set,
        name="delete_flashcards",
    ),
    # User's Flashcards URL
    path("my-flashcards/", app_views.user_flashcards, name="my_flashcards"),
    # User Authentication and Management URLs
    path("register/", user_views.register, name="register"),
    path("user-settings/", user_views.settings, name="user_settings"),
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
