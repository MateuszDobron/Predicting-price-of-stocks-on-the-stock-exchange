from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home_page, name="home-page"),
    path("model/", views.model_page, name="model-page"),
    path("profile/", views.profile, name="profile-page"),
    path("ai-model/", views.ai_model, name="ai-model"),
    path("ai-model/prediction/", views.ai_model_prediction, name="ai-model-prediction"),
    path("ai-model/upload/", views.ai_model_upload, name="ai-model-upload")
]
