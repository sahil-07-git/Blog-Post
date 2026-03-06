from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from blog.models import Post

def signup(request):
  if request.method == "POST":
    form = SignupForm(request.POST)

    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data["password"])
      user.save
    
      return redirect("login")
  
  else:
    form = SignupForm()
  
  return render(request, "registration/signup.html", {
    "form": form
  })

def login(request):
  if request.method == "POST":

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user:
      login(request, user)
      return redirect("dashboard")
    
  return render(request, "registration/login.html")

def logout(request):
  logout(request)

  return redirect("post_list")

@login_required
def dashboard(request):
  draft_posts = Post.objects.filter(author=request.user, status="draft").order_by("-created_at")

  published_posts = Post.objects.filter(author=request.user, status="published").order_by("-created_at")


  return render(request, "accounts/dashboard.html", {
    "draft_posts": draft_posts,
    "published_posts": published_posts
  })