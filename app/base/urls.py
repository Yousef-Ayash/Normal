from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("login/", LoginView.as_view(template_name='base/login.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("", views.HomeView.as_view(), name="home"),
    path(
        "create-post",
        views.CreatePostView.as_view(),
        name="create-post",
    ),
    path(
        "update-post/<slug:slug>",
        views.UpdatePostView.as_view(),
        name="update-post",
    ),
    path(
        "delete/<slug:slug>",
        views.DeletePostView.as_view(),
        name="delete-post",
    ),
    path("@<str:username>/post/<slug:slug>", views.PostView.as_view(), name="post"),
    path(
        "@<str:username>/post/<slug:slug>/like/",
        views.post_like_toggle,
        name="like-toggle",
    ),
]
