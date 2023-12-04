from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("home/", views.home_page, name="home-page"),
    path("model/", views.model_page, name="model-page"),
    path("profile/", views.profile, name="profile-page"),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", views.register, name="register"),
    path("ai-model/", views.ai_model, name="ai-model"),
    path("ai-model/prediction/", views.ai_model_prediction, name="ai-model-prediction"),
    path("ai-model/upload/", views.ai_model_upload, name="ai-model-upload")
]
