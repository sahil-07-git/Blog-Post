from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

def post_list(request):
  posts = Post.objects.filter(status="published").order_by("-created_at")
  return render(request, "blog/post_list.html", {
    "posts": posts
  })    

def post_detail(request, post_id):
  post = get_object_or_404(Post, id=post_id)
  return render(request, "blog/post_detail.html", {
    "post": post
  })

def create_post(request):
  if request.method == "POST":
    title = request.POST.get("title")
    content = request.POST.get("content")
    status = request.POST.get("status")

    Post.objects.create(
      title=title,
      content=content,
      status=status,
      author=request.user
    )

    return redirect("post_list")

  return render(request, "blog/create_post.html")

def edit_post(request, post_id):
  post = get_object_or_404(Post, id=post_id)

  if request.method == "POST":
    post.title = request.POST.get("title")
    post.content = request.POST.get("content")
    post.status = request.POST.get("status")

    post.save()

    return redirect("post_list")
  
  return render(request, "blog/edit_post.html", {
    "post": post
  })

def delete_post(request, post_id):
  post = get_object_or_404(Post, id=post_id)

  if request.method  == "POST":
    post.delete()
    return redirect("post_list")
  
  return render(request, "blog/delete_post.html", {
    "post": post
  })