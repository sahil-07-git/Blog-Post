from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Post, Reaction, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.filter(status="published").order_by("-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Draft posts are only visible to their author
    if post.status == "draft" and post.author != request.user:
        raise Http404
    
    comments = post.comments.select_related("author").all()
    comments_form = CommentForm()

    # Current user's reaction on this post
    user_reaction =  None
    if request.user.is_authenticated:
        reaction_obj = post.reactions.filter(user=request.user).first()
        user_reaction = reaction_obj.reaction if reaction_obj else None

    return render(request, "blog/post_detail.html", {
        "post": post,
        "comments": comments,
        "comment_form": comments_form,
        "user_reaction": user_reaction,
    })


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added.")
    
    return redirect("post_detail", post_id=post_id)


@login_required
def react_to_post(request, post_id, reaction_type):
    if reaction_type not in ("like", "dislike"):
        return redirect("post_detail", post_id=post_id)
    
    post = get_object_or_404(Post, id=post_id)
    reaction_obj, created = Reaction.objects.get_or_create(
        user = request.user,
        post = post,
        defaults = {"reaction": reaction_type}
    )

    if not created:
        if reaction_obj.reaction == reaction_type:
            reaction_obj.delete()
        else:
            reaction_obj.reaction = reaction_type
            reaction_obj.save()
    
    return redirect("post_detail", post_id=post_id)

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect("post_list")
    else:
        form = PostForm()

    return render(request, "blog/create_post.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect("post_list")
    else:
        form = PostForm(instance=post)

    return render(request, "blog/edit_post.html", {"form": form, "post": post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("post_list")

    return render(request, "blog/delete_post.html", {"post": post})


@login_required
def publish_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.status = "published"
    post.save()
    messages.success(request, "Post published!")
    return redirect("dashboard")
