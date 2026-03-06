from django.urls import path
from .views import post_list, post_detail, create_post, edit_post, delete_post

urlpatterns = [
    path("posts/", post_list, name="post_list"),
    path("post/<int:post_id>/", post_detail, name="post_detail"),
    path("create-post/", create_post, name="create_post"),
    path("edit-post/<int:post_id>/", edit_post, name="edit_post"),
    path("delete-post/<int:post_id>/", delete_post, name="delete_post"),
]
