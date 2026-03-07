from django import forms
from .models import Post, Comment, UserProfile


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "content": forms.Textarea(attrs={"placeholder": "Write your post here..."}),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "placeholder": "Write a comment...",
                    "rows": 3,
                }
            )
        }
        labels = {"body": ""}


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "placeholder": "Write a reply...",
                    "rows": 2,
                }
            )
        }
        labels = {"body": ""}


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["bio"]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "placeholder": "Tell readers a little about yourself...",
                    "rows": 4,
                }
            )
        }
        labels = {"bio": "Bio"}
