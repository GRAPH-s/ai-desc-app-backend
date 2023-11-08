from django.urls import path
import ai_requests.views as views

urlpatterns = [path("requests-history", views.RequestHistoryAPIList.as_view())]
