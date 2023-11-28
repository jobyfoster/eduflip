from django import forms
from django.forms import ValidationError


class GenerateFlashCardsForm(forms.Form):
    STUDY_LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("expert", "Expert"),
    ]

    NUMBER_CHOICES = [
        (10, "10"),
        (15, "15"),
        (20, "20"),
    ]

    topic = forms.CharField()
    study_level = forms.ChoiceField(choices=STUDY_LEVEL_CHOICES)
    number_of_flashcards = forms.ChoiceField(choices=NUMBER_CHOICES)

    def __init__(self, *args, **kwargs):
        super(GenerateFlashCardsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def clean_topic(self):
        topic = self.cleaned_data.get("topic")
        if len(topic) > 100:  # Example limit
            raise ValidationError(
                "Topic name is too long. Must be under 100 characters."
            )

        if len(topic) <= 3:
            raise ValidationError(
                "Topic name is too short. Must be above 3 characters."
            )

        return topic


class FlashcardSearchForm(forms.Form):
    STUDY_LEVEL_CHOICES = [
        ("", "None"),
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("expert", "Expert"),
    ]

    NUMBER_CHOICES = [
        ("", "None"),
        (10, "10"),
        (15, "15"),
        (20, "20"),
    ]

    topic = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    study_level = forms.ChoiceField(
        choices=STUDY_LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    number_of_flashcards = forms.ChoiceField(
        choices=NUMBER_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def clean_topic(self):
        topic = self.cleaned_data.get("topic")
        if topic and len(topic) > 100:
            raise ValidationError(
                "Topic name is too long. Must be under 100 characters."
            )

        if topic and len(topic) <= 3:
            raise ValidationError("Topic name is too short. Must be over 3 characters.")
        return topic

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and not username.isalnum():
            raise ValidationError(
                "Username should only contain alphanumeric characters."
            )
        return username
