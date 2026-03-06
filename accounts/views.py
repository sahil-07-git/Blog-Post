from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from blog.models import Post
from django.contrib import messages


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            login(request, user)

            messages.success(request, "Account created successfully!")

            return redirect("dashboard")

    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, "Welcome back!")

            return redirect("dashboard")

    else:
        form = LoginForm(request)

    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)

    messages.info(request, "You have been logged out.")

    return redirect("login")


@login_required
def dashboard(request):
    draft_posts = Post.objects.filter(author=request.user, status="draft").order_by(
        "-created_at"
    )

    published_posts = Post.objects.filter(
        author=request.user, status="published"
    ).order_by("-created_at")

    return render(
        request,
        "accounts/dashboard.html",
        {"draft_posts": draft_posts, "published_posts": published_posts},
    )
