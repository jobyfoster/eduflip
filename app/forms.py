from django import forms


class FlashCardsForm(forms.Form):
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
        super(FlashCardsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


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
    user_id = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    number_of_flashcards = forms.ChoiceField(
        choices=NUMBER_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
