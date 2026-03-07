from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404
from django.db.models import Q, Count
from .models import Post, Reaction, Comment, UserProfile
from .forms import PostForm, CommentForm, ReplyForm, UserProfileForm


# ─────────────────────────────────────────
# Post list — search, filter, sort
# ─────────────────────────────────────────


def post_list(request):
    posts = Post.objects.filter(status="published")

    # Search
    query = request.GET.get("q", "").strip()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    # Filter by author
    author_filter = request.GET.get("author", "").strip()
    if author_filter:
        posts = posts.filter(author__username__icontains=author_filter)

    # Sort
    sort = request.GET.get("sort", "newest")
    if sort == "oldest":
        posts = posts.order_by("created_at")
    elif sort == "most_liked":
        posts = posts.annotate(
            num_likes=Count("reactions", filter=Q(reactions__reaction="like"))
        ).order_by("-num_likes")
    else:
        posts = posts.order_by("-created_at")

    # All authors for the filter dropdown
    authors = (
        User.objects.filter(post__status="published").distinct().order_by("username")
    )

    return render(
        request,
        "blog/post_list.html",
        {
            "posts": posts,
            "query": query,
            "author_filter": author_filter,
            "sort": sort,
            "authors": authors,
        },
    )


# ─────────────────────────────────────────
# Post detail — with threaded comments
# ─────────────────────────────────────────


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.status == "draft" and post.author != request.user:
        raise Http404

    # Only top-level comments; replies come via comment.replies.all in template
    comments = (
        post.comments.filter(parent=None)
        .prefetch_related("replies__author")
        .select_related("author")
    )

    comment_form = CommentForm()
    reply_form = ReplyForm()

    user_reaction = None
    if request.user.is_authenticated:
        reaction_obj = post.reactions.filter(user=request.user).first()
        user_reaction = reaction_obj.reaction if reaction_obj else None

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_form": comment_form,
            "reply_form": reply_form,
            "user_reaction": user_reaction,
        },
    )


# ─────────────────────────────────────────
# Add top-level comment
# ─────────────────────────────────────────


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.parent = None
            comment.save()
            messages.success(request, "Comment added.")

    return redirect("post_detail", post_id=post_id)


# ─────────────────────────────────────────
# Add reply to a comment
# ─────────────────────────────────────────


@login_required
def add_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = get_object_or_404(Comment, id=comment_id, post=post, parent=None)

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.author = request.user
            reply.parent = parent_comment
            reply.save()
            messages.success(request, "Reply added.")

    return redirect("post_detail", post_id=post_id)


# ─────────────────────────────────────────
# Reactions
# ─────────────────────────────────────────


@login_required
def react_to_post(request, post_id, reaction_type):
    if reaction_type not in ("like", "dislike"):
        return redirect("post_detail", post_id=post_id)

    post = get_object_or_404(Post, id=post_id)
    reaction_obj, created = Reaction.objects.get_or_create(
        user=request.user, post=post, defaults={"reaction": reaction_type}
    )

    if not created:
        if reaction_obj.reaction == reaction_type:
            reaction_obj.delete()
        else:
            reaction_obj.reaction = reaction_type
            reaction_obj.save()

    return redirect("post_detail", post_id=post_id)


# ─────────────────────────────────────────
# User profile (public view)
# ─────────────────────────────────────────


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=profile_user)
    published_posts = Post.objects.filter(
        author=profile_user, status="published"
    ).order_by("-created_at")

    return render(
        request,
        "blog/user_profile.html",
        {
            "profile_user": profile_user,
            "profile": profile,
            "published_posts": published_posts,
        },
    )


# ─────────────────────────────────────────
# Edit own profile
# ─────────────────────────────────────────


@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("user_profile", username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "blog/edit_profile.html", {"form": form})


# ─────────────────────────────────────────
# CRUD + publish
# ─────────────────────────────────────────


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


def home(request):
    latest_posts = Post.objects.filter(status="published").order_by("-created_at")[:3]
    return render(request, "blog/home.html", {"latest_posts": latest_posts})
