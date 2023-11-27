from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import AccountRegistrationForm, UserSettingsForm, AccountUpdateForm


# Create your views here.
def register(request):
    form = AccountRegistrationForm()

    if request.POST:
        form = AccountRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Account created for {username}!")
            return redirect("login")

    return render(request, "users/register.html", context={"form": form})


@login_required
def settings(request):
    u_form = UserSettingsForm(instance=request.user)
    a_form = AccountUpdateForm(instance=request.user.account)

    if request.POST:
        u_form = UserSettingsForm(request.POST, instance=request.user)
        a_form = AccountUpdateForm(request.POST, instance=request.user.account)

        if u_form.is_valid() and a_form.is_valid():
            u_form.save()
            a_form.save()

            messages.success(request, f"Changes saved successfully!")
            return redirect("home")

    context = {
        "u_form": u_form,
        "a_form": a_form,
    }

    return render(request, "users/settings.html", context=context)
