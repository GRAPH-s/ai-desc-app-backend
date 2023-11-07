from django.urls import path
from ai_service import views

urlpatterns = [path("test", views.AiServiceWithDescription.as_view())]
