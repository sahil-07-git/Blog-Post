from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    STATUS_CHOICES = (("draft", "Draft"), ("published", "Published"))
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def like_count(self):
        return self.reactions.filter(reaction="like").count()

    def dislike_count(self):
        return self.reactions.filter(reaction="dislike").count()

    def comment_count(self):
        return self.comments.count()


class Reaction(models.Model):
    REACTION_CHOICES = (
        ("like", "Like"),
        ("dislike", "Dislike"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} — {self.reaction} — {self.post}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    # parent is None for top-level comments, set for replies
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def is_reply(self):
        return self.parent is not None

    def __str__(self):
        return f"{self.author} on {self.post}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.user.username}'s profile"

    def total_likes_received(self):
        return Reaction.objects.filter(post__author=self.user, reaction="like").count()

    def total_comments_made(self):
        return Comment.objects.filter(author=self.user).count()
