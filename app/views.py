from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from openai import OpenAI, OpenAIError
import json

from .forms import FlashCardsForm, FlashcardSearchForm
from .models import Flashcard, FlashcardSet, create_flashcard_set, advanced_search


# Create your views here.


def home_view(request):
    return render(request, "app/home.html")


@login_required
def flashcards_view(request):
    try:
        client = OpenAI(api_key=request.user.account.openai_key)
    except OpenAIError as e:
        print(f"Error connecting to OpenAI: {e}")
        return HttpResponseServerError("Error connecting to the OpenAI service.")

    form = FlashCardsForm()
    context = {"form": form}

    if request.method == "POST":
        form = FlashCardsForm(request.POST)

        if form.is_valid():
            try:
                topic = form.cleaned_data["topic"]
                study_level = form.cleaned_data["study_level"]
                number_of_flashcards = form.cleaned_data["number_of_flashcards"]

                print("Starting...")
                print("Sending request...")

                flashcards = make_chat_request(
                    f"""Generate a set of flashcards for the following specifications:
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

The response should be in JSON format like this [{{'question': ..., 'answer'}}, ...]""",
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
                        new_flashcard_set_id = new_flashcard_set.id
                        print("Flashcards created!")
                        print("Redirecting...")
                        return redirect("flashcard_set", set_id=new_flashcard_set_id)
                    else:
                        raise ValueError("Invalid response format from API")
                except json.JSONDecodeError:
                    print("Error parsing JSON response")
                    return HttpResponseServerError("Error processing the response.")

            except Exception as e:
                print(f"Error: {e}")
                return HttpResponseServerError(
                    "An error occurred while processing your request."
                )

    return render(request, "app/create_flashcards.html", context=context)


def make_chat_request(message, client):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": "You are the perfect study assistant, skilled in explaining complex topics with creative flair. Optimizing for a study session and later recall.",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        response_format={"type": "json_object"},
    )

    return completion.choices[0].message.content


def flashcard_set_view(request, set_id):
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    flashcards = flashcard_set.flashcards.all()

    return render(request, "app/study_flashcards.html", {"flashcards": flashcards})


def find_flashcards(request):
    search_results = None
    if request.method == "POST":
        form = FlashcardSearchForm(request.POST)
        if form.is_valid():
            # Use your search functions based on the form data
            # Example:
            search_results = advanced_search(
                topic=form.cleaned_data.get("topic"),
                level=form.cleaned_data.get("study_level"),
                user_id=form.cleaned_data.get("user_id"),
                start_date=form.cleaned_data.get("start_date"),
                end_date=form.cleaned_data.get("end_date"),
                # Add other criteria as needed
            )
    else:
        form = FlashcardSearchForm()

    return render(
        request,
        "app/find_flashcards.html",
        {"form": form, "search_results": search_results},
    )
