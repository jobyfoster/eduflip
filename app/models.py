from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import string
import random


# Helper function to generate a unique ID for FlashcardSet
def generate_unique_id():
    while True:
        unique_id = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        if not FlashcardSet.objects.filter(id=unique_id).exists():
            return unique_id


# Model for Flashcard Sets
class FlashcardSet(models.Model):
    id = models.CharField(
        max_length=8, primary_key=True, default=generate_unique_id, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    study_level = models.CharField(max_length=100)
    number_of_flashcards = models.IntegerField(default=10)
    topic = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id()
        super().save(*args, **kwargs)


# Model for individual Flashcards
class Flashcard(models.Model):
    flashcard_set = models.ForeignKey(
        FlashcardSet, related_name="flashcards", on_delete=models.CASCADE
    )
    question = models.TextField()
    answer = models.TextField()


# Function to create a new flashcard set
def create_flashcard_set(
    user, flashcards_data, topic, study_level, number_of_flashcards
):
    flashcard_set = FlashcardSet(
        user=user,
        topic=topic,
        study_level=study_level,
        number_of_flashcards=number_of_flashcards,
    )
    flashcard_set.save()

    for card_data in flashcards_data:
        Flashcard.objects.create(
            flashcard_set=flashcard_set,
            question=card_data["question"],
            answer=card_data["answer"],
        )

    return flashcard_set


# Various search functions
def get_user_flashcard_sets(user):
    return FlashcardSet.objects.filter(user=user)


def get_flashcards_from_set(flashcard_set):
    return flashcard_set.flashcards.all()


def search_by_topic(query):
    return FlashcardSet.objects.filter(topic__icontains=query)


def search_by_study_level(level):
    return FlashcardSet.objects.filter(study_level__icontains=level)


def search_by_date_range(start_date, end_date):
    return FlashcardSet.objects.filter(created_at__range=[start_date, end_date])


def search_by_flashcard_count(count):
    return FlashcardSet.objects.filter(number_of_flashcards=count)


def search_by_user_id(user_id):
    return FlashcardSet.objects.filter(user__id=user_id)


def search_by_username(username):
    return FlashcardSet.objects.filter(user__username=username)


def search_by_id(set_id):
    return FlashcardSet.objects.filter(id=set_id)


def recent_flashcard_sets(limit=10):
    return FlashcardSet.objects.order_by("-created_at")[:limit]


def search_by_level_and_topic(level, topic):
    return FlashcardSet.objects.filter(
        study_level__icontains=level, topic__icontains=topic
    )


def count_sets_by_user(user_id):
    return FlashcardSet.objects.filter(user__id=user_id).count()


def advanced_search(
    topic=None,
    level=None,
    username=None,
    start_date=None,
    end_date=None,
    number_of_flashcards=None,
):
    query = FlashcardSet.objects.all()
    if topic:
        query = query.filter(topic__icontains=topic)
    if level and level != "":
        query = query.filter(study_level__icontains=level)
    if username:
        query = query.filter(user__username__icontains=username)
    if number_of_flashcards and number_of_flashcards != "":
        query = query.filter(number_of_flashcards=number_of_flashcards)
    return query


# Model for managing user's favorite flashcard sets
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    flashcard_set = models.ForeignKey(
        FlashcardSet, on_delete=models.CASCADE, related_name="favorited_by"
    )

    class Meta:
        unique_together = ("user", "flashcard_set")


# Functions for managing favorites
def add_set_to_favorites(user, flashcard_set_id):
    """Add a flashcard set to a user's favorites"""
    try:
        flashcard_set = FlashcardSet.objects.get(id=flashcard_set_id)
        Favorite.objects.create(user=user, flashcard_set=flashcard_set)
    except ObjectDoesNotExist:
        # Handle the case where flashcard_set does not exist
        pass


def remove_set_from_favorites(user, flashcard_set_id):
    """Remove a flashcard set from a user's favorites"""
    try:
        flashcard_set = FlashcardSet.objects.get(id=flashcard_set_id)
        Favorite.objects.filter(user=user, flashcard_set=flashcard_set).delete()
    except FlashcardSet.DoesNotExist:
        # Handle the case where the flashcard set does not exist.
        # For example, you might log this as an error or inform the user.
        pass


def get_user_favorites(user):
    """Get all favorite flashcard sets of a user"""
    return FlashcardSet.objects.filter(favorited_by__user=user)


def is_favorite(user, flashcard_set_id):
    """Check if a flashcard set is in a user's favorites"""
    return Favorite.objects.filter(
        user=user, flashcard_set_id=flashcard_set_id
    ).exists()
