from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseServerError
from openai import OpenAI, OpenAIError
import json
import openai

from .forms import GenerateFlashCardsForm, FlashcardSearchForm
from .models import (
    Flashcard,
    FlashcardSet,
    Resource,
    Favorite,
    create_flashcard_set,
    advanced_search,
    search_by_username,
    search_by_id,
    get_user_favorites,
    is_favorite,
    add_set_to_favorites,
    remove_set_from_favorites,
    add_resource_to_flashcard_set,
    get_resources_for_flashcard_set,
)


# Create your views here.
def home_view(request):
    return render(request, "app/home.html")


def is_api_key_valid(key):
    try:
        client = OpenAI(api_key=key)
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt='This is a test. respond with "a"',
            max_tokens=5,
        )
    except Exception as ex:
        print(ex)
        return False
    else:
        return True


@login_required
def generate_flashcards_view(request):
    error_messages = []
    form = GenerateFlashCardsForm()

    print("Testing API key")
    if not is_api_key_valid(request.user.account.openai_key):
        error_messages.append(
            "Invalid or expired OpenAI API key. Please check your settings."
        )

    try:
        client = OpenAI(api_key=request.user.account.openai_key)
    except OpenAIError as e:
        print(e)
        error_messages.append(f"Error connecting to OpenAI: {e}")

    if request.method == "POST":
        form = GenerateFlashCardsForm(request.POST)

        if form.is_valid():
            try:
                topic = form.cleaned_data["topic"]
                study_level = form.cleaned_data["study_level"]
                number_of_flashcards = form.cleaned_data["number_of_flashcards"]

                print("Starting...")
                print("Sending request...")

                flashcards = generate_flashcards(
                    topic,
                    study_level,
                    number_of_flashcards,
                    client,
                )

                try:
                    print("Received response")
                    flashcards_data = json.loads(flashcards)
                    if "flashcards" in flashcards_data:
                        print("Making flashcards...")
                        new_flashcard_set = create_flashcard_set(
                            request.user,
                            flashcards_data["flashcards"],
                            topic,
                            study_level,
                            number_of_flashcards,
                        )

                        additional_resources = flashcards_data["additional_resources"]

                        for resource in additional_resources:
                            add_resource_to_flashcard_set(
                                new_flashcard_set.id,
                                resource["title"],
                                resource["link"],
                                resource["description"],
                            )

                        new_flashcard_set_id = new_flashcard_set.id
                        print("Flashcards created!")
                        print("Redirecting...")
                        return redirect(
                            "view_flashcard_set", set_id=new_flashcard_set_id
                        )
                    else:
                        raise ValueError("Invalid response format from API")
                except json.JSONDecodeError:
                    print("Error parsing JSON response")
                    return HttpResponseServerError("Error processing the response.")

            except Exception as e:
                print(f"Error: {e}")
                return HttpResponseServerError(
                    "An error occurred while processing your request. Please check your OpenAI API key in the settings."
                )

    context = {"form": form, "error_messages": error_messages}
    return render(request, "app/create_flashcards.html", context=context)


def generate_flashcards(topic, study_level, number_of_flashcards, client):
    prompt = f"""Generate a set of flashcards for the following specifications:
- Topic: {topic}
- Study Level: {study_level}
- Number of Flashcards: {number_of_flashcards}

Each flashcard should contain:
1. A concise question or concept on one side, relevant to the chosen topic and study level.
2. A clear, informative answer or explanation on the other side, designed to enhance understanding and retention.

Guidelines for Flashcard Creation:
- For Beginner level, focus on fundamental concepts and definitions. Use simple language and examples.
- For Intermediate level, include more detailed explanations and practical applications.
- For Expert level, delve into advanced theories, complex problems, and current research trends in the field.
- Ensure the content is factual, up-to-date, and sourced from credible educational materials.
- Structure the information to promote active recall and spaced repetition.

Note: The goal is to create flashcards that are not only informative but also engaging and conducive to effective learning. Each card should encourage deeper exploration of the topic and aid in building a strong foundation or advancing existing knowledge.

The response should be in JSON format like this {{'flashcards': [{{'question': ..., 'answer'}}, ..., 'additional_resources': [{{"title": "Resource Title 1", "link": "https://example.com/resource1", "description": "Brief description of Resource 1"}},...]}}

Do not include the resource if the link for it is not reliable.
"""

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": "You are the perfect study assistant, skilled in explaining complex topics with creative flair. Optimizing for a study session and later recall.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={"type": "json_object"},
    )

    return completion.choices[0].message.content


def flashcard_set_view(request, set_id):
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    flashcards = flashcard_set.flashcards.all()
    try:
        additional_resources = get_resources_for_flashcard_set(set_id)
    except ValueError:
        additional_resources = []

    print(additional_resources)

    is_favorited = is_favorite(user=request.user, flashcard_set_id=set_id)
    is_owner = flashcard_set.user == request.user

    return render(
        request,
        "app/study_flashcards.html",
        {
            "flashcards": flashcards,
            "flashcard_set": flashcard_set,
            "additional_resources": additional_resources,
            "is_favorited": is_favorited,
            "is_owner": is_owner,
        },
    )


def search_flashcards(request):
    search_results = None
    if request.method == "POST":
        form = FlashcardSearchForm(request.POST)
        if form.is_valid():
            # Use your search functions based on the form data
            # Example:
            search_results = advanced_search(
                topic=form.cleaned_data.get("topic"),
                level=form.cleaned_data.get("study_level"),
                number_of_flashcards=form.cleaned_data.get("number_of_flashcards"),
                username=form.cleaned_data.get("username"),
            )
    else:
        form = FlashcardSearchForm()

    return render(
        request,
        "app/find_flashcards.html",
        {"form": form, "search_results": search_results},
    )


@login_required
def user_flashcards(request):
    created_flashcards = search_by_username(request.user.username)
    favorited_flashcards = get_user_favorites(user=request.user)

    # Combine and mark which sets are favorited
    user_flashcards = []
    for flashcard_set in (created_flashcards | favorited_flashcards).distinct():
        flashcard_set.is_favorited = flashcard_set in favorited_flashcards
        user_flashcards.append(flashcard_set)

    return render(
        request,
        "app/user_flashcards.html",
        context={"user_flashcards": user_flashcards},
    )


@login_required
def add_to_favorites(request, set_id):
    flashcard_set = search_by_id(set_id=set_id)
    add_set_to_favorites(user=request.user, flashcard_set_id=set_id)
    return redirect(
        "view_flashcard_set", set_id=set_id
    )  # Redirect to the detail page of the flashcard set


@login_required
def remove_from_favorites(request, set_id):
    remove_set_from_favorites(user=request.user, flashcard_set_id=set_id)
    return redirect("view_flashcard_set", set_id=set_id)


@login_required
def delete_flashcard_set(request, set_id):
    flashcard_set = get_object_or_404(FlashcardSet, pk=set_id)

    # Check if the current user is the owner of the flashcard set
    if request.user != flashcard_set.user:
        messages.error(
            request, "You do not have permission to delete this flashcard set."
        )
        return redirect(reverse("view_flashcard_set", set_id=set_id))

    # Delete operation
    if request.method == "POST":
        flashcard_set.delete()
        messages.success(request, "Flashcard set deleted successfully.")
        return redirect(reverse("home"))  # Redirect to a relevant page

    context = {"flashcard_set": flashcard_set}
    return render(request, "app/delete_set_confirmation.html", context)
